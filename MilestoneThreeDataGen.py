import math
from typing import TextIO

import numpy as np
import matplotlib.pyplot as plt
from statistics import variance
import statsmodels.stats.api as sms


def within_20(array, estimate):
    if (array[0] - estimate) <= (estimate * 0.2):
        if (array[1] - estimate) <= (estimate * 0.2):
            return "yes"
        else:
            return "no"
    else:
        return "no"


##############
# Init. data #
##############
f: TextIO = open("replication_verification.txt", "w+")

init_time = open('initTimes.dat').read().splitlines()
# total_throughput = open('totalThroughput.dat').read().splitlines()
p1_throughput = open('p1Throughput.dat').read().splitlines()
p2_throughput = open('p2Throughput.dat').read().splitlines()
p3_throughput = open('p3Throughput.dat').read().splitlines()
i1_proportion_blocked = open('i1ProportionBlocked.dat').read().splitlines()
i2_proportion_blocked = open('i2ProportionBlocked.dat').read().splitlines()
w1_c1_avg = open('w1_c1_avg.dat').read().splitlines()
w2_c1_avg = open('w2_c1_avg.dat').read().splitlines()
w2_c2_avg = open('w2_c2_avg.dat').read().splitlines()
w3_c1_avg = open('w3_c1_avg.dat').read().splitlines()
w3_c3_avg = open('w3_c3_avg.dat').read().splitlines()

#################
# Program start #
#################
# Convert values from strings to floats
data_init_time = np.array(init_time).astype(np.float)
# data_total_throughput = np.array(total_throughput).astype(np.float)
data_p1_throughput = np.array(p1_throughput).astype(np.float)
data_p2_throughput = np.array(p2_throughput).astype(np.float)
data_p3_throughput = np.array(p3_throughput).astype(np.float)
data_i1_proportion_blocked = np.array(i1_proportion_blocked).astype(np.float)
data_i2_proportion_blocked = np.array(i2_proportion_blocked).astype(np.float)
data_w1_c1_avg = np.array(w1_c1_avg).astype(np.float)
data_w2_c1_avg = np.array(w2_c1_avg).astype(np.float)
data_w2_c2_avg = np.array(w2_c2_avg).astype(np.float)
data_w3_c1_avg = np.array(w3_c1_avg).astype(np.float)
data_w3_c3_avg = np.array(w3_c3_avg).astype(np.float)

mean_p1_throughput = np.mean(data_p1_throughput)
var_p1_throughput = np.var(data_p1_throughput)
sample_var_p1_throughput = variance(data_p1_throughput)
CI95_p1_throughput = sms.DescrStatsW(data_p1_throughput).tconfint_mean()
f.write("p1 throughput mean: " + str(mean_p1_throughput) + "\n")
f.write("p1 throughput variance: " + str(var_p1_throughput) + "\n")
f.write("p1 throughput sample variance: " + str(sample_var_p1_throughput) + "\n")
f.write("p1 throughput 95% confidence interval: " + str(CI95_p1_throughput) + "\n")
f.write(
    "p1 throughput 95% confidence interval does not exceed 20% of estimated value?: " + within_20(CI95_p1_throughput,
                                                                                                  mean_p1_throughput) + "\n")
f.write("\n")

mean_p2_throughput = np.mean(data_p2_throughput)
var_p2_throughput = np.var(data_p2_throughput)
sample_var_p2_throughput = variance(data_p2_throughput)
CI95_p2_throughput = sms.DescrStatsW(data_p2_throughput).tconfint_mean()
f.write("p2 throughput mean: " + str(mean_p2_throughput) + "\n")
f.write("p2 throughput variance: " + str(var_p2_throughput) + "\n")
f.write("p2 throughput sample variance: " + str(sample_var_p2_throughput) + "\n")
f.write("p2 throughput 95% confidence interval: " + str(CI95_p2_throughput) + "\n")
f.write(
    "p2 throughput 95% confidence interval does not exceed 20% of estimated value?: " + within_20(CI95_p2_throughput,
                                                                                                  mean_p2_throughput) + "\n")
f.write("\n")

mean_p3_throughput = np.mean(data_p3_throughput)
var_p3_throughput = np.var(data_p3_throughput)
sample_var_p3_throughput = variance(data_p3_throughput)
CI95_p3_throughput = sms.DescrStatsW(data_p3_throughput).tconfint_mean()
f.write("p3 throughput mean: " + str(mean_p3_throughput) + "\n")
f.write("p3 throughput variance: " + str(var_p3_throughput) + "\n")
f.write("p3 throughput sample variance: " + str(sample_var_p3_throughput) + "\n")
f.write("p3 throughput 95% confidence interval: " + str(CI95_p3_throughput) + "\n")
f.write(
    "p3 throughput 95% confidence interval does not exceed 20% of estimated value?: " + within_20(CI95_p3_throughput,
                                                                                                  mean_p3_throughput) + "\n")
f.write("\n")

mean_i1_proportion_blocked = np.mean(data_i1_proportion_blocked)
var_i1_proportion_blocked = np.var(data_i1_proportion_blocked)
sample_var_i1_proportion_blocked = variance(data_i1_proportion_blocked)
CI95_i1_proportion_blocked = sms.DescrStatsW(data_i1_proportion_blocked).tconfint_mean()
f.write("inspector 1 proportion blocked mean: " + str(mean_i1_proportion_blocked) + "\n")
f.write("inspector 1 proportion blocked variance: " + str(var_i1_proportion_blocked) + "\n")
f.write("inspector 1 proportion blocked sample variance: " + str(sample_var_i1_proportion_blocked) + "\n")
f.write("inspector 1 proportion blocked 95% confidence interval sanity: " + str(CI95_i1_proportion_blocked) + "\n")
# make first CI 0 to prevent errors
x = list(CI95_i1_proportion_blocked)
x[0] = float(0)
CI95_i1_proportion_blocked = x
f.write("inspector 1 proportion blocked 95% confidence interval does not exceed 20% of estimated value?: " + within_20(
    CI95_i1_proportion_blocked, mean_i1_proportion_blocked) + "\n")
f.write("\n")

mean_i2_proportion_blocked = np.mean(data_i2_proportion_blocked)
var_i2_proportion_blocked = np.var(data_i2_proportion_blocked)
sample_var_i2_proportion_blocked = variance(data_i2_proportion_blocked)
CI95_i2_proportion_blocked = sms.DescrStatsW(data_i2_proportion_blocked).tconfint_mean()
f.write("inspector 2 proportion blocked mean: " + str(mean_i2_proportion_blocked) + "\n")
f.write("inspector 2 proportion blocked variance: " + str(var_i2_proportion_blocked) + "\n")
f.write("inspector 2 proportion blocked sample variance: " + str(sample_var_i2_proportion_blocked) + "\n")
f.write("inspector 2 proportion blocked 95% confidence interval: " + str(CI95_i2_proportion_blocked) + "\n")
f.write("inspector 2 proportion blocked 95% confidence interval does not exceed 20% of estimated value?: " + within_20(
    CI95_i2_proportion_blocked, mean_i2_proportion_blocked) + "\n")
f.write("\n")

plt.figure(1)
plt.title("Average Components in w1 c1 Queue vs Initialization Time")
plt.plot(data_init_time, data_w1_c1_avg)
plt.ylabel("Average Components in Queue")
plt.xlabel("Initialization Time")
plt.axis([0, 700, 0, 2])

plt.figure(2)
plt.title("Average Components in w2 c1 Queue vs Initialization Time")
plt.plot(data_init_time, data_w2_c1_avg)
plt.ylabel("Average Components in Queue")
plt.xlabel("Initialization Time")
plt.axis([0, 700, 0, 2])

plt.figure(3)
plt.title("Average Components in w2 c2 Queue vs Initialization Time")
plt.plot(data_init_time, data_w2_c2_avg)
plt.ylabel("Average Components in Queue")
plt.xlabel("Initialization Time")
plt.axis([0, 700, 0, 2])

plt.figure(4)
plt.title("Average Components in w3 c1 Queue vs Initialization Time")
plt.plot(data_init_time, data_w3_c1_avg)
plt.ylabel("Average Components in Queue")
plt.xlabel("Initialization Time")
plt.axis([0, 700, 0, 2])

plt.figure(5)
plt.title("Average Components in w3 c3 Queue vs Initialization Time")
plt.plot(data_init_time, data_w3_c3_avg)
plt.ylabel("Average Components in Queue")
plt.xlabel("Initialization Time")
plt.axis([0, 700, 0, 2])

plt.show()
f.close()
