from Type import Type
from Workstation import Workstation, Buffer


def create_workstation_one(work_times):
    return Workstation(my_type=Type.ONE, my_buffers=[Buffer(Type.ONE)], my_times=work_times)


def create_workstation_two(work_times):
    return Workstation(my_type=Type.TWO, my_buffers=[Buffer(Type.ONE), Buffer(Type.TWO)], my_times=work_times)


def create_workstation_three(work_times):
    return Workstation(my_type=Type.THREE, my_buffers=[Buffer(Type.ONE), Buffer(Type.THREE)], my_times=work_times)


def create_all_workstations(times_work_one, times_work_two, times_work_three):
    return [create_workstation_one(times_work_one),
            create_workstation_two(times_work_two),
            create_workstation_three(times_work_three)]
