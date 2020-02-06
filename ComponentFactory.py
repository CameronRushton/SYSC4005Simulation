from Type import Type
from Component import Component
# We don't really need a component factory because it's so simple,
# but it sets us up nicely if we change how we create these.


def create_component_one():
    return Component(Type.ONE)


def create_component_two():
    return Component(Type.TWO)


def create_component_three():
    return Component(Type.THREE)
