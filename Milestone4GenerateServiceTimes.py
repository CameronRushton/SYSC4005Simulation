# This file is used to generate service times to be used across multiple different implementations of the simulation
import Controller as ctrl
import numpy as np

# TODO: since this depends on the controller variables, it starts running ctrl code. I need to move the variables to another file

np.random.seed(ctrl.seed)
c1 = open(ctrl.c1_st_file_name, "w+")
c2 = open(ctrl.c2_st_file_name, "w+")
c3 = open(ctrl.c3_st_file_name, "w+")
w1 = open(ctrl.w1_st_file_name, "w+")
w2 = open(ctrl.w2_st_file_name, "w+")
w3 = open(ctrl.w3_st_file_name, "w+")
files = [c1, c2, c3, w1, w2, w3]
means = [ctrl.mean_component1_service_time, ctrl.mean_component2_service_time, ctrl.mean_component3_service_time,
         ctrl.mean_workstation1_service_time, ctrl.mean_workstation2_service_time, ctrl.mean_workstation3_service_time]
for index, file in enumerate(files):
    for i in range(300):
        file.write(str(ctrl.convert_st_mins_to_sim_speed(np.random.exponential(means[index], 1)[0])) + "\n")
