import time


class Component:
    def __init__(self, my_type):
        self.type = my_type
        self.queue_arrival_time = 0
        self.creation_time = time.time()
        self.destruction_time = 0

    def get_time_in_sys(self):
        if self.destruction_time and self.creation_time:
            result = self.destruction_time - self.creation_time
            if result > 0:
                return result
