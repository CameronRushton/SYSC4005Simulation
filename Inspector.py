import random
import time
from threading import Thread
import logging
from Component import Component


class Inspector(Thread):
    # Inspector doesn't really need to know about workstations, but it makes some sense if they do
    def __init__(self, known_workstations, seed, my_types):
        super().__init__()
        self.daemon = True
        self.types = my_types
        self.seed = seed
        self.workstations = known_workstations
        self.is_working = True
        self.component = None
        self.logger = logging.getLogger(__name__)

    def run(self):
        while True:
            time.sleep(1)
            if self.is_working:
                self.component = self._grab_component()
            chosen_workstation, chosen_buffer = self._select_buffer(self.component.type)
            if chosen_workstation:
                if not self.is_working:
                    self._toggle_is_working()
                chosen_buffer.add(self.component)
                self.logger.info("Inspector of types %s added to buffer %s in workstation %s", self.types, chosen_buffer.type, chosen_workstation.type)
            elif self.is_working:
                self._toggle_is_working()

    def _select_buffer(self, component_type):
        best_buffer = None
        best_workstation = None
        for workstation in self.workstations:
            for buffer in workstation.buffers:
                if buffer.type == component_type and not buffer.full():  # buffer.full() is not reliable (See docs).
                    best_buffer = buffer
                    best_workstation = workstation
                    if buffer.qsize() < best_buffer.qsize():
                        best_buffer = buffer
                        best_workstation = workstation
        return best_workstation, best_buffer

    def _toggle_is_working(self):
        self.is_working = not self.is_working
        self.logger.info("Inspector of types %s is %s", self.types, "WORKING" if self.is_working else "BLOCKED")

    def _grab_component(self):
        return Component(random.choice(self.types))

