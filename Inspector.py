import random
import threading
import time
from threading import Thread
import atexit
import logging
from Monitor import Monitor
from Component import Component


class Inspector(Thread):
    # Inspector doesn't really need to know about workstations, but it makes some sense if they do
    def __init__(self, known_workstations, seed, my_types, mean_st_components, *args, **kwargs):
        super(Inspector, self).__init__(*args, **kwargs)
        self.types = my_types
        random.seed(seed)
        self.workstations = known_workstations
        self.mean_st_components = mean_st_components
        self.is_working = True
        self.component = None
        self.logger = logging.getLogger(__name__)
        self.monitor = Monitor.get_instance()
        self.logger.info("Initialized monitor %s in inspector.", self.monitor)

    def run(self):
        self.logger.info("Started inspector thread of types %s", self.types)
        @atexit.register
        def commit_seppuku():
            self.logger.info("Cleanly killed inspector sub-thread of type: %s [THREAD: %s]",
                             self.types, threading.currentThread().ident)
        while self.monitor.run_simulation:
            if self.is_working:
                self.component = self._grab_component()
                # This block needs to match the desired service time - code after is considered negligible
                time.sleep(self.monitor.sample_service_time(self.mean_st_components[self.component.type]))
            chosen_workstation, chosen_buffer = self._select_buffer(self.component.type)
            if chosen_workstation:  # If I found a buffer not full for my component
                if not self.is_working:  # If I'm currently blocked
                    self._toggle_is_working()  # Set self to unblocked/working
                    self.monitor.inspector_end_blocked(self.component.type)  # Notify monitor
                chosen_buffer.add(self.component)
                self.logger.info("Inspector of types %s added to buffer %s in workstation %s", self.types,
                                 chosen_buffer.type, chosen_workstation.type)
            elif self.is_working:  # All buffers are full and if I'm not blocked
                self._toggle_is_working()  # Set self to blocked
                self.monitor.inspector_start_blocked(self.component.type)  # Notify monitor

    def _select_buffer(self, component_type):
        best_buffer = None
        best_workstation = None
        for workstation in self.workstations:
            for buffer in workstation.buffers:
                if buffer.type == component_type and not buffer.full():  # buffer.full() is not reliable (See docs).
                    if best_buffer is None:
                        best_buffer = buffer
                        best_workstation = workstation
                    if buffer.qsize() < best_buffer.qsize():  # Pick the buffer with the lowest amount of items
                        best_buffer = buffer
                        best_workstation = workstation
        return best_workstation, best_buffer

    def _toggle_is_working(self):
        self.is_working = not self.is_working
        self.logger.info("Inspector of types %s is %s", self.types, "WORKING" if self.is_working else "BLOCKED")

    def _grab_component(self):
        return Component(random.choice(self.types))
