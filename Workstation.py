import logging
import queue
import time
from threading import Thread

from Product import Product


class Workstation(Thread):
    def __init__(self, my_type, my_buffers):
        super().__init__()
        self.daemon = True
        self.buffers = my_buffers
        self.type = my_type
        self.products_made = 0
        self.logger = logging.getLogger(__name__)

    def run(self):
        while True:
            time.sleep(1.2)
            if self._has_all_components():
                self._make_product()
                self.logger.info("Made product %s", self.type.name)

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
