import numpy as np

seed = 123
np.random.seed(seed)
speed_factor = 1000


def convert_st_mins_to_sim_speed(minutes):
    return minutes * 60 / speed_factor


def sample_service_time(mean):
    sampled_st = np.random.exponential(mean, 1)[0]
    print("Sampled ST: %s", sampled_st)
    return convert_st_mins_to_sim_speed(sampled_st)


for i in range(20):
    sample_service_time(10)

