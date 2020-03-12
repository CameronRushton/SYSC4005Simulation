import time
from Type import Type
import numpy as np
from threading import Lock
import logging


class Monitor:
    __instance = None
    __lock = Lock()
    __reset = False
    @staticmethod
    def get_instance():
        if not Monitor.__instance:
            # Implementation of a double-checked lock making this method thread safe
            with Monitor.__lock:
                if not Monitor.__instance:
                    Monitor.__instance = Monitor()
        return Monitor.__instance

    def __init__(self):
        if Monitor.__instance is not None and Monitor.__reset is True:
            print("Monitor attempted instantiation when instance already created. Someone might have a bad copy!")
        else:
            self.logger = logging.getLogger(__name__)

            self.factory_start_time = 0
            self.factory_end_time = 0
            # Tells the threads to run or not
            self.run_simulation = True

            # TODO: don't need this here anymore
            self.model_variables = {
                "sim_speed_factor": 1000
            }

            # The starting time is takes for an inspector to place a component in a buffer
            self.inspector_component_start_service_times = {  # TODO: Ready to be implemented in inspector
                Type.ONE: [],
                Type.TWO: [],
                Type.THREE: []
            }
            # The time is takes for an inspector to place a component in a buffer
            self.inspector_component_service_times = {  # TODO: Ready to be implemented in inspector
                Type.ONE: [],
                Type.TWO: [],
                Type.THREE: []
            }

            # The starting time it takes for a workstation to look at it's buffers, empty them, and create a product
            self.workstation_start_service_times = {  # TODO: Ready to be implemented in workstation
                Type.ONE: [],
                Type.TWO: [],
                Type.THREE: [],
            }
            # The time it takes for a workstation to look at it's buffers, empty them, and create a product
            self.workstation_service_times = {  # TODO: Ready to be implemented in workstation
                Type.ONE: [],
                Type.TWO: [],
                Type.THREE: [],
            }

            # The time a workstation starts idling TODO: Ready to be implemented in workstation
            self.workstation_start_idle_times = {
                Type.ONE: [],
                Type.TWO: [],
                Type.THREE: [],
            }
            # The time a workstation remains idling when there is nothing for it to do (one or more buffers are empty)
            self.workstation_idle_times = {  # TODO: Ready to be implemented in workstation
                Type.ONE: [],
                Type.TWO: [],
                Type.THREE: [],
            }

            # Component block times are a better metric to find because if we did inspector block times, we wouldn't
            # have as much information as looking at which components were blocked.
            # The time inspector/component started to be blocked - This is expected to be nearly always empty because
            # we pop() values out to calculate the blocked time
            self.inspector_blocked_start_times = {
                Type.ONE: [],
                Type.TWO: [],
                Type.THREE: []
            }
            self.component_block_times = {  # The total times a component spent blocked each time it was blocked
                Type.ONE: [],
                Type.TWO: [],
                Type.THREE: []
            }

            self.products_made = {
                Type.ONE: 0,
                Type.TWO: 0,
                Type.THREE: 0,
            }
            Monitor.__instance = self

    def inspector_start_blocked(self, my_component_type):
        self.inspector_blocked_start_times[my_component_type].append(time.time())

    def inspector_end_blocked(self, my_component_type):
        self.component_block_times[my_component_type].append(
            time.time() - self.inspector_blocked_start_times[my_component_type].pop()
        )

    # TODO: since we sample the service time, we know what it's going to be so there's no need to calculate it
    def inspector_start_service_time(self, my_component_type):
        self.inspector_component_start_service_times[my_component_type].append(time.time())

    def inspector_end_service_time(self, my_component_type):
        self.inspector_component_service_times[my_component_type].append(
            time.time() - self.inspector_component_start_service_times[my_component_type].pop()
        )

    def workstation_start_idle(self, my_workstation_type):
        self.workstation_start_idle_times[my_workstation_type].append(time.time())

    def workstation_end_idle(self, my_workstation_type):
        self.workstation_idle_times[my_workstation_type].append(
            time.time() - self.workstation_start_idle_times[my_workstation_type].pop()
        )

    # TODO: since we sample the service time, we know what it's going to be so there's no need to calculate it
    def workstation_start_service_time(self, my_workstation_type):
        self.workstation_start_service_times[my_workstation_type].append(time.time())

    def workstation_end_service_time(self, my_workstation_type):
        self.workstation_service_times[my_workstation_type].append(
            time.time() - self.workstation_start_service_times[my_workstation_type].pop()
        )

    def add_product(self, my_product_type):
        self.products_made[my_product_type] += 1

    def sample_service_time(self, mean):
        return self.convert_st_mins_to_sim_speed(np.random.exponential(mean, 1)[0])

    def convert_st_mins_to_sim_speed(self, minutes):
        return minutes * 60 / self.model_variables["sim_speed_factor"]

    def end_simulation(self):
        self.run_simulation = False
        # If we were blocked when we were told to finish, calculate the blocked time
        for component_type in Type:
            # We can assume there is only one value in blocked start times
            if len(self.inspector_blocked_start_times[component_type]) > 0:
                self.inspector_end_blocked(component_type)
        self.factory_end_time = time.time()

    def reset(self):
        __reset = True
        self.__instance = Monitor()
