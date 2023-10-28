import random

from element import Element


class ElementCreate(Element):
    def out_act(self, t_curr):
        super().out_act(t_curr)
        delay = self.get_delay()
        self.total_work_time += delay
        self.t_state = t_curr + delay
        n = (random.choices([1, 2, 3], weights=[0.5, 0.1, 0.4])[0], t_curr, False)
        self.get_next().in_act(t_curr, n)

    def do_statistics(self, delta):
        self.mean_queue = self.mean_queue + len(self.queue) * delta
