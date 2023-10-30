from element_process import ElementProcess


class Model:
    def __init__(self, elements):
        self.t_next = 0
        self.t_curr = self.t_next
        self.elements = elements
        self.patients_count = 0
        self.patients_duration_sum = 0

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
                    patient_times = element.out_act(self.t_curr)
                    if patient_times is not None:
                        self.patients_count += 1
                        self.patients_duration_sum += patient_times[1] - patient_times[0]
            self.print_info()
        self.print_result(time_modeling)
        print("patients in hospital mean time = ", self.patients_duration_sum / self.patients_count)

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
                # print("failure probability = ", e.failure / (e.served + e.failure))
                print("load time = ", e.total_work_time / time_modeling)

                if e.name == "Laboratory":
                    print("MEAN INTERVAL TO LABORATORY: ",
                          e.total_lab_interval / e.total_in_lab)
                    print(e.total_lab_interval)
                    print(e.total_in_lab)
            print()
