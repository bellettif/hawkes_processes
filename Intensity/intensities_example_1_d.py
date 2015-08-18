'''
Created on 3 nov. 2013

This script simulates a one-dimensional Self-exciting process.
It computes its intensity thanks to the Intensity c code.
It then plots it.

@author: francois belletti
'''

from datetime import datetime
from matplotlib import pyplot as plt
from scipy.optimize import minimize as minimize
import numpy as np

import HP_simulator.HP_wrapper as HP_wrapper
import Intensity_wrapper

current_time = datetime.now()
current_micro = (current_time.day * 24 * 3600 + current_time.hour * 3600 + current_time.minute * 60 + current_time.second) * 100000 + current_time.microsecond

# Initialize the seed of the pseudo random number generator
HP_wrapper.set_seed(current_micro)

# How many seconds will be simulated
n_seconds = 360

# Parameters of the simulation
dim = 1
exact_mu = 0.13
exact_alpha = 0.023
exact_beta = 0.11
mus = [exact_mu]
alphas = [[exact_alpha]]
betas = [[exact_beta]]
mus = np.asanyarray(mus, dtype = np.double)
alphas = np.asanyarray(alphas, dtype = np.double)
betas = np.asanyarray(betas, dtype = np.double)

# Run the simulation
example_sim = HP_wrapper.generate_sim(n_seconds, dim, mus, alphas, betas)

# Extract the result
simulation = example_sim['simulation'] # Bi-dimensional array of jumps (trim with current_indices)
current_indices = example_sim['current_indices'] # Last indices of valid jumps

# Print the number of jumps of each component
print current_indices

# Compute the intensity of the first component
last_second_0 = simulation[0, current_indices[0] - 1] # Trimming
last_second = last_second_0
resolution = 1000
target_index = 0
targets_0 = np.linspace(0.0, last_second, resolution) # Instants at which the intensity will be computed
jumps_0 = simulation[target_index, :current_indices[target_index]] # Trimming
intensities_0 = Intensity_wrapper.get_intensities(simulation,
                                         targets_0,
                                         target_index,
                                         current_indices,
                                         mus,
                                         alphas,
                                         betas)

# Plot the intensity and the jumps
plt.plot(targets_0, exact_mu * np.ones(len(targets_0)), c = 'b', linestyle = '--')
plt.plot(targets_0, intensities_0, c = 'g')
plt.plot(jumps_0, 0.35 * np.ones(len(jumps_0)), linestyle = 'None', marker = '^', c = 'g')
plt.title('Self-exciting Point Process')
plt.xlabel('t')
plt.legend(('Constant mu', 'Intensity', 'Jumps'))
plt.ylim(0, 0.4)
fig = plt.gcf()
fig.set_size_inches((12, 8))
plt.savefig('1dimension.png', dpi = 300)
plt.close()

