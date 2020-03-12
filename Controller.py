import logging
import threading
import time

from Inspector import Inspector

# import matplotlib.pyplot as plt
import numpy as np
from Monitor import Monitor
from Type import Type
from Workstation import Workstation, Buffer

logging.basicConfig(format="%(levelname)s: %(relativeCreated)6d %(threadName)s %(message)s",
                    level=logging.INFO, datefmt="%H:%M:%S")
fh = logging.FileHandler('info.log')
fh.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(fh)

# Initialization - Model/system variables

# We'll read the values in as time in minutes. 1 minute = 60 000ms and if we divide by 1000 (sim_speed_factor = 1000),
# we get 60ms, so every 60ms real time is one minute in the simulation.
# If 60ms = 1min in sim, 5s irl = 5000ms irl, then simulation ran for 83.3mins
# If we want to run it for 1000mins in sim, that's 60 000ms irl = 60s irl.
# if simulation_run_time_secs = 180 irl, the simulation runs for 3000mins in simulation
simulation_run_time_secs = 5
# How much faster we want to speed up the timing by to make the simulation run faster
sim_speed_factor = 1000

# TODO: multiple trials with one command not implemented
number_of_trials = 1

# The seed of the RVs used when sampling from a distribution & for inspector two to decide which component (two or three) to produce
seed = 123
np.random.seed(seed)


def find_mean(data):
    total = 0
    num_entries = 300
    for x in range(0, num_entries):
        total += float(data[x])
    return total / num_entries


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
    for i in range(number_of_trials):

        monitor = Monitor().get_instance()

        # Wait until information is logged and monitor is reset
        while monitor.factory_start_time is not 0 or threading.active_count() > 2:
            time.sleep(0.5)

        logger.info("----- Running Trial Number %s -----", i)

        # TODO: separate reading the files from making the calculation for multiple trials
        monitor.model_variables["sim_speed_factor"] = sim_speed_factor

        component1_service_times = open('servinsp1.dat').read().splitlines()
        component2_service_times = open('servinsp22.dat').read().splitlines()
        component3_service_times = open('servinsp23.dat').read().splitlines()
        workstation1_service_times = open('ws1.dat').read().splitlines()
        workstation2_service_times = open('ws2.dat').read().splitlines()
        workstation3_service_times = open('ws3.dat').read().splitlines()
        # Sanity check for exponential distribution sampling
        # samples = []
        # for i in range(300):
        #     samples.append(monitor.sample_service_time(find_mean(component1_service_times))
        # samples.sort()
        # plt.plot(samples, 'bo')
        # plt.show()

        # We need workstations to constantly monitor their buffers and make products
        # We need the inspectors to constantly grab components and put them in the workstation buffer
        # The order matters! Workstation 1 has highest priority and Workstation 3 has the lowest priority
        workstations = [
            Workstation(my_type=Type.THREE,
                        my_buffers=[Buffer(Type.ONE), Buffer(Type.THREE)],
                        mean_st=find_mean(workstation1_service_times)),
            Workstation(my_type=Type.TWO,
                        my_buffers=[Buffer(Type.ONE), Buffer(Type.TWO)],
                        mean_st=find_mean(workstation2_service_times)),
            Workstation(my_type=Type.ONE,
                        my_buffers=[Buffer(Type.ONE)],
                        mean_st=find_mean(workstation3_service_times))
        ]
        inspector_one = Inspector(known_workstations=workstations, seed=seed, my_types=[Type.ONE],
                                  mean_st_components={
                                      Type.ONE: find_mean(component1_service_times)
                                  })
        inspector_two = Inspector(known_workstations=workstations, seed=seed, my_types=[Type.TWO, Type.THREE],
                                  mean_st_components={
                                      Type.TWO: find_mean(component2_service_times),
                                      Type.THREE: find_mean(component3_service_times)
                                  })

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
