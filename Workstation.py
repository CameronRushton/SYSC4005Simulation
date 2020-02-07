import atexit
import logging
import queue
import threading
import time
from threading import Thread
from Monitor import Monitor
from Product import Product


class Workstation(Thread):
    def __init__(self, my_type, my_buffers):
        super().__init__()
        self.daemon = True
        self.buffers = my_buffers
        self.type = my_type
        self.products_made = 0
        self.logger = logging.getLogger(__name__)
        self.monitor = Monitor.get_instance()
        self.service_time = self.monitor.model_variables["workstation_service_times"][my_type]
        self.logger.info("Initialized monitor %s in workstation as monitor ", self.monitor)

    def run(self):
        self.logger.info("Started workstation thread %s", self.type.name)
        @atexit.register
        def commit_seppuku():
            self.logger.info("'Cleanly' killed workstation sub-thread of type: %s [THREAD: %s]",
                             self.type, threading.currentThread().ident)
        while True:
            # This block needs to match the desired service time - code after is considered negligible
            time.sleep(self.monitor.model_variables["workstation_service_times"][self.type])
            if self._has_all_components():
                self._make_product()
                self.logger.info("Made product %s", self.type.name)
                self.monitor.add_product(self.type)

    def _has_all_components(self):
        for buffer in self.buffers:
            if buffer.empty():  # This isn't reliable (See docs)
                return False
        return True

    def _make_product(self):
        for buffer in self.buffers:
            buffer.pop()
        self.products_made += 1
        return Product(self.type)


class Buffer(queue.Queue):
    def __init__(self, buffer_type):
        super().__init__(maxsize=2)
        self.type = buffer_type

    def add(self, component):
        if component.type == self.type:
            self.put(component)

    def pop(self):
        self.get()  # We dont need to return the value here
