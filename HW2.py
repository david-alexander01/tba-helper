from FSM import *

# HW 2 no 1
print("NO 1")
fsm1 = FSM(sts=("A", "B", "C", "D", "E", "F"), sgm=("a", "b"))

fsm1.set_initial("A")
fsm1.add_accepting("F")

fsm1.add_transition("A", "a", "A")
fsm1.add_transition("A", "b", "B")
fsm1.add_transition("A", "^", "E")
fsm1.add_transition("A", "^", "D")

fsm1.add_transition("B", "^", "C")

fsm1.add_transition("C", "a", "E")

fsm1.add_transition("D", "a", "F")

fsm1.add_transition("E", "b", "B")
fsm1.add_transition("E", "^", "F")

fsm1.add_transition("F", "a", "F")
fsm1.add_transition("F", "b", "D")

fsm1.ndfsm_to_dfsm()

# HW 2 no 2
print("\nNO 2")
fsm2 = FSM(sts=("A", "B", "C", "D", "E", "F"), sgm=("a", "b"))

fsm2.set_initial("A")
fsm2.add_accepting("F")

fsm2.add_transition("A", "b", "A")
fsm2.add_transition("A", "^", "D")
fsm2.add_transition("A", "a", "B")
fsm2.add_transition("A", "a", "E")

fsm2.add_transition("B", "^", "C")

fsm2.add_transition("C", "b", "E")

fsm2.add_transition("D", "a", "F")

fsm2.add_transition("E", "b", "B")
fsm2.add_transition("E", "a", "F")

fsm2.add_transition("F", "b", "F")
fsm2.add_transition("F", "b", "D")

fsm2.ndfsm_to_dfsm()

# HW 2 no 3
print("\nNO 3")
fsm3 = FSM(sts=("A", "B", "C", "D", "E", "F"), sgm=("a", "b"))

fsm3.set_initial("A")
fsm3.add_accepting("F")

fsm3.add_transition("A", "b", "A")
fsm3.add_transition("A", "^", "B")
fsm3.add_transition("A", "a", "E")
fsm3.add_transition("A", "b", "D")

fsm3.add_transition("B", "a", "C")

fsm3.add_transition("C", "^", "E")

fsm3.add_transition("D", "a", "F")

fsm3.add_transition("E", "^", "F")
fsm3.add_transition("E", "b", "B")

fsm3.add_transition("F", "a", "F")
fsm3.add_transition("F", "b", "D")

fsm3.ndfsm_to_dfsm()