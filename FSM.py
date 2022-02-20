from queue import SimpleQueue
from tabulate import tabulate


class FSM:
    def __init__(self, sts=None, sgm=None):
        """
        sts: tuples of states. sgm: tuples of alphabet, '^' will be considered as
        epsilon.
        """
        self.states = dict()
        if sts is not None:
            for s in sts:
                self.states[s] = State(s)

        if sgm is not None:
            self.sigma = sgm
        else:
            self.sigma = tuple("ab")

        self.initial_state = None  # name of state
        self.accepting_states = set()  # names of state

    def add_state(self, name):
        self.states[name] = State(name)

    def set_initial(self, state):
        self.initial_state = state

    def add_accepting(self, state):
        self.accepting_states.add(state)
        self.states[state].accepting = True

    # add transition (next state) from s1 to s2
    def add_transition(self, s1, label, s2):
        if label in self.states[s1].next:
            self.states[s1].next[label].append(s2)
        else:
            self.states[s1].next[label] = [s2]

    def eps(self, state_name):
        state = self.states[state_name]
        result = {state}
        process = SimpleQueue()
        process.put(state)
        while not process.empty():
            p = process.get()
            if "^" in p.next:
                nexts = p.next["^"]
                for n in nexts:
                    next_state = self.states[n]
                    if next_state not in result:
                        result.add(next_state)
                        process.put(next_state)
        return result

    def ndfsm_simulate(self, w):
        st = self.eps(self.initial_state)
        st1 = set()
        for c in w:
            st1 = set()
            for q in st:
                if c in q.next:
                    p = q.next[c]
                    for p_state in p:
                        st1 |= self.eps(p_state)
            st = st1
            if st == set():
                break
        acc_set = {self.states[x] for x in self.accepting_states}
        return (st & acc_set) != set()

    def dfsm_simulate(self, w):
        st = self.states[self.initial_state]
        for c in w:
            st = self.states[st.next[c][0]]
        acc_set = {self.states[x] for x in self.accepting_states}
        return st in acc_set

    def ndfsm_to_dfsm(self):
        """Returns quintuple (K, Σ, δ, s, A) of tuples K, Σ, δ, A and string s.
        K -> states.
        Σ -> alphabet.
        δ -> transition function.
        s -> starting state.
        A -> accepting states."""
        epsilons = dict()
        for s in self.states:
            epsilons[s] = self.eps(s)

        start = epsilons[self.initial_state]

        active_state = set()
        deltas = set()
        process = SimpleQueue()
        start_tuple = self.state_set_to_tuple(start)

        # active_state.add(start_tuple)
        process.put(start_tuple)

        data = []  # to print tabulate

        while not process.empty():
            data_row = []  # to print tabulate
            state_tuple = process.get()
            if state_tuple not in active_state:
                active_state.add(state_tuple)
                data_row.append(self.state_tuple_to_string(state_tuple))
                for c in self.sigma:
                    new_state = set()
                    for q in state_tuple:
                        if c in q.next:
                            p = q.next[c]
                            for p_state in p:
                                new_state |= self.eps(p_state)
                    new_state_tuple = self.state_set_to_tuple(new_state)
                    deltas.add((state_tuple, c, new_state_tuple))
                    data_row.append(self.state_tuple_to_string(new_state_tuple))
                    if new_state_tuple not in active_state:
                        # active_state.add(new_state_tuple)
                        process.put(new_state_tuple)
            else:
                continue
            data.append(data_row)

        active_state_name = {tuple(x.name for x in y) for y in active_state}
        new_acc_states = {
            x for x in active_state_name if (set(x) & self.accepting_states != set())
        }

        new_init_state = self.state_tuple_to_string(start_tuple)

        print(tabulate(data, headers=["Active State"] + list(self.sigma)))
        print("accepting states:", new_acc_states)
        print("initial state:", new_init_state)

        # print(data)
        return (
            tuple(active_state_name),
            self.sigma,
            tuple(deltas),
            new_init_state,
            tuple(new_acc_states),
        )

    def state_set_to_tuple(self, states):
        states = list(states)
        states.sort(key=lambda x: x.name)
        states = tuple(states)
        return states

    def state_tuple_to_string(self, states):
        if len(states) == 0:
            return "{}"
        return ",".join(str(s.name) for s in states)


class State:
    def __init__(self, name):
        self.name = name
        self.next = dict()
        self.accepting = False


def main():
    a = FSM()
    a.add_state(0)
    a.add_state(1)
    a.add_state(2)
    a.add_state(3)

    a.set_initial(0)
    a.add_accepting(2)

    a.add_transition(0, "a", 3)
    a.add_transition(0, "^", 1)

    a.add_transition(1, "a", 0)
    a.add_transition(1, "b", 2)
    a.add_transition(1, "^", 2)

    a.add_transition(2, "^", 0)

    a.add_transition(3, "b", 2)

    # a.ndfsm_to_dfsm()

    # visualization of b: https://prnt.sc/Zf3bA5kSKkvL
    b = FSM(sts=(1, 2, 3, 4, 5, 6, 7, 8), sgm=("a", "b", "c"))
    b.add_transition(1, "b", 1)
    b.add_transition(1, "^", 2)

    b.add_transition(2, "^", 7)
    b.add_transition(2, "b", 3)
    b.add_transition(2, "b", 5)

    b.add_transition(3, "a", 4)
    b.add_transition(3, "c", 4)

    b.add_transition(4, "c", 2)
    b.add_transition(4, "c", 7)

    b.add_transition(5, "a", 6)
    b.add_transition(5, "b", 6)

    b.add_transition(6, "^", 2)
    b.add_transition(6, "c", 2)
    b.add_transition(6, "c", 7)

    b.add_transition(7, "b", 8)

    b.set_initial(1)
    b.add_accepting(8)

    b.ndfsm_to_dfsm()


def print_eps(e):
    for i in e:
        print(i.name, end=" ")
    print()


if __name__ == "__main__":
    main()
