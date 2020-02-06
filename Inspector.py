class Inspector:
    # my_types isn't strictly necessary - we just use it to make sure that we give the inspector the right types
    def __init__(self, known_workstations, my_types=None):
        self.types = my_types
        self.workstations = known_workstations
        self.is_working = True

    def place_component(self, component):
        if self.types and not self.types.contains(component.type):
            print("Inspector of types ", self.types, " given incorrect component of type ", component.type.name)
            return

        chosen_workstation, chosen_buffer = self._select_buffer(component)
        if chosen_workstation:
            if not self.is_working:
                self._toggle_is_working()
            return chosen_workstation.add_component(component, chosen_buffer)
        elif self.is_working:
            self._toggle_is_working()

    def _select_buffer(self, component):
        best_buffer = None
        best_workstation = None
        for workstation in self.workstations:
            for buffer in workstation.buffers:
                if buffer.type == component.type and buffer.has_room():
                    best_buffer = buffer
                    best_workstation = workstation
                    if len(buffer.components) < len(best_buffer.components):
                        best_buffer = buffer
                        best_workstation = workstation
        return best_workstation, best_buffer

    def _toggle_is_working(self):
        self.is_working = not self.is_working
        print("Inspector of types ", self.types, " is ", "BLOCKED" if self.is_working else "WORKING")
