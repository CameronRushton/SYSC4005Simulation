import time


# TODO: Implement me. Perhaps we can either make this a thread and have it pull info from everything else or have
#  everything else push to here.
class Monitor:
    __instance = None

    @staticmethod
    def get_instance():
        if Monitor.__instance is None:
            Monitor()
        return Monitor.__instance

    def __init__(self):
        if Monitor.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.i1 = None
            self.i2 = None
            self.w1_b1 = None
            self.w2_b1 = None
            self.w2_b2 = None
            self.w3_b1 = None
            self.w3_b2 = None
            self.i1_blocked_time = 0
            self.i1_start_time = 0
            self.i2_blocked_time = 0
            self.i2_start_time = 0
            self.p1_made = 0
            self.p2_made = 0
            self.p3_made = 0
            Monitor.__instance = self

    def print_status(self):
        print("Inspector One has component type: ", self.i1.component.type.name, " \n",
              "Inspector Two has component type: ", self.i2.component.type.name, " \n",
              "Workstation 1 - Buffer ", self.w1_b1.type.name, " size: ", self.w1_b1.qsize(), " \n",
              "Workstation 2 - Buffer ", self.w2_b1.type.name, " size: ", self.w2_b1.qsize(), " \n",
              "Workstation 2 - Buffer ", self.w2_b2.type.name, " size: ", self.w2_b2.qsize(), " \n",
              "Workstation 3 - Buffer ", self.w3_b1.type.name, " size: ", self.w3_b1.qsize(), " \n",
              "Workstation 3 - Buffer ", self.w3_b2.type.name, " size: ", self.w3_b2.qsize(), " \n",
              "Product 1s made: ", self.p1_made, " \n",
              "Product 2s made: ", self.p2_made, " \n",
              "Product 3s made: ", self.p3_made, " \n")

    def inspector_one_start_blocked(self):
        self.i1_start_time = time.time()

    def inspector_one_end_blocked(self):
        self.i1_blocked_time += time.time() - self.i1_start_time

    def inspector_two_start_blocked(self):
        self.i2_start_time = time.time()

    def inspector_two_end_blocked(self):
        self.i2_blocked_time += time.time() - self.i2_start_time
