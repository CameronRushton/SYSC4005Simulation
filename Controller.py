import ComponentFactory
from Inspector import Inspector
import WorkstationFactory
import numpy as np
import time


# This method can be moved to the Inspector, but being able to change the seed is nice outside of the Inspector context.
# If we do this, we would use the my_types parameter in Inspector to know which types we can randomly choose.
def grab_comp_for_inspector_two():
    value = np.random.normal(loc=0, scale=1, size=1)
    if value > 0:
        return ComponentFactory.create_component_two()
    else:
        return ComponentFactory.create_component_three()


def run():
    # Initialization
    np.random.seed(1)
    workstations = WorkstationFactory.create_all_workstations()

    # We can make an inspector factory, but we should decide if we obtain all workstations here or have the inspector
    # factory use the workstation factory to create the inspectors. This is probably OK since any workstation can be
    # given to any inspector.
    inspector_one = Inspector(known_workstations=workstations)
    inspector_two = Inspector(known_workstations=workstations)

    component_for_i2 = None
    for iteration in range(1, 6):
        component_for_i1 = ComponentFactory.create_component_one()
        if inspector_two.is_working:
            component_for_i2 = grab_comp_for_inspector_two()
        result = inspector_one.place_component(component_for_i1)
        print("Inspector one made product ", result.type.name if result else "None")
        time.sleep(1)
        print("Inspector two has component type ", component_for_i2.type.name)
        result = inspector_two.place_component(component_for_i2)
        print("Inspector two made product ", result.type.name if result else "None")
        time.sleep(3)


if __name__ == "__main__":
    run()
