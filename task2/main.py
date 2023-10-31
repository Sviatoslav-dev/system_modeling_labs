import numpy as np

from element_create import ElementCreate
from element_process import ElementProcess
from model import Model

create = ElementCreate(delay=0.5, name="Create")
cashier1 = ElementProcess(delay=0.3, name="Cashier1", max_queue=3, count_of_workers=1)
cashier2 = ElementProcess(delay=0.3, name="Cashier2", max_queue=3, count_of_workers=1)

create.t_state = 0.1

cashier1.distribution = np.random.normal
cashier1.delay = (1, 0.3)
cashier1.in_act(0, 0.0001, 1)
cashier1.queue = [0.01, 0.01]
cashier1.distribution = np.random.exponential
cashier1.delay = 0.3

cashier2.distribution = np.random.normal
cashier2.delay = (1, 0.3)
cashier2.in_act(0, 0.0001, 1)
cashier2.queue = [0.01, 0.01]
cashier2.distribution = np.random.exponential
cashier2.delay = 0.3


create.set_next_elements([cashier1, cashier2], priorities=[1, 0])

elements = [create, cashier1, cashier2]
model = Model(elements)
model.simulate(1000)
