from Component import Component
# We don't really need a component factory because it's so simple,
# but it sets us up nicely if we change how we create these.


def create_component(my_type):
    return Component(my_type)

