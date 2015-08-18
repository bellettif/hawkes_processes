'''
Created on 3 nov. 2013

This script simulates a bi-dimensional Self-exciting point process.
It computes the intensities thanks to the Intensity c code and plots them.

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
dim = 2
exact_mu = 0.13
exact_alpha = 0.023
exact_beta = 0.11
mus = [exact_mu, exact_mu]
alphas = [[0.0, exact_alpha],
          [exact_alpha, 0.0]]
betas = [[0.0, exact_beta],
         [exact_beta, 0.0]]
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

# Compute the position of the last jump on the time axis
last_second_0 = simulation[0, current_indices[0] - 1]
last_second_1 = simulation[1, current_indices[1] - 1]
last_second = max(last_second_0, last_second_1)

# Number of points at which the intensity will be computed between
# 0 and last_second
resolution = 1000
target_index = 0

# Computation of the intensity of the first component
targets_0 = np.linspace(0.0, last_second, resolution) # Instants at which the intensity will be computed
jumps_0 = simulation[target_index, :current_indices[target_index]]
intensities_0 = Intensity_wrapper.get_intensities(simulation,
                                         targets_0,
                                         target_index,
                                         current_indices,
                                         mus,
                                         alphas,
                                         betas)

# Computation of the intensity if the second component
target_index = 1
targets_1 = np.linspace(0, last_second, resolution) # Instants at which the intensity will be computed
jumps_1 = simulation[target_index, :current_indices[target_index]]
intensities_1 = Intensity_wrapper.get_intensities(simulation,
                                         targets_1,
                                         target_index,
                                         current_indices,
                                         mus,
                                         alphas,
                                         betas)

# Plotting
gap = 0.1 # Separation between the two components on the plot
plt.plot(targets_0, gap + intensities_0, c = 'r')
plt.plot(jumps_0, gap * np.ones(len(jumps_0)), linestyle = 'None', marker = '^', c = 'r')
plt.plot(targets_1, - gap - intensities_1, c = 'b')
plt.plot(jumps_1, - gap * np.ones(len(jumps_1)), linestyle = 'None', marker = 'v', c = 'b')
plt.title('Mutually exciting dimensions')
plt.xlabel('t')
plt.legend(('Intensity 1', 'Jumps 1', 'Intensity 2', 'Jumps 2'))
fig = plt.gcf()
fig.set_size_inches((12, 8))
plt.savefig('2dimensions.png', dpi = 300)
plt.close()

