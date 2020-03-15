import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import math

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


####################
# Init. input data #
####################
seed = 1
np.random.seed(seed)
num_bins = 40
f = open("workstation_3_st_data_TEST.txt", "w+")
data = workstation3_service_times


#################
# Program start #
#################
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

fig, axs = plt.subplots(2, figsize=(8, 12))
axs[0].set_title("Q-Q plot of exponential samples vs. input data")

# Create Q-Q plot to see if input data relates to samples
samples_from_distribution = np.random.exponential(mean, num_samples)
f.write("sorted samples from distribution for Q-Q plot: \n")
samples_from_distribution.sort()
write_array_vertically_to_file(samples_from_distribution, f)

# Uncomment me to create the Q-Q plot
sm.qqplot_2samples(data, samples_from_distribution, ylabel="Quantiles of input service times (minutes)",
                   xlabel="Quantiles of drawn service times (minutes) (exp. distrib.)", line='45', ax=axs[0])


binwidth = max_val / num_bins
observed_frequencies, junk = np.histogram(data, bins=np.arange(min_val, max_val + binwidth, binwidth))
f.write("histogram frequencies in each bin: \n")
write_array_vertically_to_file(observed_frequencies, f)

# Uncomment me to create the histogram
axs[1].hist(data, bins=np.arange(min_val, max_val + binwidth, binwidth), alpha=0.8)
axs[1].set_title('Workstation 3 Service Times')
axs[1].set_xlabel(str(num_bins) + ' service time (mins) bins of width ' + str(binwidth))
axs[1].set_ylabel('Frequency')


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