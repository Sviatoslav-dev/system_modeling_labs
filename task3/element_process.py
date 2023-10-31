from element import Element
from task3.Patient import Patient


class ElementProcess(Element):
    def __init__(self, delay, name, max_queue, count_of_workers=1,
                 type_depends_delay=False, distribution=None):
        super().__init__(delay, name, max_queue, type_depends_delay, distribution=distribution)
        self.t_state = float("inf")
        self.worker_states = [0 for _ in range(count_of_workers)]
        self.workers_t_next = [float("inf") for _ in range(count_of_workers)]

        self.last_in_lab = None
        self.total_lab_interval = 0
        self.total_in_lab = 0

    def in_act(self, t_curr, patient=1):
        if self.name == "Laboratory":
            if self.last_in_lab is None:
                self.last_in_lab = t_curr
            else:
                self.total_in_lab += 1
                self.total_lab_interval = t_curr - self.last_in_lab
                self.last_in_lab = t_curr

        try:
            worker = self.worker_states.index(0)
        except ValueError:
            worker = None

        if worker is not None:
            self.worker_states[worker] = patient
            delay = self.get_delay(patient.type)
            self.workers_t_next[worker] = t_curr + delay
            self.t_state = min(self.workers_t_next)
            if 0 not in self.worker_states:
                self.is_blocked = True
        else:
            if len(self.queue) < self.max_queue:
                # self.queue.append(obj)
                if self.name == "Doctors on duty" and patient.was_in_lab:
                    self.queue.insert(0, patient)
                else:
                    self.queue.append(patient)
            else:
                self.failure += 1

    def out_act(self, t_curr):
        super().out_act(t_curr)
        worker_index = self.workers_t_next.index(t_curr)
        print("PROCESSED: ", self.worker_states[worker_index])
        processed_patient = self.worker_states[worker_index]
        self.worker_states[worker_index] = 0
        self.workers_t_next[worker_index] = float("inf")
        self.t_state = min(self.workers_t_next)
        if len(self.queue) > 0:
            patient = self.queue.pop(0)
            self.worker_states[worker_index] = patient
            delay = self.get_delay(patient.type)
            self.total_work_time += delay
            self.workers_t_next[worker_index] = t_curr + delay
            self.t_state = min(self.workers_t_next)
        else:
            if 0 in self.worker_states:
                self.is_blocked = False
        if self.next_elements is not None:
            next_element = self.get_next(processed_patient.type)
            if next_element is not None:
                if self.name == "Road from laboratory":
                    processed_patient = Patient(1, processed_patient.arrival_time, True)
                next_element.in_act(t_curr, processed_patient)
            else:
                return processed_patient.arrival_time, t_curr
        else:
            return processed_patient.arrival_time, t_curr

    def do_statistics(self, delta):
        self.mean_queue += len(self.queue) * delta

    def print_result(self):
        super().print_result()
        print(f"failure = {self.failure}")
