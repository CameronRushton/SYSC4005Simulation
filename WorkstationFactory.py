from Type import Type
from Workstation import Workstation, Buffer


def create_workstation_one():
    return Workstation(my_type=Type.ONE, my_buffers=[Buffer(Type.ONE)])


def create_workstation_two():
    return Workstation(my_type=Type.TWO, my_buffers=[Buffer(Type.ONE), Buffer(Type.TWO)])


def create_workstation_three():
    return Workstation(my_type=Type.THREE, my_buffers=[Buffer(Type.ONE), Buffer(Type.THREE)])


def create_all_workstations():
    return [create_workstation_one(),
            create_workstation_two(),
            create_workstation_three()]
