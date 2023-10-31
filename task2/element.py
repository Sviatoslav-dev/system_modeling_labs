import copy
import random
import numpy as np


class Element:
    def __init__(self, delay, name, max_queue=0, distribution=None):
        self.mean_queue = 0
        self.t_state = 0
        self.delay = delay
        self.total_work_time = 0

        self.state = 0
        self.queue = []
        self.max_queue = max_queue
        self.failure = 0
        self.served = 0

        self.next_elements = None
        self.name = name

        self.is_blocked = False

        self.probabilities = None
        self.blocked = None
        self.priorities = None

        self.distribution = distribution if distribution is not None else np.random.exponential

    def in_act(self, t_curr, start_time):
        pass

    def out_act(self, t_curr):
        self.served += 1

    def print_info(self):
        print(
            f"Element = {self.name} t_next = {self.t_state} queue: {len(self.queue)} state = {self.state}"
        )

    def print_statistic(self, time_modeling):
        print(f"Element = {self.name} served = {self.served} failure = {self.failure}")

    def print_result(self):
        print(f"{self.name} served = {self.served}")

    def do_statistics(self, delta):
        pass

    def set_next_elements(self, next_elements, probabilities=None, blocked=None, priorities=None):
        self.next_elements = next_elements
        self.probabilities = probabilities
        self.blocked = blocked
        self.priorities = priorities

    def get_next(self):
        if self.priorities:
            priorities = copy.copy(self.priorities)
            next_elements = copy.copy(self.next_elements)
            best = None
            while priorities:
                max_priority = max(priorities)
                max_priority_index = priorities.index(max_priority)

                if best is None:
                    best = next_elements[max_priority_index]

                    if best.is_blocked:
                        return best
                elif len(next_elements[max_priority_index].queue) < len(best.queue):
                    best = next_elements[max_priority_index]

                del priorities[max_priority_index]
                del next_elements[max_priority_index]

        if self.probabilities:
            n = random.random()
            r = 0
            for i, p in enumerate(self.probabilities):
                r += p
                if n < r:
                    return self.next_elements[i]
        return random.choice(self.next_elements)

    def get_delay(self):
        if isinstance(self.delay, tuple):
            return self.distribution(*self.delay)
        else:
            return self.distribution(self.delay)
