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
fh = logging.FileHandler('info.log')
fh.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(fh)
# How much faster we want to speed up the timing by to make the simulation run faster
# We'll read the values in as time in minutes. 1 minute = 60 000ms and if we divide by 1000, we get 60ms
# So, every 60ms is one minute.
sim_speed_factor = 1000


def read_model(monitor):
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
    for x in range(0, num_entries):
        total += float(data[x])
    mean = total / num_entries
    # TODO: This mistakenly takes only the first value. We want to keep this distrib. and have some rng values to pick
    # TODO: ... points in the distribution to be the service time. Right now, the service times are the same thoughout which is wrong.
    # TODO: We should convert to seconds and divide by the speed factor when we want to actually use the time and get a new one once used.
    return np.random.exponential(mean, 1)[0] * 60 / sim_speed_factor  # Draw from exponential distribution and convert to seconds


# Calculate the throughput of the factory and other metrics using the monitor object
def calculate_performance(monitor):
    calc_factory_runtime = (monitor.factory_end_time - monitor.factory_start_time) * sim_speed_factor / 60
    logger.info("Product ones made: %s", monitor.products_made[Type.ONE])
    logger.info("Product twos made: %s", monitor.products_made[Type.TWO])
    logger.info("Product threes made: %s", monitor.products_made[Type.THREE])
    logger.info("Factory run time (mins): %s", calc_factory_runtime)
    logger.info("Factory throughput (products/min) for product one: %s", monitor.products_made[Type.ONE]/calc_factory_runtime)
    logger.info("Factory throughput (products/min) for product two: %s", monitor.products_made[Type.TWO]/calc_factory_runtime)
    logger.info("Factory throughput (products/min) for product three: %s", monitor.products_made[Type.THREE]/calc_factory_runtime)
    logger.info("Inspector one component one's total block time (mins): %s", sum(monitor.component_block_times[Type.ONE])*sim_speed_factor/60)
    logger.info("Inspector two component two's total block time (mins): %s", sum(monitor.component_block_times[Type.TWO])*sim_speed_factor/60)
    logger.info("Inspector two component three's total block time (mins): %s", sum(monitor.component_block_times[Type.THREE])*sim_speed_factor/60)


def terminate_threads(monitor):
    logger.info("Issuing threads to stop.")
    monitor.end_simulation()
    while threading.active_count() > 2:  # We should only have this thread and the main thread left
        time.sleep(0.5)
    calculate_performance(monitor)
    monitor.reset()


def run():
    # Initialization - Model/system variables
    # If 60ms = 1min in sim, 5s = 5000ms irl, then simulation ran for 83.3mins
    # If we want to run it for 1000mins in sim, that's 60 000ms irl = 60s.
    simulation_run_time_secs = 180
    seed = 1  # The seed for inspector two to decide which component (two or three) to produce
    number_of_trials = 1

    for i in range(number_of_trials):

        monitor = Monitor().get_instance()

        # Wait until information is logged and monitor is reset
        while monitor.factory_start_time is not 0 or threading.active_count() > 2:
            time.sleep(0.5)

        logger.info("----- Running Trial Number %s -----", i)

        # TODO: separate reading the files from making the calculation for multiple trials
        read_model(monitor)
        print(monitor.model_variables)

        np.random.seed(seed)

        # We need workstations to constantly monitor their buffers and make products
        # We need the inspectors to constantly grab components and put them in the workstation buffer
        workstations = WorkstationFactory.create_all_workstations()
        inspector_one = Inspector(known_workstations=workstations, seed=seed, my_types=[Type.ONE])
        inspector_two = Inspector(known_workstations=workstations, seed=seed, my_types=[Type.TWO, Type.THREE])

        # Start threads
        monitor.factory_start_time = time.time()
        for workstation in workstations:
            workstation.start()
        inspector_one.start()
        inspector_two.start()

        # Start the timer for how long this simulation will go on
        threading.Timer(simulation_run_time_secs, terminate_threads, args=[monitor]).start()


if __name__ == "__main__":
    run()
