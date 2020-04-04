import matplotlib.pyplot as plt
import numpy as np
from Type import Type

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
num_times_in_queue_samples = {
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
sim_speed_factor = 10000


def _convert_to_mins(seconds):
    return seconds / 60


def convert_to_sim_mins(irl_seconds):
    return _convert_to_mins(irl_seconds) * sim_speed_factor


def avg(lst):
    return sum(lst) / len(lst)


def generate_data(sizes_file_name, times_file_name):
    time_data = open(times_file_name).read().splitlines()
    wc_times = np.array(time_data).astype(np.float)
    wc_times = list(map(convert_to_sim_mins, wc_times))
    wc_size_data = open(sizes_file_name).read().splitlines()
    wc_sizes = np.array(wc_size_data).astype(np.float)
    running_avgs = []
    temp_array_of_data = []
    for size in wc_sizes:
        temp_array_of_data.append(size)
        running_avgs.append(avg(temp_array_of_data))

    dupe_wc_times = [wc_times[0]]
    skip_first = True
    for time in wc_times:
        if skip_first:
            skip_first = not skip_first
            continue
        dupe_wc_times.append(time-0.1)
        dupe_wc_times.append(time)
    dupe_wc_sizes = []
    for index in range(len(wc_sizes)):
        dupe_wc_sizes.append(wc_sizes[index])
        dupe_wc_sizes.append(wc_sizes[index])
    dupe_wc_sizes.pop()
    return wc_times, dupe_wc_times, dupe_wc_sizes, running_avgs


w1_c1_times, dupe_w1_c1_times, dupe_w1_c1_sizes, w1_c1_running_avgs = generate_data("Type.ONEType.ONE-buffer-sizes.txt", "Type.ONEType.ONE-buffer-size-times.txt")
w2_c1_times, dupe_w2_c1_times, dupe_w2_c1_sizes, w2_c1_running_avgs = generate_data("Type.TWOType.ONE-buffer-sizes.txt", "Type.TWOType.ONE-buffer-size-times.txt")
w2_c2_times, dupe_w2_c2_times, dupe_w2_c2_sizes, w2_c2_running_avgs = generate_data("Type.TWOType.TWO-buffer-sizes.txt", "Type.TWOType.TWO-buffer-size-times.txt")
w3_c1_times, dupe_w3_c1_times, dupe_w3_c1_sizes, w3_c1_running_avgs = generate_data("Type.THREEType.ONE-buffer-sizes.txt", "Type.THREEType.ONE-buffer-size-times.txt")
w3_c3_times, dupe_w3_c3_times, dupe_w3_c3_sizes, w3_c3_running_avgs = generate_data("Type.THREEType.THREE-buffer-sizes.txt", "Type.THREEType.THREE-buffer-size-times.txt")

plt.figure(1, figsize=(20, 10))
plt.ylim(ymax=2.1, ymin=0.0)
plt.title("Components in Workstation 1 Queue 1 vs Time")
plt.plot(dupe_w1_c1_times, dupe_w1_c1_sizes)
plt.ylabel("Components in Queue")
plt.xlabel("Time in Minutes")

plt.figure(2, figsize=(20, 10))
plt.ylim(ymax=2.1, ymin=0.0)
plt.title("Average Components in Workstation 1 Queue 1 vs Time")
plt.plot(w1_c1_times, w1_c1_running_avgs)
plt.ylabel("Average Components in Queue")
plt.xlabel("Time in Minutes")

plt.figure(3, figsize=(20, 10))
plt.ylim(ymax=2.1, ymin=0.0)
plt.title("Components in Workstation 2 Queue 1 vs Time")
plt.plot(dupe_w2_c1_times, dupe_w2_c1_sizes)
plt.ylabel("Components in Queue")
plt.xlabel("Time in Minutes")

plt.figure(4, figsize=(20, 10))
plt.ylim(ymax=2.1, ymin=0.0)
plt.title("Average Components in Workstation 2 Queue 1 vs Time")
plt.plot(w2_c1_times, w2_c1_running_avgs)
plt.ylabel("Average Components in Queue")
plt.xlabel("Time in Minutes")

plt.figure(5, figsize=(20, 10))
plt.ylim(ymax=2.1, ymin=0.0)
plt.title("Components in Workstation 2 Queue 2 vs Time")
plt.plot(dupe_w2_c2_times, dupe_w2_c2_sizes)
plt.ylabel("Components in Queue")
plt.xlabel("Time in Minutes")

plt.figure(6, figsize=(20, 10))
plt.ylim(ymax=2.1, ymin=0.0)
plt.title("Average Components in Workstation 2 Queue 2 vs Time")
plt.plot(w2_c2_times, w2_c2_running_avgs)
plt.ylabel("Average Components in Queue")
plt.xlabel("Time in Minutes")

plt.figure(7, figsize=(20, 10))
plt.ylim(ymax=2.1, ymin=0.0)
plt.title("Components in Workstation 3 Queue 1 vs Time")
plt.plot(dupe_w3_c1_times, dupe_w3_c1_sizes)
plt.ylabel("Components in Queue")
plt.xlabel("Time in Minutes")

plt.figure(8, figsize=(20, 10))
plt.ylim(ymax=2.1, ymin=0.0)
plt.title("Average Components in Workstation 3 Queue 1 vs Time")
plt.plot(w3_c1_times, w3_c1_running_avgs)
plt.ylabel("Average Components in Queue")
plt.xlabel("Time in Minutes")

plt.figure(9, figsize=(20, 10))
plt.ylim(ymax=2.1, ymin=0.0)
plt.title("Components in Workstation 3 Queue/Component 3 vs Time")
plt.plot(dupe_w3_c3_times, dupe_w3_c3_sizes)
plt.ylabel("Components in Queue")
plt.xlabel("Time in Minutes")

plt.figure(10, figsize=(20, 10))
plt.ylim(ymax=2.1, ymin=0.0)
plt.title("Average Components in Workstation 3 Queue/Component 3 vs Time")
plt.plot(w3_c3_times, w3_c3_running_avgs)
plt.ylabel("Average Components in Queue")
plt.xlabel("Time in Minutes")

plt.show()