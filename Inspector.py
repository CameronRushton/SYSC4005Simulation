import random
import threading
import time
from threading import Thread
import atexit
import logging

from Type import Type
from Monitor import Monitor
from Component import Component


class Inspector(Thread):
    # Inspector doesn't really need to know about workstations, but it makes some sense if they do
    def __init__(self, known_workstations, seed, my_types, mean_st_components, st_file_names, round_robin, *args, **kwargs):
        super(Inspector, self).__init__(*args, **kwargs)
        self.types = my_types
        random.seed(seed)
        self.workstations = known_workstations
        self.round_robin_index = 0
        self.mean_st_components = mean_st_components
        self.round_robin = round_robin
        self.is_working = True
        self.component = None
        self.logger = logging.getLogger(__name__)
        self.monitor = Monitor.get_instance()
        self.service_times = []
        if self.monitor.use_common_service_times:
            self.common_service_times = {}
            self.st_counters = {}
            for typ in my_types:
                self.common_service_times[typ] = open(st_file_names[typ]).read().splitlines()
                self.st_counters[typ] = 0
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
                if self.monitor.use_common_service_times:
                    if self.st_counters[self.component.type] >= len(self.common_service_times[self.component.type]):
                        self.st_counters[self.component.type] = 0
                        self.logger.warning("Inspector of types %s went back to the beginning of service time list "
                                            "for %s (ran out of samples).", self.component.type, self.types)
                    st = float(self.common_service_times[self.component.type][self.st_counters[self.component.type]])
                    self.st_counters[self.component.type] += 1
                else:
                    st = self.monitor.sample_service_time(self.mean_st_components[self.component.type])
                self.service_times.append(st)
                time.sleep(st)

            if self.round_robin:
                chosen_workstation, chosen_buffer = self._select_buffer_round_robin(self.component.type)
            else:
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

    def _select_buffer_round_robin(self, component_type):
        if component_type == Type.TWO or component_type == Type.THREE:
            for workstation in self.workstations:
                for buffer in workstation.buffers:
                    if buffer.type == component_type and not buffer.full():
                        return workstation, buffer
            return None, None
        else:
            check = 0
            while check < 3:  # check if every workstation is full
                round_robin_workstation = self.workstations[self.round_robin_index]
                for buffer in round_robin_workstation.buffers:
                    if buffer.type == component_type and not buffer.full():
                        self._next_index()
                        return round_robin_workstation, buffer
                # no empty buffer of correct type at workstation
                self._next_index()
                check += 1
            return None, None

    def _next_index(self):
        if self.round_robin_index < (len(self.workstations) - 1):
            self.round_robin_index += 1
        else:
            self.round_robin_index = 0

    def _toggle_is_working(self):
        self.is_working = not self.is_working
        self.logger.info("Inspector of types %s is %s", self.types, "WORKING" if self.is_working else "BLOCKED")

    def _grab_component(self):
        self.monitor.total_components += 1
        self.monitor.sample_components_in_sys()
        component = Component(random.choice(self.types))
        self.monitor.all_components_made.append(component)
        return component
