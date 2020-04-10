import atexit
import logging
import queue
import threading
import time
from threading import Thread
from Monitor import Monitor


class Workstation(Thread):
    def __init__(self, my_type, my_buffers, mean_st, *args, **kwargs):
        super(Workstation, self).__init__(*args, **kwargs)
        self.buffers = my_buffers
        self.type = my_type
        self.mean_st = mean_st
        self.isMakingProduct = False
        self.logger = logging.getLogger(__name__)
        self.monitor = Monitor.get_instance()
        self.logger.info("Initialized monitor %s in workstation.", self.monitor)
        self.service_times = []

    def run(self):
        self.logger.info("Started workstation thread %s", self.type.name)
        @atexit.register
        def commit_seppuku():
            self.logger.info("Cleanly killed workstation sub-thread of type: %s [THREAD: %s]",
                             self.type, threading.currentThread().ident)
        while self.monitor.run_simulation:
            if self._has_all_components():
                self._make_product()
                self.logger.info("Made product %s", self.type.name)
                self.isMakingProduct = False
                self.monitor.add_product(self.type)
        # Simulation has stopped
        self._empty_buffers()

    def _has_all_components(self):
        for buffer in self.buffers:
            if buffer.empty():  # This isn't reliable (See docs)
                return False
        return True

    def _make_product(self):
        self.logger.info("Making product %s", self.type.name)
        self.isMakingProduct = True
        components = []
        for buffer in self.buffers:
            comp = buffer.pop()
            components.append(comp)
            self.monitor.add_component_queue_time(comp.queue_arrival_time, self.type, buffer.type)
        # This block needs to match the desired service time - code before is considered negligible
        # This means that the workstation can be assembling a product while its buffer(s) is/are full, meaning we can
        # ...potentially make 3 products in a row without filling the queue in that time. Finish the one it currently
        # ...has and then pull the next two from the queue.
        st = self.monitor.sample_service_time(self.mean_st)
        self.service_times.append(st)
        time.sleep(st)
        for component in components:
            component.destruction_time = time.time()

    def _empty_buffers(self):
        for buffer in self.buffers:
            while not buffer.empty():
                self.monitor.add_component_queue_time(buffer.pop().queue_arrival_time, self.type, buffer.type)


class Buffer(queue.Queue):
    def __init__(self, buffer_type):
        super().__init__(maxsize=2)
        self.type = buffer_type
        self.sizes = [0]
        self.zero = time.time()  # time.time() is our zero
        self.size_timestamps = [0.0]

    def add(self, component):
        if component.type == self.type:
            self.put(component)
            self.sizes.append(self.qsize())
            self.size_timestamps.append(time.time() - self.zero)
            component.queue_arrival_time = time.time()

    def pop(self):
        value = self.get()
        self.sizes.append(self.qsize())
        self.size_timestamps.append(time.time() - self.zero)
        return value
