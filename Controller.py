import logging
import threading
import time

from Inspector import Inspector
import WorkstationFactory

import numpy as np
from Monitor import Monitor
from Type import Type

logging.basicConfig(format="%(levelname)s: %(relativeCreated)6d %(threadName)s %(message)s", level=logging.INFO, datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)
monitor = Monitor().get_instance()


def read_model():
    component1_service_times = open('servinsp1.dat').read().splitlines()
    monitor.model_variables["component_service_times"][Type.ONE] = find_mean(component1_service_times)
    component2_service_times = open('servinsp22.dat').read().splitlines()
    monitor.model_variables["component_service_times"][Type.TWO] = find_mean(component2_service_times)
    component3_service_times = open('servinsp23.dat').read().splitlines()
    monitor.model_variables["component_service_times"][Type.THREE] = find_mean(component3_service_times)
    workstation1_service_times = open('ws1.dat').read().splitlines()
    monitor.model_variables["workstation_service_times"][Type.ONE] = find_mean(workstation1_service_times)
    workstation2_service_times = open('ws2.dat').read().splitlines()
    monitor.model_variables["workstation_service_times"][Type.TWO] = find_mean(workstation2_service_times)
    workstation3_service_times = open('ws3.dat').read().splitlines()
    monitor.model_variables["workstation_service_times"][Type.THREE] = find_mean(workstation3_service_times)


def find_mean(data):
    total = 0
    num_entries = 300
    sim_speed_factor = 1000  # How much faster we want to speed up the timing by to make the simulation happen faster
    for x in range(0, num_entries):
        total += float(data[x])
    mean = total / num_entries
    return np.random.exponential(mean, 1)[0] * 60 / sim_speed_factor  # Draw from exponential distribution and convert to seconds


# Calculate the throughput of the factory and other metrics using the monitor object
# Since this is on the main thread, the simulation will still be running while we print these out.
def calculate_performance():
    calc_factory_runtime = monitor.factory_end_time - monitor.factory_start_time
    logger.info("Product ones made: %s", monitor.products_made[Type.ONE])
    logger.info("Product twos made: %s", monitor.products_made[Type.TWO])
    logger.info("Product threes made: %s", monitor.products_made[Type.THREE])
    logger.info("Factory run time: %s", calc_factory_runtime)
    logger.info("Factory throughput for product one: %s", monitor.products_made[Type.ONE]/calc_factory_runtime)
    logger.info("Factory throughput for product two: %s", monitor.products_made[Type.TWO]/calc_factory_runtime)
    logger.info("Factory throughput for product three: %s", monitor.products_made[Type.THREE]/calc_factory_runtime)
    # TODO: These block times may be inaccurate right now because there is a chance that an inspector is blocked while
    # the simulation finishes, so it didn't get a chance to register the final block time.
    logger.info("Inspector one component one's total block time: %s", sum(monitor.component_block_times[Type.ONE]))
    logger.info("Inspector two component two's total block time: %s", sum(monitor.component_block_times[Type.TWO]))
    logger.info("Inspector two component three's total block time: %s", sum(monitor.component_block_times[Type.THREE]))

def terminate_main_thread():
    logger.info("KILLING MAIN THREAD: %s" % threading.currentThread().ident)
    monitor.factory_end_time = time.time()
    calculate_performance()
    # monitor.reset()
    # We may not want to exit the system if we want to do more trials
    # raise SystemExit


def run():
    # Initialization - Model/system variables
    simulation_run_time_secs = 300
    seed = 1  # The seed for inspector two to decide which component (two or three) to produce
    number_of_trials = 1
    servinsp1 = np.loadtxt('servinsp1.dat')
    servinsp22 = np.loadtxt('servinsp22.dat')
    servinsp23 = np.loadtxt('servinsp23.dat')

    workstation_one_times = np.loadtxt('ws1.dat')
    workstation_two_times = np.loadtxt('ws2.dat')
    workstation_three_times = np.loadtxt('ws3.dat')

    read_model()

    for i in range(number_of_trials):
        np.random.seed(seed)
        workstations = WorkstationFactory.create_all_workstations(times_work_one=workstation_one_times, times_work_two=workstation_two_times, times_work_three=workstation_three_times)
        inspector_one = Inspector(inspector_type=Type.ONE, known_workstations=workstations, seed=seed, my_types=[Type.ONE], inspection_times=[servinsp1])
        inspector_two = Inspector(inspector_type=Type.TWO, known_workstations=workstations, seed=seed, my_types=[Type.TWO, Type.THREE], inspection_times=[servinsp22, servinsp23])

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
