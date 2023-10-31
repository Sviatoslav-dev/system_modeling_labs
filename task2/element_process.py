from element import Element


class ElementProcess(Element):
    def __init__(self, delay, name, max_queue, count_of_workers=1, distribution=None):
        super().__init__(delay, name, max_queue, distribution=distribution)
        self.t_state = float("inf")
        self.worker_states = [0 for _ in range(count_of_workers)]
        self.workers_t_next = [float("inf") for _ in range(count_of_workers)]

        self.block_start = 0
        self.mean_clients = 0  # statistic 2

        self.total_time_in_system = 0

    def in_act(self, t_curr, start_time, delay=None):
        try:
            worker = self.worker_states.index(0)
        except ValueError:
            worker = None

        if worker is not None:
            self.worker_states[worker] = start_time
            delay = delay if delay else self.get_delay()
            self.workers_t_next[worker] = t_curr + delay
            self.t_state = min(self.workers_t_next)
            if 0 not in self.worker_states:
                self.is_blocked = True
                self.block_start = t_curr
        else:
            if len(self.queue) < self.max_queue:
                self.queue.append(start_time)
            else:
                self.failure += 1

    def out_act(self, t_curr):
        super().out_act(t_curr)
        worker_index = self.workers_t_next.index(t_curr)
        start_time = self.worker_states[worker_index]
        self.worker_states[worker_index] = 0
        self.workers_t_next[worker_index] = float("inf")
        self.t_state = min(self.workers_t_next)
        if len(self.queue) > 0:
            start_time = self.queue.pop()
            self.worker_states[worker_index] = start_time
            delay = self.get_delay()
            self.total_work_time += delay
            self.workers_t_next[worker_index] = t_curr + delay
            self.t_state = min(self.workers_t_next)
        else:
            if 0 in self.worker_states:
                self.is_blocked = False
        if self.next_elements is not None:
            self.get_next().in_act(t_curr, start_time)
        else:
            print("sys_dor: ", start_time, t_curr, t_curr - start_time)
            self.total_time_in_system += t_curr - start_time
            return t_curr

    def do_statistics(self, delta):
        self.mean_queue += len(self.queue) * delta
        self.mean_clients += (len(self.queue) + int(self.is_blocked)) * delta

    def print_result(self):
        super().print_result()
        print(f"failure = {self.failure}")
