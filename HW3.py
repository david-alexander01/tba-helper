from FSM import *

# HW 3 no 9 (1)
fsm9 = FSM(sts=("A", "B", "C", "D", "E", "F", "G", "H", "J", "K"), sgm=tuple("abc"))

fsm9.add_transition("A", "a", "G")
fsm9.add_transition("A", "b", "E")
fsm9.add_transition("A", "c", "A")

fsm9.add_transition("B", "a", "A")
fsm9.add_transition("B", "b", "E")
fsm9.add_transition("B", "c", "C")

fsm9.add_transition("C", "a", "C")
fsm9.add_transition("C", "b", "F")
fsm9.add_transition("C", "c", "C")

fsm9.add_transition("D", "a", "F")
fsm9.add_transition("D", "b", "D")
fsm9.add_transition("D", "c", "C")

fsm9.add_transition("E", "a", "A")
fsm9.add_transition("E", "b", "K")
fsm9.add_transition("E", "c", "G")

fsm9.add_transition("F", "a", "C")
fsm9.add_transition("F", "b", "D")
fsm9.add_transition("F", "c", "C")

fsm9.add_transition("G", "a", "G")
fsm9.add_transition("G", "b", "H")
fsm9.add_transition("G", "c", "A")

fsm9.add_transition("H", "a", "G")
fsm9.add_transition("H", "b", "J")
fsm9.add_transition("H", "c", "A")

fsm9.add_transition("J", "a", "B")
fsm9.add_transition("J", "b", "K")
fsm9.add_transition("J", "c", "G")

fsm9.add_transition("K", "a", "B")
fsm9.add_transition("K", "b", "K")
fsm9.add_transition("K", "c", "G")

fsm9.add_accepting("C")
fsm9.add_accepting("D")
fsm9.add_accepting("F")

fsm9.set_initial("A")

print("9 (1)")
fsm9.min_dfsm()

# HW 3 no 11 (3)
fsm11 = FSM(sts=("A", "B", "C", "D", "E", "F", "G", "H", "J", "K"), sgm=tuple("abc"))

fsm11.add_transition("A", "a", "B")
fsm11.add_transition("A", "b", "C")
fsm11.add_transition("A", "c", "A")

fsm11.add_transition("B", "a", "D")
fsm11.add_transition("B", "b", "C")
fsm11.add_transition("B", "c", "A")

fsm11.add_transition("C", "a", "F")
fsm11.add_transition("C", "b", "C")
fsm11.add_transition("C", "c", "A")

fsm11.add_transition("D", "a", "E")
fsm11.add_transition("D", "b", "G")
fsm11.add_transition("D", "c", "C")

fsm11.add_transition("E", "a", "D")
fsm11.add_transition("E", "b", "G")
fsm11.add_transition("E", "c", "C")

fsm11.add_transition("F", "a", "E")
fsm11.add_transition("F", "b", "C")
fsm11.add_transition("F", "c", "C")

fsm11.add_transition("G", "a", "F")
fsm11.add_transition("G", "b", "A")
fsm11.add_transition("G", "c", "H")

fsm11.add_transition("H", "a", "K")
fsm11.add_transition("H", "b", "H")
fsm11.add_transition("H", "c", "H")

fsm11.add_transition("J", "a", "H")
fsm11.add_transition("J", "b", "K")
fsm11.add_transition("J", "c", "H")

fsm11.add_transition("K", "a", "J")
fsm11.add_transition("K", "b", "H")
fsm11.add_transition("K", "c", "H")

fsm11.add_accepting("H")
fsm11.add_accepting("J")
fsm11.add_accepting("K")

fsm11.set_initial("A")

print("11 (3)")
fsm11.min_dfsm()

# HW 3 no 14 (6)
fsm14 = FSM(sts=("A", "B", "C", "D", "E", "F", "G", "H", "J", "K"), sgm=tuple("abc"))

fsm14.add_transition("A", "a", "H")
fsm14.add_transition("A", "b", "A")
fsm14.add_transition("A", "c", "B")

fsm14.add_transition("B", "a", "C")
fsm14.add_transition("B", "b", "B")
fsm14.add_transition("B", "c", "A")

fsm14.add_transition("C", "a", "H")
fsm14.add_transition("C", "b", "E")
fsm14.add_transition("C", "c", "B")

fsm14.add_transition("D", "a", "C")
fsm14.add_transition("D", "b", "B")
fsm14.add_transition("D", "c", "G")

fsm14.add_transition("E", "a", "C")
fsm14.add_transition("E", "b", "D")
fsm14.add_transition("E", "c", "A")

fsm14.add_transition("F", "a", "G")
fsm14.add_transition("F", "b", "G")
fsm14.add_transition("F", "c", "K")

fsm14.add_transition("G", "a", "G")
fsm14.add_transition("G", "b", "F")
fsm14.add_transition("G", "c", "K")

fsm14.add_transition("H", "a", "H")
fsm14.add_transition("H", "b", "E")
fsm14.add_transition("H", "c", "A")

fsm14.add_transition("J", "a", "H")
fsm14.add_transition("J", "b", "A")
fsm14.add_transition("J", "c", "K")

fsm14.add_transition("K", "a", "G")
fsm14.add_transition("K", "b", "K")
fsm14.add_transition("K", "c", "K")

fsm14.add_accepting("F")
fsm14.add_accepting("G")
fsm14.add_accepting("K")

fsm14.set_initial("A")

print("14 (6)")
fsm14.min_dfsm()
