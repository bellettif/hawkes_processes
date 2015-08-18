'''
Created on 3 nov. 2013

This script generates one simulation of mean reverting
stock prices modeled with Self-exciting Point Processes.

The value between two consecutive jumps is computed as the last
observed price.

@author: francois belletti
'''

from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np
import time
import resource

import HP_simulator.HP_wrapper as HP_wrapper
import add_traj_wrapper

# This function computes the price between two jumps as 
# the last observation carried forward (locf)
def locf(time_grid, values, target_time_grid):
    result = np.ones(len(target_time_grid))
    result[0] = values[0]
    last_value = values[0]
    last_index = 0
    for i in range(len(result)):
        for j in range(last_index, len(time_grid)):
            if time_grid[j] > target_time_grid[i]:
                last_index = j
                break
            last_value = values[j]
        result[i] = last_value
    return {'time_grid' : target_time_grid,
            'values' : result}

current_time = datetime.now()
current_micro = (current_time.day * 24 * 3600 + current_time.hour * 3600 + current_time.minute * 60 + current_time.second) * 100000 + current_time.microsecond

# Initialize the seed of the pseudo random number generator
HP_wrapper.set_seed(current_micro)

# How many seconds will be simulated
n_seconds = 1200

# Parameters of the simulation
mu = 0.17
alpha = 0.011
beta = 0.04
dim = 2
mus = [mu, mu]
alphas = [[0.0, alpha],
          [alpha, 0.0]]
betas = [[0.0, beta],
         [beta, 0.0]]
mus = np.asanyarray(mus, dtype = np.double)
alphas = np.asanyarray(alphas, dtype = np.double)
betas = np.asanyarray(betas, dtype = np.double)

# Running the simulation
example_sim = HP_wrapper.generate_sim(n_seconds, dim, mus, alphas, betas)['simulation']
minus_traj = example_sim[0,:]
plus_traj = example_sim[1,:]
added_trajs = add_traj_wrapper.add_trajectories(minus_traj, plus_traj)
target_time_grid = np.linspace(0, np.max(added_trajs[0,:]), 1000)
locf_result = locf(added_trajs[0,:], added_trajs[1,:], target_time_grid)
time_grid = locf_result['time_grid']
values = locf_result['values']

# Plotting
plt.title('Mean reverting price, mu = %.2f, alpha = %.2f, beta = %.2f' % (mu, alpha, beta))
plt.ylabel('Price')
plt.xlabel('t')
plt.plot(time_grid, 80 + values)
fig = plt.gcf()
fig.set_size_inches((12, 8))
plt.savefig('Mean_reverting_price_locf_%.2f_%.2f_%2.f.png' % (mu, alpha, beta), dpi = 300)
plt.close()

print'Done'