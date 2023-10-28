from element_create import ElementCreate
from element_process import ElementProcess
from model import Model

create = ElementCreate(delay=0.5, name="Create")
process1 = ElementProcess(delay=0.3, name="Process1", max_queue=3, count_of_workers=1)
process2 = ElementProcess(delay=0.3, name="Process2", max_queue=3, count_of_workers=1)

create.set_next_elements([process1, process2], priorities=[1, 0])

elements = [create, process1, process2]
model = Model(elements)
model.simulate(1000)