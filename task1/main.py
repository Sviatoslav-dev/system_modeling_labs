from element_create import ElementCreate
from element_process import ElementProcess
from model import Model

create = ElementCreate(delay=1, name="Create")
process1 = ElementProcess(delay=1, name="Process1", max_queue=5, count_of_workers=1)
process2 = ElementProcess(delay=1, name="Process2", max_queue=5, count_of_workers=1)
process3 = ElementProcess(delay=1, name="Process3", max_queue=5, count_of_workers=1)

create.set_next_elements([process1])
process1.set_next_elements([process2, process1, process3],
                           priorities=[2, 3, 1], blocked=[False, True, False])
process2.set_next_elements([process3, process2], probabilities=[0.2, 0.8])

elements = [create, process1, process2, process3]
model = Model(elements)
model.simulate(1000)
