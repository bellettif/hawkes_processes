'''
Created on 3 nov. 2013

This script generates batches of simulations of mean reverting
stock prices modeled with Self-exciting Point Processes.

@author: francois belletti
'''

from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np
import time
import resource

import HP_simulator.HP_wrapper as HP_wrapper
import add_traj_wrapper

current_time = datetime.now()
current_micro = (current_time.day * 24 * 3600 + current_time.hour * 3600 + current_time.minute * 60 + current_time.second) * 100000 + current_time.microsecond

# Initialize the seed of the pseudo random number generator
HP_wrapper.set_seed(current_micro)

# How many seconds will be simulated
n_seconds = 3600

# Parameters of the simulation
dim = 2
mus = [0.13, 0.13]
alphas = [[0.0, 0.023],
          [0.023, 0.0]]
betas = [[0.0, 0.20],
         [0.20, 0.0]]
mus = np.asanyarray(mus, dtype = np.double)
alphas = np.asanyarray(alphas, dtype = np.double)
betas = np.asanyarray(betas, dtype = np.double)

# Reporting of the simulation
n_points = 0
total_time = 0
n_trajs = 10000

# Running the simulation batch
for i in xrange(n_trajs):
    start_point = time.clock()
    example_sim = HP_wrapper.generate_sim(n_seconds, dim, mus, alphas, betas)['simulation']
    total_time += time.clock() - start_point
    minus_traj = example_sim[0,:]
    plus_traj = example_sim[1,:]
    added_trajs = add_traj_wrapper.add_trajectories(minus_traj, plus_traj)
    n_points += len(added_trajs[0,:])
    plt.plot(added_trajs[0,:], 250 + added_trajs[1,:])

print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000.0
print "Took %f seconds, %d jumps" % (time.clock() - start_point, n_points)

# Plotting the batch (can take some time)
plt.title('Simulation batch of %d trajectories, %d jumps, took %.2f seconds' % (n_trajs, n_points, total_time))
plt.ylabel('Price')
plt.xlabel('t')
fig = plt.gcf()
fig.set_size_inches((12, 8))
plt.savefig('Simulation_batch_mean_reverting.png', dpi = 150)
plt.close()

print'Done'