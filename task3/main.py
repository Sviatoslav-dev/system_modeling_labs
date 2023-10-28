from element_create import ElementCreate
from element_process import ElementProcess
from model import Model

create = ElementCreate(delay=15, name="Create")
doctors_on_duty = ElementProcess(delay=1, name="Doctors on duty",
                                 max_queue=10000, count_of_workers=2, type_depends_delay=True)
doctors_on_duty.type_delays = {
    1: 15,
    2: 40,
    3: 30,
}
accompanying_to_chamber = ElementProcess(delay=5, name="Accompanying to chamber",
                                         max_queue=100, count_of_workers=3)

road_to_lab = ElementProcess(delay=3, name="Road to laboratory",
                             max_queue=100, count_of_workers=100)

lab_registration = ElementProcess(delay=4.5, name="Registration to laboratory",
                                  max_queue=100, count_of_workers=1)

lab = ElementProcess(delay=4, name="Laboratory",
                     max_queue=100, count_of_workers=2)


road_from_lab = ElementProcess(delay=3, name="Road from laboratory",
                               max_queue=100, count_of_workers=100)

create.set_next_elements([doctors_on_duty])
doctors_on_duty.set_next_elements({
    1: accompanying_to_chamber,
    2: road_to_lab,
    3: road_to_lab,
})
road_to_lab.set_next_elements([lab_registration])
lab_registration.set_next_elements([lab])
lab.set_next_elements({
    2: road_from_lab,
    3: None
})
road_from_lab.set_next_elements([doctors_on_duty])
model = Model([
    create,
    doctors_on_duty,
    accompanying_to_chamber,
    road_to_lab,
    lab_registration,
    lab,
    road_from_lab,
])
model.simulate(10000)
