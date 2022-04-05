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
        print("\nNDSFM Simulate")
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
        print("\nDFSM Simulate")
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
        print("\nNDFSM to DFSM")
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

    def min_dfsm(self):
        print("\nMinimize DFSM")
        acc = list(sorted(list(self.accepting_states)))
        k_min_acc = list(sorted(list(self.states.keys() - self.accepting_states)))
        classes = [acc, k_min_acc]
        step = 1
        while True:
            print("Step", step)
            print("classes:", classes)
            step += 1
            new_classes = []
            to_tabulate = []
            for e in classes:
                outputs = []
                for q in e:
                    e_output = []
                    for c in self.sigma:
                        e_output.append(((q, c), self.get_next_class(q, c, classes)))
                    outputs.append(e_output)
                    tmp_to_tabulate = [q]
                    for i in range(len(self.sigma)):
                        tmp_to_tabulate.append(e_output[i][1])
                    to_tabulate.append(tmp_to_tabulate)
                to_tabulate.append(["-"] * (len(self.sigma) + 1))
                new_classes.extend(self.get_new_classes(outputs))
            print(tabulate(to_tabulate, headers=["State"] + list(self.sigma)))
            if classes == new_classes:
                break
            classes = new_classes

    def get_next_class(self, s, c, classes):
        state = self.states[s]
        next_state = state.next[c][0]
        for next_class in classes:
            if next_state in next_class:
                return next_class
        raise Exception("No class found")

    def get_new_classes(self, outputs):
        new_classes = []
        equivalence_class = []
        for item in outputs:
            item_output = []
            for i in range(len(self.sigma)):
                item_output.append(item[i][1])
            if item_output in equivalence_class:
                idx = equivalence_class.index(item_output)
                new_classes[idx].append(item[0][0][0])
            else:
                equivalence_class.append(item_output)
                new_classes.append([item[0][0][0]])
        return new_classes

    def ndfsm_to_regex(self):
        """Returns string of regular expression from rip states.
        Please make sure the ndfsm fulfills the precondition.
        Initial state should be named init and final state should be
        named acc.
        WARNING: HAVE NOT BEEN THOROUGHLY TESTED, USE WITH CAUTION
        """
        print("\nNDFSM TO REGEX")
        regex = ""

        cur_states = list(self.states.keys())
        to_tabulate = self.create_transition_table()
        cols = cur_states.copy()
        cols.remove("init")
        header = ["State"] + cols
        print(tabulate(to_tabulate, headers=header))
        print("\n")

        while len(to_tabulate) > 1:
            encodings = dict(enumerate(cols[:-1], 1))
            encodings = {str(k): str(v) for k, v in encodings.items()}
            print("Rip state (", end="")
            print(", ".join(":".join(_) for _ in encodings.items()), end="")
            print("): ", end="")
            to_rip = input()
            state_to_rip = encodings[to_rip]
            new_cols = cols.copy()
            new_cols.remove(state_to_rip)

            col_indexes = dict()
            for i in range(1, len(header)):
                col_indexes[header[i]] = i

            ripped_row = []
            for row in to_tabulate:
                if row[0] == state_to_rip:
                    ripped_row = row
                    break

            to_tabulate = [None] + to_tabulate  # convert to one-based indexing
            new_table = []

            ripped_loop = ripped_row[col_indexes[state_to_rip]]
            if ripped_loop != "∅":
                if "U" in ripped_loop:
                    ripped_loop = "(" + ripped_loop + ")*"
                else:
                    ripped_loop = ripped_loop + "*"
            else:
                ripped_loop = ""

            for i in range(1, len(to_tabulate)):
                label = to_tabulate[i][0]
                if label == state_to_rip:
                    continue
                cur_row = to_tabulate[i]
                new_row = [label] + ["."] * (len(to_tabulate[i]) - 2)

                idx = 0
                for j in range(len(cols)):
                    if cols[j] == state_to_rip:
                        continue
                    idx += 1

                    this_to_dest = cur_row[col_indexes[cols[j]]]

                    this_to_ripped = cur_row[col_indexes[state_to_rip]]
                    ripped_to_dest = ripped_row[col_indexes[cols[j]]]

                    if this_to_dest != "∅":
                        if len(this_to_dest) > 1 and this_to_dest.count("U") > 1:
                            this_to_dest = "(" + this_to_dest + ")"
                    else:
                        this_to_dest = ""

                    if this_to_ripped == "∅" or ripped_to_dest == "∅":
                        new_row[idx] = this_to_dest if this_to_dest != "" else "∅"
                        continue

                    temp_regex = (
                        "(" + this_to_dest + ")U"
                        if this_to_dest != "" and "U" in this_to_dest
                        else this_to_dest + "U"
                        if this_to_dest != ""
                        else ""
                    )

                    if this_to_ripped == "^":
                        this_to_ripped = ""
                    else:
                        if len(this_to_ripped) > 1 and this_to_ripped.count("U"):
                            this_to_ripped = f"({this_to_ripped})"

                    if ripped_to_dest == "^":
                        ripped_to_dest = ""
                    else:
                        if len(ripped_to_dest) > 1 and ripped_to_dest.count("U"):
                            ripped_to_dest = f"({ripped_to_dest})"

                    this_to_ripped_to_dest = (
                        f"{this_to_ripped}{ripped_loop}{ripped_to_dest}"
                    )

                    if "U" in this_to_ripped_to_dest and temp_regex != "":
                        temp_regex += "(" + this_to_ripped_to_dest + ")"
                    else:
                        temp_regex += this_to_ripped_to_dest

                    new_row[idx] = temp_regex

                pass
                new_table.append(new_row)

            to_tabulate = new_table

            cols = new_cols
            header = ["State"] + cols
            print(tabulate(to_tabulate, headers=header))
            print("\n")

    def create_transition_table(self):
        cur_states = list(self.states.keys())

        table = []
        cols = cur_states.copy()
        cols.remove("init")
        for s in cur_states:
            if s == "acc":
                continue
            cur_row = []
            cur_row.append(s)
            st = self.states.get(s)
            for next_s in cols:
                ans = ""
                for k, v in st.next.items():
                    if next_s in v:
                        ans += k + "U"
                if ans == "":
                    ans = "∅"
                else:
                    ans = ans[:-1]
                cur_row.append(ans)
            table.append(cur_row)
        return table


class State:
    def __init__(self, name):
        self.name = name
        self.next = dict()
        self.accepting = False


def main():
    # minimize dfsm demo
    # visualization of a: https://prnt.sc/sRIxEdmVPSr9
    a = FSM(sts=(1, 2, 3, 4, 5, 6), sgm=("a", "b"))
    a.add_transition(1, "a", 2)
    a.add_transition(1, "b", 4)

    a.add_transition(2, "a", 3)
    a.add_transition(2, "b", 6)

    a.add_transition(3, "a", 2)
    a.add_transition(3, "b", 4)

    a.add_transition(4, "a", 6)
    a.add_transition(4, "b", 5)

    a.add_transition(5, "a", 2)
    a.add_transition(5, "b", 4)

    a.add_transition(6, "a", 6)
    a.add_transition(6, "b", 6)

    a.add_accepting(2)
    a.add_accepting(4)

    a.set_initial(1)

    a.min_dfsm()

    # convert ndfsm to dfsm demo
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

    # convert ndfsm to regex demo
    # https://docs.google.com/spreadsheets/d/1Esfdl43IZ9DZb-F0cFK4ZkthGIqfWfHlqPPFqjTdG_E/edit#gid=0
    # q5 -> acc
    c = FSM(sts=("init", "A", "B", "C", "D", "acc"), sgm=("a", "b", "c"))

    c.set_initial("init")
    c.add_accepting("acc")

    c.add_transition("init", "^", "A")

    c.add_transition("A", "a", "B")
    c.add_transition("A", "b", "A")
    c.add_transition("A", "c", "A")
    c.add_transition("A", "^", "acc")

    c.add_transition("B", "a", "B")
    c.add_transition("B", "b", "D")
    c.add_transition("B", "c", "A")
    c.add_transition("B", "^", "acc")

    c.add_transition("C", "b", "A")
    c.add_transition("C", "c", "A")
    c.add_transition("C", "^", "acc")

    c.add_transition("D", "a", "B")
    c.add_transition("D", "b", "A")
    c.add_transition("D", "c", "C")
    c.add_transition("D", "^", "acc")

    c.ndfsm_to_regex()
    # input 3, 3, 2, 1 to rip state C, D, B, then A


def print_eps(e):
    for i in e:
        print(i.name, end=" ")
    print()


if __name__ == "__main__":
    main()
