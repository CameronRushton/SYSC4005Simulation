# This file compares two simulation strategies using the data generated from the runs
import math
import statistics as stats
import numpy as np
import scipy.stats


def calc_mean_to_string(lst):
    lst = [float(i) for i in lst]
    return str(round(stats.mean(lst), 5))


def calc_variance_to_string(lst):
    lst = [float(i) for i in lst]
    return str(round(stats.variance(lst), 9))


def mean_confidence_interval(data, confidence=0.95):
    data = [float(i) for i in data]
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return str(m), str(m-h), str(m+h)


def calc_crn_difference_variance(samples_sys1, samples_sys2, variance1, variance2):
    samples_sys1 = [float(i) for i in samples_sys1]
    samples_sys2 = [float(i) for i in samples_sys2]
    covariance = np.cov(samples_sys1, samples_sys2)[0][1]
    variance = variance1 + variance2 - 2 * covariance
    return str(variance)


def calc_crn_ci(mean, variance, num_samples, confidence=0.95):
    variance = float(variance)
    se = math.sqrt(variance) / math.sqrt(num_samples)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., num_samples - 1)
    return str(mean - h), str(mean + h)


# To calculate the confidence interval for differences, it's +/- (t alpha/2,v)(sqrt(variance1/numReplications + variance2/numReplications))
# where v = ((variance1/numReplications + variance2/numReplications)^2 / (((variance1/numReplications)^2 / (numReplications+1)) + ((variance2/numReplications)^2 / (numReplications+1)))) - 2
# assuming that num samples is the same for both
# This is for independent sampling with unequal variances. Need num replications > 7
# (not used in the milestone)
def calc_difference_confidence_interval(difference, variance1, variance2, num_samples):
    variance1 = float(variance1)
    variance2 = float(variance2)
    v_denominator = ((variance1/num_samples)**2 / (num_samples+1)) + ((variance2/num_samples)**2 / (num_samples+1))
    if v_denominator == 0:
        v_denominator = 1
    v = (variance1/num_samples + variance2/num_samples)**2 / v_denominator
    v = v - 2
    h = scipy.stats.t.ppf((1 + 0.95) / 2., round(v)) * math.sqrt(variance1/num_samples + variance2/num_samples)
    return str(difference - h), str(difference + h)

# SYSTEM ONE
# Products produced
product1_produced_sys1 = open("./m4_data/product1_produced_sys1.dat").read().splitlines()
num_replications_sys1 = len(product1_produced_sys1)
mean_product1_produced_sys1 = calc_mean_to_string(product1_produced_sys1)
variance_product1_produced_sys1 = calc_variance_to_string(product1_produced_sys1)
confidence_product1_produced_sys1, min_confidence_product1_produced_sys1, max_confidence_product1_produced_sys1 = mean_confidence_interval(product1_produced_sys1)

product2_produced_sys1 = open("./m4_data/product2_produced_sys1.dat").read().splitlines()
mean_product2_produced_sys1 = calc_mean_to_string(product2_produced_sys1)
variance_product2_produced_sys1 = calc_variance_to_string(product2_produced_sys1)
confidence_product2_produced_sys1, min_confidence_product2_produced_sys1, max_confidence_product2_produced_sys1 = mean_confidence_interval(product2_produced_sys1)

product3_produced_sys1 = open("./m4_data/product3_produced_sys1.dat").read().splitlines()
mean_product3_produced_sys1 = calc_mean_to_string(product3_produced_sys1)
variance_product3_produced_sys1 = calc_variance_to_string(product3_produced_sys1)
confidence_product3_produced_sys1, min_confidence_product3_produced_sys1, max_confidence_product3_produced_sys1 = mean_confidence_interval(product3_produced_sys1)

total_products_produced_sys1 = open("./m4_data/total_products_produced_sys1.dat").read().splitlines()
mean_total_products_produced_sys1 = calc_mean_to_string(total_products_produced_sys1)
variance_total_products_produced_sys1 = calc_variance_to_string(total_products_produced_sys1)
confidence_total_products_produced_sys1, min_total_products_produced_sys1, max_total_products_produced_sys1 = mean_confidence_interval(total_products_produced_sys1)

# Throughput
throughput_product1_sys1 = open("./m4_data/throughput_product1_sys1.dat").read().splitlines()
mean_throughput_product1_sys1 = calc_mean_to_string(throughput_product1_sys1)
variance_throughput_product1_sys1 = calc_variance_to_string(throughput_product1_sys1)
confidence_throughput_product1_sys1, min_throughput_product1_sys1, max_throughput_product1_sys1 = mean_confidence_interval(throughput_product1_sys1)

throughput_product2_sys1 = open("./m4_data/throughput_product2_sys1.dat").read().splitlines()
mean_throughput_product2_sys1 = calc_mean_to_string(throughput_product2_sys1)
variance_throughput_product2_sys1 = calc_variance_to_string(throughput_product2_sys1)
confidence_throughput_product2_sys1, min_throughput_product2_sys1, max_throughput_product2_sys1 = mean_confidence_interval(throughput_product2_sys1)

throughput_product3_sys1 = open("./m4_data/throughput_product3_sys1.dat").read().splitlines()
mean_throughput_product3_sys1 = calc_mean_to_string(throughput_product3_sys1)
variance_throughput_product3_sys1 = calc_variance_to_string(throughput_product3_sys1)
confidence_throughput_product3_sys1, min_throughput_product3_sys1, max_throughput_product3_sys1 = mean_confidence_interval(throughput_product3_sys1)

total_throughput_sys1 = open("./m4_data/total_throughput_sys1.dat").read().splitlines()
mean_total_throughput_sys1 = calc_mean_to_string(total_throughput_sys1)
variance_total_throughput_sys1 = calc_variance_to_string(total_throughput_sys1)
confidence_total_throughput_sys1, min_total_throughput_sys1, max_total_throughput_sys1 = mean_confidence_interval(total_throughput_sys1)

# Block time
block_time_inspector1_sys1 = open("./m4_data/block_time_inspector1_sys1.dat").read().splitlines()
mean_block_time_inspector1_sys1 = calc_mean_to_string(block_time_inspector1_sys1)
variance_block_time_inspector1_sys1 = calc_variance_to_string(block_time_inspector1_sys1)
confidence_block_time_inspector1_sys1, min_block_time_inspector1_sys1, max_block_time_inspector1_sys1 = mean_confidence_interval(block_time_inspector1_sys1)

block_time_inspector2_sys1 = open("./m4_data/block_time_inspector2_sys1.dat").read().splitlines()
mean_block_time_inspector2_sys1 = calc_mean_to_string(block_time_inspector2_sys1)
variance_block_time_inspector2_sys1 = calc_variance_to_string(block_time_inspector2_sys1)
confidence_block_time_inspector2_sys1, min_block_time_inspector2_sys1, max_block_time_inspector2_sys1 = mean_confidence_interval(block_time_inspector2_sys1)

total_block_time_sys1 = open("./m4_data/total_block_time_sys1.dat").read().splitlines()
mean_total_block_time_sys1 = calc_mean_to_string(total_block_time_sys1)
variance_total_block_time_sys1 = calc_variance_to_string(total_block_time_sys1)
confidence_total_block_time_sys1, min_total_block_time_sys1, max_total_block_time_sys1 = mean_confidence_interval(total_block_time_sys1)

# SYSTEM TWO
product1_produced_sys2 = open("./m4_data/product1_produced_sys2.dat").read().splitlines()
num_replications_sys2 = len(product1_produced_sys2)
mean_product1_produced_sys2 = calc_mean_to_string(product1_produced_sys2)
variance_product1_produced_sys2 = calc_variance_to_string(product1_produced_sys2)
confidence_product1_produced_sys2, min_confidence_product1_produced_sys2, max_confidence_product1_produced_sys2 = mean_confidence_interval(product1_produced_sys2)

product2_produced_sys2 = open("./m4_data/product2_produced_sys2.dat").read().splitlines()
mean_product2_produced_sys2 = calc_mean_to_string(product2_produced_sys2)
variance_product2_produced_sys2 = calc_variance_to_string(product2_produced_sys2)
confidence_product2_produced_sys2, min_confidence_product2_produced_sys2, max_confidence_product2_produced_sys2 = mean_confidence_interval(product2_produced_sys2)

product3_produced_sys2 = open("./m4_data/product3_produced_sys2.dat").read().splitlines()
mean_product3_produced_sys2 = calc_mean_to_string(product3_produced_sys2)
variance_product3_produced_sys2 = calc_variance_to_string(product3_produced_sys2)
confidence_product3_produced_sys2, min_confidence_product3_produced_sys2, max_confidence_product3_produced_sys2 = mean_confidence_interval(product3_produced_sys2)

total_products_produced_sys2 = open("./m4_data/total_products_produced_sys2.dat").read().splitlines()
mean_total_products_produced_sys2 = calc_mean_to_string(total_products_produced_sys2)
variance_total_products_produced_sys2 = calc_variance_to_string(total_products_produced_sys2)
confidence_total_products_produced_sys2, min_total_products_produced_sys2, max_total_products_produced_sys2 = mean_confidence_interval(total_products_produced_sys2)

# Throughput
throughput_product1_sys2 = open("./m4_data/throughput_product1_sys2.dat").read().splitlines()
mean_throughput_product1_sys2 = calc_mean_to_string(throughput_product1_sys2)
variance_throughput_product1_sys2 = calc_variance_to_string(throughput_product1_sys2)
confidence_throughput_product1_sys2, min_throughput_product1_sys2, max_throughput_product1_sys2 = mean_confidence_interval(throughput_product1_sys2)

throughput_product2_sys2 = open("./m4_data/throughput_product2_sys2.dat").read().splitlines()
mean_throughput_product2_sys2 = calc_mean_to_string(throughput_product2_sys2)
variance_throughput_product2_sys2 = calc_variance_to_string(throughput_product2_sys2)
confidence_throughput_product2_sys2, min_throughput_product2_sys2, max_throughput_product2_sys2 = mean_confidence_interval(throughput_product2_sys2)

throughput_product3_sys2 = open("./m4_data/throughput_product3_sys2.dat").read().splitlines()
mean_throughput_product3_sys2 = calc_mean_to_string(throughput_product3_sys2)
variance_throughput_product3_sys2 = calc_variance_to_string(throughput_product3_sys2)
confidence_throughput_product3_sys2, min_throughput_product3_sys2, max_throughput_product3_sys2 = mean_confidence_interval(throughput_product3_sys2)

total_throughput_sys2 = open("./m4_data/total_throughput_sys2.dat").read().splitlines()
mean_total_throughput_sys2 = calc_mean_to_string(total_throughput_sys2)
variance_total_throughput_sys2 = calc_variance_to_string(total_throughput_sys2)
confidence_total_throughput_sys2, min_total_throughput_sys2, max_total_throughput_sys2 = mean_confidence_interval(total_throughput_sys2)

# Block time
block_time_inspector1_sys2 = open("./m4_data/block_time_inspector1_sys2.dat").read().splitlines()
mean_block_time_inspector1_sys2 = calc_mean_to_string(block_time_inspector1_sys2)
variance_block_time_inspector1_sys2 = calc_variance_to_string(block_time_inspector1_sys2)
confidence_block_time_inspector1_sys2, min_block_time_inspector1_sys2, max_block_time_inspector1_sys2 = mean_confidence_interval(block_time_inspector1_sys2)

block_time_inspector2_sys2 = open("./m4_data/block_time_inspector2_sys2.dat").read().splitlines()
mean_block_time_inspector2_sys2 = calc_mean_to_string(block_time_inspector2_sys2)
variance_block_time_inspector2_sys2 = calc_variance_to_string(block_time_inspector2_sys2)
confidence_block_time_inspector2_sys2, min_block_time_inspector2_sys2, max_block_time_inspector2_sys2 = mean_confidence_interval(block_time_inspector2_sys2)

total_block_time_sys2 = open("./m4_data/total_block_time_sys2.dat").read().splitlines()
mean_total_block_time_sys2 = calc_mean_to_string(total_block_time_sys2)
variance_total_block_time_sys2 = calc_variance_to_string(total_block_time_sys2)
confidence_total_block_time_sys2, min_total_block_time_sys2, max_total_block_time_sys2 = mean_confidence_interval(total_block_time_sys2)

data_file = open("Milestone4FinalComparisonData.dat", "w+")

data_file.write("For system one \n")
data_file.write("Mean product ones produced: " + mean_product1_produced_sys1 + "\n")
data_file.write("Variance: " + variance_product1_produced_sys1 + "\n")
data_file.write("CI [" + min_confidence_product1_produced_sys1 + ", " + max_confidence_product1_produced_sys1 + "] " + "\n")

data_file.write("Mean product twos produced: " + mean_product2_produced_sys1 + "\n")
data_file.write("Variance: " + variance_product2_produced_sys1 + "\n")
data_file.write("CI [" + min_confidence_product2_produced_sys1 + ", " + max_confidence_product2_produced_sys1 + "] " + "\n")

data_file.write("Mean product threes produced: " + mean_product3_produced_sys1 + "\n")
data_file.write("Variance: " + variance_product3_produced_sys1 + "\n")
data_file.write("CI [" + min_confidence_product3_produced_sys1 + ", " + max_confidence_product3_produced_sys1 + "] " + "\n")

data_file.write("Mean total products produced: " + mean_total_products_produced_sys1 + "\n")
data_file.write("Variance: " + variance_total_products_produced_sys1 + "\n")
data_file.write("CI [" + min_total_products_produced_sys1 + ", " + max_total_products_produced_sys1 + "] " + "\n")

data_file.write("Mean throughput for product 1: " + mean_throughput_product1_sys1 + "\n")
data_file.write("Variance: " + variance_throughput_product1_sys1 + "\n")
data_file.write("CI [" + min_throughput_product1_sys1 + ", " + max_throughput_product1_sys1 + "] " + "\n")

data_file.write("Mean throughput for product 2: " + mean_throughput_product2_sys1 + "\n")
data_file.write("Variance: " + variance_throughput_product2_sys1 + "\n")
data_file.write("CI [" + min_throughput_product2_sys1 + ", " + max_throughput_product2_sys1 + "] " + "\n")

data_file.write("Mean throughput for product 3: " + mean_throughput_product3_sys1 + "\n")
data_file.write("Variance: " + variance_throughput_product3_sys1 + "\n")
data_file.write("CI [" + min_throughput_product3_sys1 + ", " + max_throughput_product3_sys1 + "] " + "\n")

data_file.write("Mean total throughput for products: " + mean_total_throughput_sys1 + "\n")
data_file.write("Variance: " + variance_total_throughput_sys1 + "\n")
data_file.write("CI [" + min_total_throughput_sys1 + ", " + max_total_throughput_sys1 + "] " + "\n")

data_file.write("Mean block percentage for inspector 1: " + mean_block_time_inspector1_sys1 + "\n")
data_file.write("Variance: " + variance_block_time_inspector1_sys1 + "\n")
data_file.write("CI [" + min_block_time_inspector1_sys1 + ", " + max_block_time_inspector1_sys1 + "] " + "\n")

data_file.write("Mean block percentage for inspector 2: " + mean_block_time_inspector2_sys1 + "\n")
data_file.write("Variance: " + variance_block_time_inspector2_sys1 + "\n")
data_file.write("CI [" + min_block_time_inspector2_sys1 + ", " + max_block_time_inspector2_sys1 + "] " + "\n")

data_file.write("Mean total block percentage for inspectors: " + mean_total_block_time_sys1 + "\n")
data_file.write("Variance: " + variance_total_block_time_sys1 + "\n")
data_file.write("CI [" + min_total_block_time_sys1 + ", " + max_total_block_time_sys1 + "] " + "\n")

data_file.write("\nFor system two \n")
data_file.write("Mean product ones produced: " + mean_product1_produced_sys2 + "\n")
data_file.write("Variance: " + variance_product1_produced_sys2 + "\n")
data_file.write("CI [" + min_confidence_product1_produced_sys2 + ", " + max_confidence_product1_produced_sys2 + "] " + "\n")

data_file.write("Mean product twos produced: " + mean_product2_produced_sys2 + "\n")
data_file.write("Variance: " + variance_product2_produced_sys2 + "\n")
data_file.write("CI [" + min_confidence_product2_produced_sys2 + ", " + max_confidence_product2_produced_sys2 + "] " + "\n")

data_file.write("Mean product threes produced: " + mean_product3_produced_sys2 + "\n")
data_file.write("Variance: " + variance_product3_produced_sys2 + "\n")
data_file.write("CI [" + min_confidence_product3_produced_sys2 + ", " + max_confidence_product3_produced_sys2 + "] " + "\n")

data_file.write("Mean total products produced: " + mean_total_products_produced_sys2 + "\n")
data_file.write("Variance: " + variance_total_products_produced_sys2 + "\n")
data_file.write("CI [" + min_total_products_produced_sys2 + ", " + max_total_products_produced_sys2 + "] " + "\n")

data_file.write("Mean throughput for product 1: " + mean_throughput_product1_sys2 + "\n")
data_file.write("Variance: " + variance_throughput_product1_sys2 + "\n")
data_file.write("CI [" + min_throughput_product1_sys2 + ", " + max_throughput_product1_sys2 + "] " + "\n")

data_file.write("Mean throughput for product 2: " + mean_throughput_product2_sys2 + "\n")
data_file.write("Variance: " + variance_throughput_product2_sys2 + "\n")
data_file.write("CI [" + min_throughput_product2_sys2 + ", " + max_throughput_product2_sys2 + "] " + "\n")

data_file.write("Mean throughput for product 3: " + mean_throughput_product3_sys2 + "\n")
data_file.write("Variance: " + variance_throughput_product3_sys2 + "\n")
data_file.write("CI [" + min_throughput_product3_sys2 + ", " + max_throughput_product3_sys2 + "] " + "\n")

data_file.write("Mean total throughput for products: " + mean_total_throughput_sys2 + "\n")
data_file.write("Variance: " + variance_total_throughput_sys2 + "\n")
data_file.write("CI [" + min_total_throughput_sys2 + ", " + max_total_throughput_sys2 + "] " + "\n")

data_file.write("Mean block percentage for inspector 1: " + mean_block_time_inspector1_sys2 + "\n")
data_file.write("Variance: " + variance_block_time_inspector1_sys2 + "\n")
data_file.write("CI [" + min_block_time_inspector1_sys2 + ", " + max_block_time_inspector1_sys2 + "] " + "\n")

data_file.write("Mean block percentage for inspector 2: " + mean_block_time_inspector2_sys2 + "\n")
data_file.write("Variance: " + variance_block_time_inspector2_sys2 + "\n")
data_file.write("CI [" + min_block_time_inspector2_sys2 + ", " + max_block_time_inspector2_sys2 + "] " + "\n")

data_file.write("Mean total block percentage for inspectors: " + mean_total_block_time_sys2 + "\n")
data_file.write("Variance: " + variance_total_block_time_sys2 + "\n")
data_file.write("CI [" + min_total_block_time_sys2 + ", " + max_total_block_time_sys2 + "] " + "\n")


# DIFFERENCES
# Products produced
data_file.write("\nDifferences \n")
diff_mean_product1_produced = float(mean_product1_produced_sys1) - float(mean_product1_produced_sys2)
variance_diff_mean_product1_produced = calc_crn_difference_variance(product1_produced_sys1, product1_produced_sys2, float(variance_product1_produced_sys1), float(variance_product1_produced_sys2))
min_diff_product1_produced, max_diff_product1_produced = calc_crn_ci(diff_mean_product1_produced, variance_diff_mean_product1_produced, num_replications_sys1)

diff_mean_product2_produced = float(mean_product2_produced_sys1) - float(mean_product2_produced_sys2)
variance_diff_mean_product2_produced = calc_crn_difference_variance(product2_produced_sys1, product2_produced_sys2, float(variance_product2_produced_sys1), float(variance_product2_produced_sys2))
min_diff_product2_produced, max_diff_product2_produced = calc_crn_ci(diff_mean_product2_produced, variance_diff_mean_product2_produced, num_replications_sys1)

diff_mean_product3_produced = float(mean_product3_produced_sys1) - float(mean_product3_produced_sys2)
variance_diff_mean_product3_produced = calc_crn_difference_variance(product3_produced_sys1, product3_produced_sys2, float(variance_product3_produced_sys1), float(variance_product3_produced_sys2))
min_diff_product3_produced, max_diff_product3_produced = calc_crn_ci(diff_mean_product3_produced, variance_diff_mean_product3_produced, num_replications_sys1)

diff_mean_total_products_produced = float(mean_total_products_produced_sys1) - float(mean_total_products_produced_sys2)
variance_diff_mean_total_products_produced = calc_crn_difference_variance(total_products_produced_sys1, total_products_produced_sys2, float(variance_product3_produced_sys1), float(variance_product3_produced_sys2))
min_diff_total_products_produced, max_diff_total_products_produced = calc_crn_ci(diff_mean_total_products_produced, variance_diff_mean_total_products_produced, num_replications_sys1)

# Throughput
diff_mean_throughput_product1 = float(mean_throughput_product1_sys1) - float(mean_throughput_product1_sys2)
variance_diff_mean_throughput_product1 = calc_crn_difference_variance(throughput_product1_sys1, throughput_product1_sys2, float(variance_throughput_product1_sys1), float(variance_throughput_product1_sys2))
min_diff_throughput_product1, max_diff_throughput_product1 = calc_crn_ci(diff_mean_throughput_product1, variance_diff_mean_throughput_product1, num_replications_sys1)

diff_mean_throughput_product2 = float(mean_throughput_product2_sys1) - float(mean_throughput_product2_sys2)
variance_diff_mean_throughput_product2 = calc_crn_difference_variance(throughput_product2_sys1, throughput_product2_sys2, float(variance_throughput_product2_sys1), float(variance_throughput_product2_sys2))
min_diff_throughput_product2, max_diff_throughput_product2 = calc_crn_ci(diff_mean_throughput_product2, variance_diff_mean_throughput_product2, num_replications_sys1)

diff_mean_throughput_product3 = float(mean_throughput_product3_sys1) - float(mean_throughput_product3_sys2)
variance_diff_mean_throughput_product3 = calc_crn_difference_variance(throughput_product3_sys1, throughput_product3_sys2, float(variance_throughput_product3_sys1), float(variance_throughput_product3_sys2))
min_diff_throughput_product3, max_diff_throughput_product3 = calc_crn_ci(diff_mean_throughput_product3, variance_diff_mean_throughput_product3, num_replications_sys1)

diff_mean_total_throughput = float(mean_total_throughput_sys1) - float(mean_total_throughput_sys2)
variance_diff_mean_total_throughput = calc_crn_difference_variance(total_throughput_sys1, total_throughput_sys2, float(variance_total_throughput_sys1), float(variance_total_throughput_sys2))
min_diff_total_throughput, max_diff_total_throughput = calc_crn_ci(diff_mean_total_throughput, variance_diff_mean_total_throughput, num_replications_sys1)

# Block Percentage
diff_mean_block_time_inspector1 = float(mean_block_time_inspector1_sys1) - float(mean_block_time_inspector1_sys2)
variance_diff_mean_block_time_inspector1 = calc_crn_difference_variance(block_time_inspector1_sys1, block_time_inspector1_sys2, float(variance_block_time_inspector1_sys1), float(variance_block_time_inspector1_sys2))
min_diff_block_time_inspector1, max_diff_block_time_inspector1 = calc_crn_ci(diff_mean_block_time_inspector1, variance_diff_mean_block_time_inspector1, num_replications_sys1)

diff_mean_block_time_inspector2 = float(mean_block_time_inspector2_sys1) - float(mean_block_time_inspector2_sys2)
variance_diff_mean_block_time_inspector2 = calc_crn_difference_variance(block_time_inspector2_sys1, block_time_inspector2_sys2, float(variance_block_time_inspector2_sys1), float(variance_block_time_inspector2_sys2))
min_diff_block_time_inspector2, max_diff_block_time_inspector2 = calc_crn_ci(diff_mean_block_time_inspector2, variance_diff_mean_block_time_inspector2, num_replications_sys1)

diff_mean_total_block_time = float(mean_total_block_time_sys1) - float(mean_total_block_time_sys2)
variance_diff_mean_total_block_time = calc_crn_difference_variance(total_block_time_sys1, total_block_time_sys2, float(variance_total_block_time_sys1), float(variance_total_block_time_sys2))
min_diff_total_block_time, max_diff_total_block_time = calc_crn_ci(diff_mean_total_block_time, variance_diff_mean_total_block_time, num_replications_sys1)

# Products produced
data_file.write("A negative value means system two has a higher mean.\n")
data_file.write("Estimated mean product 1 produced: " + str(diff_mean_product1_produced) + "\n")
data_file.write("Variance: " + variance_diff_mean_product1_produced + "\n")
data_file.write("CI [" + min_diff_product1_produced + ", " + max_diff_product1_produced + "]\n")

data_file.write("Estimated mean product 2 produced: " + str(diff_mean_product2_produced) + "\n")
data_file.write("Variance: " + variance_diff_mean_product2_produced + "\n")
data_file.write("CI [" + min_diff_product2_produced + ", " + max_diff_product2_produced + "]\n")

data_file.write("Estimated mean product 3 produced: " + str(diff_mean_product3_produced) + "\n")
data_file.write("Variance: " + variance_diff_mean_product3_produced + "\n")
data_file.write("CI [" + min_diff_product3_produced + ", " + max_diff_product3_produced + "]\n")

data_file.write("Estimated mean of total products produced: " + str(diff_mean_total_products_produced) + "\n")
data_file.write("Variance: " + variance_diff_mean_total_products_produced + "\n")
data_file.write("CI [" + min_diff_total_products_produced + ", " + max_diff_total_products_produced + "]\n")

# Throughput
data_file.write("Estimated mean throughput of product 1: " + str(diff_mean_throughput_product1) + "\n")
data_file.write("Variance: " + variance_diff_mean_throughput_product1 + "\n")
data_file.write("CI [" + min_diff_throughput_product1 + ", " + max_diff_throughput_product1 + "]\n")

data_file.write("Estimated mean throughput of product 2: " + str(diff_mean_throughput_product2) + "\n")
data_file.write("Variance: " + variance_diff_mean_throughput_product2 + "\n")
data_file.write("CI [" + min_diff_throughput_product2 + ", " + max_diff_throughput_product2 + "]\n")

data_file.write("Estimated mean throughput of product 3: " + str(diff_mean_throughput_product3) + "\n")
data_file.write("Variance: " + variance_diff_mean_throughput_product3 + "\n")
data_file.write("CI [" + min_diff_throughput_product3 + ", " + max_diff_throughput_product3 + "]\n")

data_file.write("Estimated mean of total product throughput: " + str(diff_mean_total_throughput) + "\n")
data_file.write("Variance: " + variance_diff_mean_total_throughput + "\n")
data_file.write("CI [" + min_diff_total_throughput + ", " + max_diff_total_throughput + "]\n")

# Block percentage
data_file.write("Estimated mean block percentage of inspector 1: " + str(diff_mean_block_time_inspector1) + "\n")
data_file.write("Variance: " + variance_diff_mean_block_time_inspector1 + "\n")
data_file.write("CI [" + min_diff_block_time_inspector1 + ", " + max_diff_block_time_inspector1 + "]\n")

data_file.write("Estimated mean block percentage of inspector 2: " + str(diff_mean_block_time_inspector2) + "\n")
data_file.write("Variance: " + variance_diff_mean_block_time_inspector2 + "\n")
data_file.write("CI [" + min_diff_block_time_inspector2 + ", " + max_diff_block_time_inspector2 + "]\n")

data_file.write("Estimated mean total block percentage: " + str(diff_mean_total_block_time) + "\n")
data_file.write("Variance: " + variance_diff_mean_total_block_time + "\n")
data_file.write("CI [" + min_diff_total_block_time + ", " + max_diff_total_block_time + "]\n")

data_file.close()

