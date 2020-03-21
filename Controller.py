import logging
import threading
import time

from Inspector import Inspector

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
simulation_run_time_secs = 30
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


def _convert_to_mins(seconds):
    return seconds / 60


def convert_to_sim_mins(irl_seconds):
    return _convert_to_mins(irl_seconds) * sim_speed_factor


# Calculate the throughput of the factory and other metrics using the monitor object
def calculate_performance(monitor):
    factory_run_time = convert_to_sim_mins(monitor.factory_end_time - monitor.factory_start_time)
    logger.info("Product ones made: %s", monitor.products_made[Type.ONE])
    logger.info("Product twos made: %s", monitor.products_made[Type.TWO])
    logger.info("Product threes made: %s", monitor.products_made[Type.THREE])
    logger.info("Factory run time (mins): %s", factory_run_time)
    logger.info("Factory throughput (products/hour) for product one: %s", monitor.products_made[Type.ONE]/factory_run_time*60)  # Multiply by 60 to convert mins to hours
    logger.info("Factory throughput (products/hour) for product two: %s", monitor.products_made[Type.TWO]/factory_run_time*60)
    logger.info("Factory throughput (products/hour) for product three: %s", monitor.products_made[Type.THREE]/factory_run_time*60)
    logger.info("Inspector one component one's total block time (mins): %s", convert_to_sim_mins(sum(monitor.component_block_times[Type.ONE])))
    logger.info("Inspector two component two's total block time (mins): %s", convert_to_sim_mins(sum(monitor.component_block_times[Type.TWO])))
    logger.info("Inspector two component three's total block time (mins): %s", convert_to_sim_mins(sum(monitor.component_block_times[Type.THREE])))
    num_c1_queued_for_w1 = len(monitor.component_queue_times[Type.ONE][Type.ONE])
    num_c1_queued_for_w2 = len(monitor.component_queue_times[Type.TWO][Type.ONE])
    num_c1_queued_for_w3 = len(monitor.component_queue_times[Type.THREE][Type.ONE])
    total_c1_grabbed = num_c1_queued_for_w1 + num_c1_queued_for_w2 + num_c1_queued_for_w3
    total_c2_grabbed = len(monitor.component_queue_times[Type.TWO][Type.TWO])  # num_c2_queued_for_w2
    total_c3_grabbed = len(monitor.component_queue_times[Type.THREE][Type.THREE])  # num_c3_queued_for_w3

    logger.info("Total component 1s placed in a queue: %s", total_c1_grabbed)
    # 0 <= Total placed in queue - Total products made <= total capacity in system (num slots in c1 queues and workstations with c1 queues)?
    is_possible = 0 <= (total_c1_grabbed - monitor.products_made[Type.ONE] - monitor.products_made[Type.TWO] - monitor.products_made[Type.THREE]) <= 9  # TODO: Hard coded magic number
    logger.info("Is this possible? %s", is_possible)
    logger.info("Total component 2s placed in a queue: %s", total_c2_grabbed)
    is_possible = 0 <= (total_c2_grabbed - monitor.products_made[Type.TWO]) <= 3  # TODO: Hard coded magic number
    logger.info("Is this possible? %s", is_possible)
    logger.info("Total component 3s placed in a queue: %s", total_c3_grabbed)
    is_possible = 0 <= (total_c3_grabbed - monitor.products_made[Type.THREE]) <= 3  # TODO: Hard coded magic number
    logger.info("Is this possible? %s", is_possible)

    logger.info("Average queue wait times: ")
    avg_queue_time_w1_c1 = convert_to_sim_mins(sum(monitor.component_queue_times[Type.ONE][Type.ONE]) / num_c1_queued_for_w1)
    logger.info("Workstation 1 component 1 queue wait time average (mins): %s", avg_queue_time_w1_c1)

    avg_queue_time_w2_c1 = convert_to_sim_mins(sum(monitor.component_queue_times[Type.TWO][Type.ONE]) / num_c1_queued_for_w2)
    logger.info("Workstation 2 component 1 queue wait time average (mins): %s", avg_queue_time_w2_c1)

    avg_queue_time_w3_c1 = convert_to_sim_mins(sum(monitor.component_queue_times[Type.THREE][Type.ONE]) / num_c1_queued_for_w3)
    logger.info("Workstation 3 component 1 queue wait time average (mins): %s", avg_queue_time_w3_c1)

    avg_queue_time_w2_c2 = convert_to_sim_mins(sum(monitor.component_queue_times[Type.TWO][Type.TWO]) / total_c2_grabbed)
    logger.info("Workstation 2 component 2 queue wait time average (mins): %s", avg_queue_time_w2_c2)

    avg_queue_time_w3_c3 = convert_to_sim_mins(sum(monitor.component_queue_times[Type.THREE][Type.THREE]) / total_c3_grabbed)
    logger.info("Workstation 3 component 3 queue wait time average (mins): %s", avg_queue_time_w3_c3)

    # Apply Little's law
    avg_c1_in_w1 = (num_c1_queued_for_w1 / factory_run_time) * avg_queue_time_w1_c1
    avg_c1_in_w2 = (num_c1_queued_for_w2 / factory_run_time) * avg_queue_time_w2_c1
    avg_c1_in_w3 = (num_c1_queued_for_w3 / factory_run_time) * avg_queue_time_w3_c1
    avg_c2_in_w2 = (total_c2_grabbed / factory_run_time) * avg_queue_time_w2_c2
    avg_c3_in_w3 = (total_c3_grabbed / factory_run_time) * avg_queue_time_w3_c3
    logger.info("Average number of components in workstation 1 queue 1: %s", avg_c1_in_w1)
    logger.info("Average number of components in workstation 2 queue 1: %s", avg_c1_in_w2)
    logger.info("Average number of components in workstation 2 queue 2: %s", avg_c2_in_w2)
    logger.info("Average number of components in workstation 3 queue 1: %s", avg_c1_in_w3)
    logger.info("Average number of components in workstation 4 queue 3: %s", avg_c3_in_w3)

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
            Workstation(my_type=Type.ONE,
                        my_buffers=[Buffer(Type.ONE)],
                        mean_st=find_mean(workstation3_service_times)),
            Workstation(my_type=Type.TWO,
                        my_buffers=[Buffer(Type.ONE), Buffer(Type.TWO)],
                        mean_st=find_mean(workstation2_service_times)),
            Workstation(my_type=Type.THREE,
                        my_buffers=[Buffer(Type.ONE), Buffer(Type.THREE)],
                        mean_st=find_mean(workstation1_service_times))
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
