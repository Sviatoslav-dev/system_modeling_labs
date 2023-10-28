from element import Element


class ElementProcess(Element):
    def __init__(self, delay, name, max_queue, count_of_workers):
        super().__init__(delay, name, max_queue)
        self.t_state = float("inf")
        self.worker_states = [0 for _ in range(count_of_workers)]
        self.workers_t_next = [float("inf") for _ in range(count_of_workers)]

    def in_act(self, t_curr):
        try:
            worker = self.worker_states.index(0)
        except ValueError:
            worker = None

        if worker is not None:
            self.worker_states[worker] = 1
            delay = self.get_delay()
            self.workers_t_next[worker] = t_curr + delay
            self.t_state = min(self.workers_t_next)
            if 0 not in self.worker_states:
                self.is_blocked = True
        else:
            if self.queue < self.max_queue:
                self.queue += 1
            else:
                self.failure += 1

    def out_act(self, t_curr):
        super().out_act(t_curr)
        worker_index = self.workers_t_next.index(t_curr)
        self.worker_states[worker_index] = 0
        self.workers_t_next[worker_index] = float("inf")
        self.t_state = min(self.workers_t_next)
        if self.queue > 0:
            self.queue -= 1
            self.worker_states[worker_index] = 1
            delay = self.get_delay()
            self.total_work_time += delay
            self.workers_t_next[worker_index] = t_curr + delay
            self.t_state = min(self.workers_t_next)
        else:
            if 0 in self.worker_states:
                self.is_blocked = False
        if self.next_elements is not None:
            self.get_next().in_act(t_curr)

    def do_statistics(self, delta):
        self.mean_queue += self.queue * delta

    def print_result(self):
        super().print_result()
        print(f"failure = {self.failure}")
