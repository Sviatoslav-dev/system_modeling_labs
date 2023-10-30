import random
import numpy as np


class Element:
    def __init__(self, delay, name, max_queue=0):
        self.mean_queue = 0
        self.t_state = 0
        self.delay = delay
        self.total_work_time = 0

        self.state = 0
        self.queue = 0
        self.max_queue = max_queue
        self.failure = 0
        self.served = 0

        self.next_elements = None
        self.name = name

        self.probabilities = None
        self.blocked = None
        self.priorities = None

    def in_act(self, t_curr):
        pass

    def out_act(self, t_curr):
        self.served += 1

    def print_info(self):
        print(
            f"Element = {self.name} t_next = {self.t_state} queue: {self.queue} state = {self.state}"
        )

    def print_statistic(self, time_modeling):
        print(f"Element = {self.name} served = {self.served} failure = {self.failure}")

    def print_result(self):
        print(f"{self.name} served = {self.served}")

    def do_statistics(self, delta):
        pass

    def set_next_elements(self, next_elements, probabilities=None, priorities=None, blocked=None):
        self.next_elements = next_elements
        self.probabilities = probabilities
        self.blocked = blocked
        self.priorities = priorities

    def get_next(self):
        if self.probabilities:
            while True:
                n = random.random()
                r = 0
                for i, p in enumerate(self.probabilities):
                    r += p
                    if n < r and (self.blocked is None or not self.blocked[i]):
                        return self.next_elements[i]

        if self.priorities:
            if self.blocked is not None:
                elements = []
                for i, _ in enumerate(self.next_elements):
                    if not self.blocked[i]:
                        elements.append((self.next_elements[i], self.priorities[i]))
            else:
                elements = list(zip(self.next_elements, self.priorities))
            random.shuffle(elements)
            max_prior_el = elements[0]
            for el in elements[1:]:
                if el[1] > max_prior_el[1]:
                    max_prior_el = el
            return max_prior_el[0]

        if self.blocked is not None:
            elements = random.choice(self.next_elements)
            for i, _ in self.blocked:
                if self.blocked[i]:
                    del elements[i]
            return random.choice(self.next_elements)
        return random.choice(self.next_elements)

    def get_delay(self):
        return np.random.exponential(self.delay)
