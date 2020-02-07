import logging
import threading
import time

from Inspector import Inspector
import WorkstationFactory

import numpy as np
from Monitor import Monitor
from Type import Type

logging.basicConfig(format="%(levelname)s: %(relativeCreated)6d %(threadName)s %(message)s",
                    level=logging.INFO, datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)
monitor = Monitor().get_instance()


# Calculate the throughput of the factory and other metrics using the monitor object
def calculate_performance():
    calc_factory_runtime = monitor.factory_start_time - monitor.factory_end_time
    logger.info("Product ones made: %s", monitor.products_made[Type.ONE])
    logger.info("Product twos made: %s", monitor.products_made[Type.TWO])
    logger.info("Product ones made: %s", monitor.products_made[Type.THREE])
    logger.info("Factory run time: %s", calc_factory_runtime)
    logger.info("Factory throughput for product one: %s", monitor.products_made[Type.ONE]/calc_factory_runtime)
    logger.info("Factory throughput for product two: %s", monitor.products_made[Type.TWO]/calc_factory_runtime)
    logger.info("Factory throughput for product three: %s", monitor.products_made[Type.THREE]/calc_factory_runtime)


def terminate_main_thread():
    logger.info("KILLED MAIN THREAD: %s" % threading.currentThread().ident)
    monitor.factory_end_time = time.time()
    calculate_performance()
    # monitor.reset()
    # We may not want to exit the system if we want to do more trials
    # raise SystemExit


def run():
    # Initialization - Model/system variables
    simulation_run_time_secs = 5
    seed = 1
    number_of_trials = 1

    for i in range(number_of_trials):
        np.random.seed(seed)

        workstations = WorkstationFactory.create_all_workstations()
        inspector_one = Inspector(known_workstations=workstations, seed=seed, my_types=[Type.ONE])
        inspector_two = Inspector(known_workstations=workstations, seed=seed, my_types=[Type.TWO, Type.THREE])

        # We need workstations to constantly monitor their buffers and make products
        # We need the inspectors to constantly grab components and put them in the workstation buffer
        # Start threads
        # Daemon threads above will terminate on termination of main, non-daemon thread
        # Start the timer for how long this simulation will go on
        threading.Timer(simulation_run_time_secs, terminate_main_thread).start()
        monitor.factory_start_time = time.time()
        for workstation in workstations:
            workstation.start()
        inspector_one.start()
        inspector_two.start()


if __name__ == "__main__":
    run()
