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

    def set_next_elements(self, next_elements):
        self.next_elements = next_elements

    def get_next(self):
        return random.choice(self.next_elements)

    def get_delay(self):
        return np.random.exponential(self.delay)
