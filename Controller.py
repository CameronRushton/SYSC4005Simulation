import logging
import threading
import time
from Inspector import Inspector
from Sampler import Sampler

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
init_bias_min_in_sim = 400
min_in_sim = 2000 + init_bias_min_in_sim

# How much faster we want to speed up the timing by to make the simulation run faster
sim_speed_factor = 10000

simulation_run_time_secs = (min_in_sim / sim_speed_factor) * 60
init_bias_time = (init_bias_min_in_sim / sim_speed_factor) * 60

# The seed of the RVs used when sampling from a distribution & for inspector two to decide which component (two or three) to produce
seed = 123

np.random.seed(seed)
monitor = Monitor().get_instance()
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


def find_mean(data):
    total = 0
    num_entries = 300
    for x in range(0, num_entries):
        total += float(data[x])
    return total / num_entries


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
# queue_sampler = Sampler(known_workstations=workstations, known_inspectors=[inspector_one, inspector_two])


def _convert_to_mins(seconds):
    return seconds / 60


def convert_to_sim_mins(irl_seconds):
    return _convert_to_mins(irl_seconds) * sim_speed_factor


def avg(lst):
    return sum(lst) / len(lst)


# Calculate the throughput of the factory and other metrics using the monitor object
def calculate_performance(monitor):
    num_components_in_queue_samples = {
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

    for workstation in workstations:
        for buffer in workstation.buffers:
            num_components_in_queue_samples[workstation.type][buffer.type] = buffer.sizes
            f1 = open(str(workstation.type) + str(buffer.type) + "-buffer-sizes.txt", "w+")
            for sample in buffer.sizes:
                f1.write(str(sample) + "\n")
            f2 = open(str(workstation.type) + str(buffer.type) + "-buffer-size-times.txt", "w+")
            for sample in buffer.size_timestamps:
                f2.write(str(sample) + "\n")

    factory_run_time = convert_to_sim_mins(monitor.factory_end_time - monitor.factory_start_time)
    factory_init_time = convert_to_sim_mins(monitor.init_bias - monitor.factory_start_time)
    data_collection_time = factory_run_time - factory_init_time
    logger.info("Simulation stats:")
    logger.info("Product ones made: %s", monitor.products_made[Type.ONE])
    logger.info("Product twos made: %s", monitor.products_made[Type.TWO])
    logger.info("Product threes made: %s", monitor.products_made[Type.THREE])
    logger.info("Factory run time (mins): %s", factory_run_time)
    logger.info("Factory init time (mins): %s", factory_init_time)
    logger.info("Factory data collection time (mins): %s", data_collection_time)
    logger.info("Factory throughput (products/hour) for product one: %s",
                monitor.products_made[Type.ONE] / data_collection_time * 60)  # Multiply by 60 to convert mins to hours
    logger.info("Factory throughput (products/hour) for product two: %s",
                monitor.products_made[Type.TWO] / data_collection_time * 60)
    logger.info("Factory throughput (products/hour) for product three: %s",
                monitor.products_made[Type.THREE] / data_collection_time * 60)
    c1_block_time_mins = convert_to_sim_mins(sum(monitor.component_block_times[Type.ONE]))
    c2_block_time_mins = convert_to_sim_mins(sum(monitor.component_block_times[Type.TWO]))
    c3_block_time_mins = convert_to_sim_mins(sum(monitor.component_block_times[Type.THREE]))
    i1_prop_block = c1_block_time_mins / data_collection_time
    i2_prop_block = (c2_block_time_mins + c3_block_time_mins) / data_collection_time
    logger.info("Inspector one component one's total block time (mins): %s", c1_block_time_mins)
    logger.info("Inspector one proportion of time blocked: %s %%", i1_prop_block * 100)
    logger.info("Inspector two component two's total block time (mins): %s", c2_block_time_mins)
    logger.info("Inspector two component three's total block time (mins): %s", c3_block_time_mins)
    logger.info("Inspector two total block time (mins): %s", c2_block_time_mins + c3_block_time_mins)
    logger.info("Inspector two proportion of time blocked: %s %%", i2_prop_block * 100)
    num_c1_queued_for_w1 = len(monitor.component_queue_times[Type.ONE][Type.ONE])
    num_c1_queued_for_w2 = len(monitor.component_queue_times[Type.TWO][Type.ONE])
    num_c1_queued_for_w3 = len(monitor.component_queue_times[Type.THREE][Type.ONE])
    total_c1_queued = num_c1_queued_for_w1 + num_c1_queued_for_w2 + num_c1_queued_for_w3
    total_c2_queued = len(monitor.component_queue_times[Type.TWO][Type.TWO])  # num_c2_queued_for_w2
    total_c3_queued = len(monitor.component_queue_times[Type.THREE][Type.THREE])  # num_c3_queued_for_w3

    logger.info("Total component 1s placed in a queue: %s", total_c1_queued)
    # 0 <= Total placed in queue - Total products made <= total capacity in system (num slots in c1 queues and workstations with c1 queues and inspectors that have a component)?
    num_possible_spaces_in_sys_for_c1 = 2 + 2 + 2 + 1 + 1 + 1 + 1  # 2 for each queue (6), one in inspector's hands (1), one for each workstation (3)
    is_possible = 0 <= (total_c1_queued - monitor.products_made[Type.ONE] - monitor.products_made[Type.TWO] -
                        monitor.products_made[Type.THREE]) <= num_possible_spaces_in_sys_for_c1
    logger.info("Is this possible? %s", is_possible)
    num_possible_spaces_in_sys_for_c2 = 4  # 2 for each queue (2), one in inspector's hands (1), one for each workstation that deals with component 2 (1)
    logger.info("Total component 2s placed in a queue: %s", total_c2_queued)
    is_possible = 0 <= (total_c2_queued - monitor.products_made[Type.TWO]) <= num_possible_spaces_in_sys_for_c2
    logger.info("Is this possible? %s", is_possible)
    num_possible_spaces_in_sys_for_c3 = 4  # 2 for each queue (2), one in inspector's hands (1), one for each workstation that deals with component 3 (1)
    logger.info("Total component 3s placed in a queue: %s", total_c3_queued)
    is_possible = 0 <= (total_c3_queued - monitor.products_made[Type.THREE]) <= num_possible_spaces_in_sys_for_c3
    logger.info("Is this possible? %s", is_possible)

    avg_queue_time_w1_c1 = convert_to_sim_mins(
        sum(monitor.component_queue_times[Type.ONE][Type.ONE]) / num_c1_queued_for_w1)
    avg_queue_time_w2_c1 = convert_to_sim_mins(
        sum(monitor.component_queue_times[Type.TWO][Type.ONE]) / num_c1_queued_for_w2)
    avg_queue_time_w3_c1 = convert_to_sim_mins(
        sum(monitor.component_queue_times[Type.THREE][Type.ONE]) / num_c1_queued_for_w3)
    avg_queue_time_w2_c2 = convert_to_sim_mins(sum(monitor.component_queue_times[Type.TWO][Type.TWO]) / total_c2_queued)
    avg_queue_time_w3_c3 = convert_to_sim_mins(
        sum(monitor.component_queue_times[Type.THREE][Type.THREE]) / total_c3_queued)
    logger.info("Average queue wait times: ")
    logger.info("Workstation 1 component 1 queue wait time average (mins): %s", avg_queue_time_w1_c1)
    logger.info("Workstation 2 component 1 queue wait time average (mins): %s", avg_queue_time_w2_c1)
    logger.info("Workstation 3 component 1 queue wait time average (mins): %s", avg_queue_time_w3_c1)
    logger.info("Workstation 2 component 2 queue wait time average (mins): %s", avg_queue_time_w2_c2)
    logger.info("Workstation 3 component 3 queue wait time average (mins): %s", avg_queue_time_w3_c3)

    # Apply Little's law
    #  Expected values:  L  =  throughput  *   W
    avg_c1_in_w1 = (num_c1_queued_for_w1 / data_collection_time) * avg_queue_time_w1_c1
    avg_c1_in_w2 = (num_c1_queued_for_w2 / data_collection_time) * avg_queue_time_w2_c1
    avg_c1_in_w3 = (num_c1_queued_for_w3 / data_collection_time) * avg_queue_time_w3_c1
    avg_c2_in_w2 = (total_c2_queued / data_collection_time) * avg_queue_time_w2_c2
    avg_c3_in_w3 = (total_c3_queued / data_collection_time) * avg_queue_time_w3_c3
    # Actual values for L
    # TODO: This is incorrect because it also counts values when it's not in steady state
    actual_avg_c1_in_w1 = avg(num_components_in_queue_samples[Type.ONE][Type.ONE])
    actual_avg_c1_in_w2 = avg(num_components_in_queue_samples[Type.TWO][Type.ONE])
    actual_avg_c2_in_w2 = avg(num_components_in_queue_samples[Type.TWO][Type.TWO])
    actual_avg_c1_in_w3 = avg(num_components_in_queue_samples[Type.THREE][Type.ONE])
    actual_avg_c3_in_w3 = avg(num_components_in_queue_samples[Type.THREE][Type.THREE])
    logger.info("Expected average number of components in workstation 1 queue 1: %s", avg_c1_in_w1)
    logger.info("Actual average number of components in workstation 1 queue 1: %s", actual_avg_c1_in_w1)
    logger.info("Percent difference: %s",
                abs(avg_c1_in_w1 - actual_avg_c1_in_w1) / ((avg_c1_in_w1 + actual_avg_c1_in_w1) / 2) * 100)

    logger.info("Expected average number of components in workstation 2 queue 1: %s", avg_c1_in_w2)
    logger.info("Actual average number of components in workstation 2 queue 1: %s", actual_avg_c1_in_w2)
    logger.info("Percent difference: %s",
                abs(avg_c1_in_w2 - actual_avg_c1_in_w2) / ((avg_c1_in_w2 + actual_avg_c1_in_w2) / 2) * 100)

    logger.info("Expected average number of components in workstation 2 queue 2: %s", avg_c2_in_w2)
    logger.info("Actual average number of components in workstation 2 queue 2: %s", actual_avg_c2_in_w2)
    logger.info("Percent difference: %s",
                abs(avg_c2_in_w2 - actual_avg_c2_in_w2) / ((avg_c2_in_w2 + actual_avg_c2_in_w2) / 2) * 100)

    logger.info("Expected average number of components in workstation 3 queue 1: %s", avg_c1_in_w3)
    logger.info("Actual average number of components in workstation 3 queue 1: %s", actual_avg_c1_in_w3)
    logger.info("Percent difference: %s",
                abs(avg_c1_in_w3 - actual_avg_c1_in_w3) / ((avg_c1_in_w3 + actual_avg_c1_in_w3) / 2) * 100)

    logger.info("Expected average number of components in workstation 3 queue 3: %s", avg_c3_in_w3)
    logger.info("Actual average number of components in workstation 3 queue 3: %s", actual_avg_c3_in_w3)
    logger.info("Percent difference: %s",
                abs(avg_c3_in_w3 - actual_avg_c3_in_w3) / ((avg_c3_in_w3 + actual_avg_c3_in_w3) / 2) * 100)

    # avg_component1_in_system = (avgBlockTimeOfComponent1 + avgQueueTimeOfComponent1) * numC1Grabbed / factoryRunTime
    # We're taking into account that the inspectors may have a component in hand. The component block time also takes
    # ...this into account, so the block times are correct as well.
    currently_held_components = {
        Type.ONE: 0,
        Type.TWO: 0,
        Type.THREE: 0
    }
    if inspector_one.component is not None:
        currently_held_components[
            inspector_one.component] = 1  # We can set it to one because the inspectors are assigned different types
    if inspector_two.component is not None:
        currently_held_components[inspector_two.component] = 1
    num_c1_grabbed = total_c1_queued + currently_held_components[Type.ONE]
    num_c2_grabbed = total_c2_queued + currently_held_components[Type.TWO]
    num_c3_grabbed = total_c3_queued + currently_held_components[Type.THREE]
    avg_c1_time_blocked = (c1_block_time_mins / num_c1_grabbed)
    avg_c2_time_blocked = (c2_block_time_mins / num_c2_grabbed)
    avg_c3_time_blocked = (c3_block_time_mins / num_c3_grabbed)
    avg_c1_in_sys = (avg_c1_time_blocked + avg_queue_time_w1_c1 + avg_queue_time_w2_c1 + avg_queue_time_w3_c1) * (
            num_c1_grabbed / data_collection_time)
    avg_c2_in_sys = (avg_c2_time_blocked + avg_queue_time_w2_c2) * (num_c2_grabbed / data_collection_time)
    avg_c3_in_sys = (avg_c3_time_blocked + avg_queue_time_w3_c3) * (num_c3_grabbed / data_collection_time)
    exp_avg_components_in_sys = avg_c1_in_sys + avg_c2_in_sys + avg_c3_in_sys
    logger.info("Expected average number of components in the system: %s", avg_c1_in_sys + avg_c2_in_sys + avg_c3_in_sys)
    logger.info("Actual average number of components in the system: %s", avg(monitor.avg_components_in_system))
    logger.info("Percent difference: %s",
                abs(exp_avg_components_in_sys - avg(monitor.avg_components_in_system)) / ((exp_avg_components_in_sys + avg(monitor.avg_components_in_system)) / 2) * 100)

    logger.info("")
    prod1_made = monitor.products_made[Type.ONE]
    logger.info("Factory throughput (products/hour) for product one: %s",
                prod1_made / data_collection_time * 60)
    prod2_made = monitor.products_made[Type.TWO]
    logger.info("Factory throughput (products/hour) for product two: %s",
                prod2_made / data_collection_time * 60)
    prod3_made = monitor.products_made[Type.THREE]
    logger.info("Factory throughput (products/hour) for product three: %s",
                prod3_made / data_collection_time * 60)
    total_products_made = prod1_made + prod2_made + prod3_made
    logger.info("Factory total throughput (products/hour): %s",
                total_products_made / data_collection_time * 60)
    logger.info("")
    i1_prop_block = c1_block_time_mins / data_collection_time
    i2_block_time_mins = c2_block_time_mins + c3_block_time_mins
    i2_prop_block = i2_block_time_mins / data_collection_time
    logger.info("Inspector one total block time (mins): %s", c1_block_time_mins)
    logger.info("Inspector one proportion of time blocked: %s %%",
                i1_prop_block * 100)
    logger.info("Inspector two total block time (mins): %s", i2_block_time_mins)
    logger.info("Inspector two proportion of time blocked: %s %%",
                i2_prop_block * 100)
    logger.info("")


def terminate_threads(monitor):
    logger.info("Issuing threads to stop.")
    monitor.end_simulation()
    while threading.active_count() > 2:  # We should only have this thread and the main thread left
        time.sleep(0.5)
    calculate_performance(monitor)
    monitor.reset()


def run(init_bias):
    # Start threads
    logger.info("-------------- Starting Simulation --------------")
    monitor.init_bias = time.time() + init_bias
    monitor.factory_start_time = time.time()
    for workstation in workstations:
        workstation.start()
    inspector_one.start()
    inspector_two.start()
    # queue_sampler.start()

    # Start the timer for how long this simulation will go on
    threading.Timer(simulation_run_time_secs, terminate_threads, args=[monitor]).start()


if __name__ == "__main__":
    run(init_bias_time)
