from Product import Product


class Workstation:
    def __init__(self, my_type, my_buffers):
        self.buffers = my_buffers
        self.type = my_type

    def add_component(self, component, buffer):
        buffer.add(component)
        if self._has_all_components():
            return self._make_product()

    def _has_all_components(self):
        for buffer in self.buffers:
            if buffer.is_empty():
                return False
        return True

    def _make_product(self):
        for buffer in self.buffers:
            buffer.components.pop()
        return Product(self.type)


class Buffer:
    def __init__(self, buffer_type):
        self.max_size = 2
        self.type = buffer_type
        self.components = []

    def add(self, component):
        if component.type == self.type and len(self.components) != self.max_size:
            self.components.append(component)

    def has_room(self):
        if len(self.components) == self.max_size:
            return False
        else:
            return True

    def is_empty(self):
        return len(self.components) == 0
