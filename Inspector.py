import random
import threading
from threading import Thread
from Type import Type
import atexit
import logging
import time
from Monitor import Monitor
from Component import Component


class Inspector(Thread):
    # Inspector doesn't really need to know about workstations, but it makes some sense if they do
    def __init__(self, inspector_type, known_workstations, seed, my_types, inspection_times):
        super().__init__()
        self.daemon = True
        self.types = my_types
        self.seed = seed
        self.workstations = known_workstations
        self.inspection_times = inspection_times
        self.inspector_type = inspector_type
        self.is_working = True
        self.component = None
        self.logger = logging.getLogger(__name__)
        self.monitor = Monitor.get_instance()
        self.logger.info("Initialized monitor %s in inspector as monitor ", self.monitor)
        self.first_component_counter = 0
        self.second_component_counter = 0

    def run(self):
        self.logger.info("Started inspector thread of types %s", self.types)

        @atexit.register
        def commit_seppuku():
            self.logger.info("'Cleanly' killed inspector sub-thread of type: %s [THREAD: %s]",
                             self.types, threading.currentThread().ident)

        while True:
            if self.is_working:
                self.component = self._grab_component()
            chosen_workstation, chosen_buffer = self._select_buffer(self.component.type)
            if chosen_workstation:
                if not self.is_working:
                    self._toggle_is_working()
                self._inspect_time()
                chosen_buffer.add(self.component)
                self.logger.info("Inspector %s added to buffer %s in workstation %s", self.inspector_type.value,
                                 chosen_buffer.type, chosen_workstation.type)
            elif self.is_working:
                self._toggle_is_working()

    def _select_buffer(self, component_type):
        best_buffer = None
        best_workstation = None
        for workstation in self.workstations:
            for buffer in workstation.buffers:
                if buffer.type == component_type and not buffer.full():  # buffer.full() is not reliable (See docs).
                    if best_buffer is None:
                        best_buffer = buffer
                        best_workstation = workstation
                    else:
                        if buffer.qsize() < best_buffer.qsize():
                            best_buffer = buffer
                            best_workstation = workstation
        return best_workstation, best_buffer

    def _toggle_is_working(self):
        self.is_working = not self.is_working
        self.logger.info("Inspector %s is %s", self.inspector_type.value, "WORKING" if self.is_working else "BLOCKED")

    def _grab_component(self):
        return Component(random.choice(self.types))

    def _inspect_time(self):
        inspector_three = False
        for times in self.inspection_times:
            if self.component.type == Type.ONE or self.component.type == Type.TWO:
                self.logger.info("Inspector %s is working for %s on component %s", self.inspector_type.value,
                                 times.item(self.first_component_counter), self.component.type.value)
                time.sleep(times.item(self.first_component_counter))
                self.first_component_counter += 1
                break
            else:
                if inspector_three:
                    self.logger.info("Inspector %s is working for %s on component %s", self.inspector_type.value,
                                     times.item(self.second_component_counter), self.component.type.value)
                    time.sleep(times.item(self.second_component_counter))
                    self.second_component_counter += 1
                inspector_three = True
