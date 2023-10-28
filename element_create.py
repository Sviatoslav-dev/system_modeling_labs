from element import Element


class ElementCreate(Element):
    def out_act(self, t_curr):
        super().out_act(t_curr)
        delay = self.get_delay()
        self.total_work_time += delay
        self.t_state = t_curr + delay
        self.get_next().in_act(t_curr)

    def doStatistics(self, delta):
        self.mean_queue = self.mean_queue + self.queue * delta
