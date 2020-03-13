import logging
import threading
import time

from Inspector import Inspector

import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.api as sm
import pylab as py
import math
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
seed = 1
np.random.seed(seed)


monitor = Monitor().get_instance()
component1_service_times = open('servinsp1.dat').read().splitlines()
component2_service_times = open('servinsp22.dat').read().splitlines()
component3_service_times = open('servinsp23.dat').read().splitlines()
workstation1_service_times = open('ws1.dat').read().splitlines()
workstation2_service_times = open('ws2.dat').read().splitlines()
workstation3_service_times = open('ws3.dat').read().splitlines()


def write_array_vertically_to_file(array, file):
    for j in range(len(array)):
        file.write(str(array[j]) + "\n")
    file.write("\n\n")


num_bins = 14

# Init. input data
f = open("workstation_3_st_data.txt","w+")
data = workstation3_service_times
# Convert values from strings to floats
data = np.array(data).astype(np.float)

num_samples = len(data)
f.write("num_samples: " + str(num_samples) + "\n")
f.write("num_bins: " + str(num_bins) + "\n")
f.write("data: \n")
write_array_vertically_to_file(data, f)

data.sort()
f.write("sorted data: \n")
write_array_vertically_to_file(data, f)

mean = np.mean(data)
f.write("mean: " + str(mean) + "\n")
f.write("variance: " + str(np.var(data)) + "\n")
max_val = max(data)
min_val = min(data)
f.write("max: " + str(max_val) + "\n")
f.write("min: " + str(min_val) + "\n")


# Create Q-Q plot to see if input data relates to samples
samples_from_distribution = np.random.exponential(mean, num_samples)
f.write("sorted samples from distribution for Q-Q plot: \n")
samples_from_distribution.sort()
write_array_vertically_to_file(samples_from_distribution, f)

# Uncomment me to create the Q-Q plot
# sm.qqplot_2samples(data, samples_from_distribution, ylabel="Quantiles of input service times (minutes)",
#                    xlabel="Quantiles of drawn service times (minutes) (exp. distrib.)", line='45')


binwidth = max_val / num_bins
observed_frequencies, junk = np.histogram(data, bins=np.arange(min_val, max_val + binwidth, binwidth))
f.write("histogram frequencies in each bin: \n")
write_array_vertically_to_file(observed_frequencies, f)

# Uncomment me to create the histogram
plt.hist(data, bins=np.arange(min_val, max_val + binwidth, binwidth), alpha=0.8)
plt.title('Workstation 3 Service Times')
plt.xlabel(str(num_bins) + ' service time (mins) bins of width ' + str(binwidth))
plt.ylabel('Frequency')


# Chi-square test
# (lambda)e^(-(lambda)(x)) is the pdf
# lambda = reciprocal rate
reciprocal_rate = 1/mean
f.write("reciprocal rate " + str(reciprocal_rate) + "\n")
# Null hypothesis: RV follows an exponential distrib.
# Alt Hypothesis: It does not follow exp. distrib.
# pdf = 1 - math.exp(reciprocal_rate * endpoint_of_interval_i)
# Create endpoints of intervals array
f.write("bins \n")
endpoint_of_intervals = []
for i in range(num_bins+1):
    if i != 0:
        endpoint_of_intervals.append(i * binwidth)
write_array_vertically_to_file(endpoint_of_intervals, f)
f.write("\n")

# Generate expected percentage of values in each bin and multiply each probability by number of samples to get the expected frequency in each bin
f.write("P(X=x) \n")
expected_probabilities = []
for i in range(num_bins):
    if i is 0:
        expected_probabilities.append(1 - math.exp(-1 * reciprocal_rate * endpoint_of_intervals[i]))
    else:
        expected_probabilities.append((1 - math.exp(-1 * reciprocal_rate * endpoint_of_intervals[i])) - sum(expected_probabilities))

write_array_vertically_to_file(expected_probabilities, f)
f.write("\n")

f.write("Expected \n")
expected_frequencies = []
for i in range(num_bins):
    expected_frequencies.append(expected_probabilities[i] * num_samples)
write_array_vertically_to_file(expected_frequencies, f)
f.write("\n")

# Calculate chi-square: X^2 = (Observed - Expected)^2 / Expected
chi_square_values = []
f.write("X^2 \n")
for i in range(num_bins):
    chi_square_values.append((observed_frequencies[i] - expected_frequencies[i])**2 / expected_frequencies[i])
write_array_vertically_to_file(chi_square_values, f)
f.write("\n")
chi_square = sum(chi_square_values)
f.write("X^2 = " + str(chi_square) + "\n")
degrees_of_freedom = num_bins - 1 - 1
f.write("degrees of freedom = " + str(degrees_of_freedom) + "\n")
alpha = 0.05  # Level of significance
f.write("alpha (significance) = " + str(alpha) + "\n")

plt.show()
f.close()


def find_mean(data):
    total = 0
    num_entries = len(data)
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
    return
    for i in range(number_of_trials):

        monitor = Monitor().get_instance()

        # Wait until information is logged and monitor is reset
        while monitor.factory_start_time is not 0 or threading.active_count() > 2:
            time.sleep(0.5)

        logger.info("----- Running Trial Number %s -----", i)

        # TODO: separate reading the files from making the calculation for multiple trials
        monitor.model_variables["sim_speed_factor"] = sim_speed_factor

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
