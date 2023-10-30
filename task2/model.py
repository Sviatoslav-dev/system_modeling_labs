from element_process import ElementProcess


class Model:
    def __init__(self, elements):
        self.t_next = 0.001
        self.t_curr = self.t_next
        self.elements = elements

        self.last_departure_time = None
        self.total_departure_interval = 0
        self.total_departured = 0

        self.total_queue_change = 0

    def simulate(self, time_modeling):
        while self.t_curr < time_modeling:
            self.t_next = float("inf")
            next_element = None

            for element in self.elements:
                if element.t_state < self.t_next:
                    self.t_next = element.t_state
                    next_element = element
            print(f"\nIt's time for element in {next_element.name}, time = {self.t_next}")
            for e in self.elements:
                e.do_statistics(self.t_next - self.t_curr)
            self.t_curr = self.t_next

            for element in self.elements:
                if element.t_state == self.t_curr:
                    last_departure_time = element.out_act(self.t_curr)
                    if last_departure_time is not None:
                        if self.last_departure_time is not None:
                            self.total_departure_interval += last_departure_time - self.last_departure_time
                            self.total_departured += 1
                        self.last_departure_time = last_departure_time
                    self.change_queue()  # only task 2
            self.print_info()
        self.print_result(time_modeling)

    def change_queue(self):
        if len(self.elements[1].queue) - len(self.elements[2].queue) >= 2:
            start_time = self.elements[1].queue.pop()
            self.elements[2].queue.append(start_time)
            self.total_queue_change += 1

        if len(self.elements[2].queue) - len(self.elements[1].queue) >= 2:
            start_time = self.elements[2].queue.pop()
            self.elements[1].queue.append(start_time)
            self.total_queue_change += 1

    def print_info(self):
        for element in self.elements:
            if element.state == 1:
                element.printInfo()

    def print_result(self, time_modeling):
        print("\n-------------RESULTS-------------")
        mean_clients = 0
        total_time_in_system = 0
        total_served = 0
        for e in self.elements:
            e.print_result()
            if isinstance(e, ElementProcess):
                print("mean length of queue = ", e.mean_queue / self.t_curr)
                print("failure probability = ", e.failure / (e.served + e.failure))
                print("load time = ", e.total_work_time / time_modeling)
                mean_clients += e.mean_clients / self.t_curr
                total_time_in_system += e.total_time_in_system
                total_served += e.served
            print()
        print()
        print(f"mean count of clients in bank = {mean_clients}")
        print(f"MEAN DEPARTURE TIME = {self.total_departure_interval / self.total_departured}")
        print(f"mean client time in bank = {total_time_in_system / total_served}")
        print(f"count of queue change = {self.total_queue_change}")
