import atexit
import logging
import threading
from threading import Thread
from Monitor import Monitor
import time
from Type import Type


class Sampler(Thread):
    def __init__(self, known_workstations, known_inspectors, *args, **kwargs):
        super(Sampler, self).__init__(*args, **kwargs)
        self.workstations = known_workstations
        self.inspectors = known_inspectors
        self.logger = logging.getLogger(__name__)
        self.monitor = Monitor.get_instance()
        self.logger.info("Initialized monitor %s in sampler.", self.monitor)
        self.num_components_in_queue_samples = {
            Type.ONE: {  # Workstation type
                Type.ONE: []  # Queue / component type
            },
            Type.TWO: {
                Type.ONE: [],
                Type.TWO: []
            },
            Type.THREE: {
                Type.ONE: [],
                Type.THREE: []
            },
        }

    def run(self):
        self.logger.info("Started queue sampler thread.")
        @atexit.register
        def commit_seppuku():
            self.logger.info("Cleanly killed queue sampler sub-thread [THREAD: %s]", threading.currentThread().ident)
        while self.monitor.run_simulation:
            if time.time() > self.monitor.init_bias:
                time.sleep(0.1)  # Take a sample of the queues every x seconds
                self._sample_queues_and_workstations()

    # TODO: The original idea here is to take responsibility of reporting queue size off of a component and put it on something like this
    # sampler that has it's own thread. This works and is accurate enough, but it would be more accurate if we had the component
    # report it's state every time the state changed.
    def _sample_queues_and_workstations(self):
        for workstation in self.workstations:
            for buffer in workstation.buffers:
                self.num_components_in_queue_samples[workstation.type][buffer.type].append(buffer.qsize())
