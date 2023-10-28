from element_process import ElementProcess


class Model:
    def __init__(self, elements):
        self.t_next = 0
        self.t_curr = self.t_next
        self.elements = elements

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
                    element.out_act(self.t_curr)
                    self.change_queue()  # only task 2
            self.print_info()
        self.print_result(time_modeling)

    def change_queue(self):
        if self.elements[1].queue - self.elements[2].queue >= 2:
            self.elements[1].queue -= 1
            self.elements[2].queue += 1

        if self.elements[2].queue - self.elements[1].queue >= 2:
            self.elements[2].queue -= 1
            self.elements[1].queue += 1

    def print_info(self):
        for element in self.elements:
            if element.state == 1:
                element.printInfo()

    def print_result(self, time_modeling):
        print("\n-------------RESULTS-------------")
        for e in self.elements:
            e.print_result()
            if isinstance(e, ElementProcess):
                print("mean length of queue = ", e.mean_queue / self.t_curr)
                print("failure probability = ", e.failure / (e.served + e.failure))
                print("load time = ", e.total_work_time / time_modeling)
            print()
