'''
Created on 3 nov. 2013

This script simulates a 4-dimensional Self-exciting process.
It computes its intensities thanks to the Intensity c code.
They are then plotted.

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
dim = 4
exact_mu = 0.13
exact_alpha = 0.023
exact_beta = 0.11
mus = [0.10, 0.08, 0.15, 0.01]
alphas = [[0.0, 0.020, 0.011, 0.005],
          [0.010, 0.08, 0.007, 0.012],
          [0.001, 0.018, 0.002, 0.006],
          [0.0, 0.022, 0.012, 0.008]]
betas = [[0.12, 0.24, 0.11, 0.45],
         [0.33, 0.45, 0.57, 0.80],
         [0.22, 0.50, 0.12, 1.80],
         [0.13, 0.42, 0.34, 0.85]]
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

# Compute the last jump
last_second_1 = simulation[0, current_indices[0] - 1]
last_second_2 = simulation[1, current_indices[1] - 1]
last_second_3 = simulation[2, current_indices[2] - 1]
last_second_4 = simulation[3, current_indices[3] - 1]
last_second = max(last_second_1, last_second_2, last_second_3, last_second_3)

# Number of points between 0 and last_second for which the intensities
# will be computed
resolution = 1000

# Compute the intensity of the first component
target_index = 0
targets_1 = np.linspace(0.0, last_second, resolution) # Instants at which the intensity will be computed
jumps_1 = simulation[target_index, :current_indices[target_index]]
intensities_1 = Intensity_wrapper.get_intensities(simulation,
                                         targets_1,
                                         target_index,
                                         current_indices,
                                         mus,
                                         alphas,
                                         betas)

# Compute the intensity of the second component
target_index = 1
targets_2 = np.linspace(0, last_second, resolution)  # Instants at which the intensity will be computed
jumps_2 = simulation[target_index, :current_indices[target_index]]
intensities_2 = Intensity_wrapper.get_intensities(simulation,
                                         targets_2,
                                         target_index,
                                         current_indices,
                                         mus,
                                         alphas,
                                         betas)

# Compute the intensity of the third component
target_index = 2
targets_3 = np.linspace(0, last_second, resolution)  # Instants at which the intensity will be computed
jumps_3 = simulation[target_index, :current_indices[target_index]]
intensities_3 = Intensity_wrapper.get_intensities(simulation,
                                         targets_3,
                                         target_index,
                                         current_indices,
                                         mus,
                                         alphas,
                                         betas)

# Compute the intensity of the fourth component
target_index = 3
targets_4 = np.linspace(0, last_second, resolution) # Instants at which the intensity will be computed
jumps_4 = simulation[target_index, :current_indices[target_index]]
intensities_4 = Intensity_wrapper.get_intensities(simulation,
                                         targets_4,
                                         target_index,
                                         current_indices,
                                         mus,
                                         alphas,
                                         betas)


# Plot the intensity of the first component
plt.plot(targets_1, np.ones(len(targets_1)) * mus[0], linestyle = '--', c = 'b')
plt.plot(targets_1, intensities_1, c = 'b')
plt.plot(jumps_1, np.max(intensities_1) * 1.1 * np.ones(len(jumps_1)), linestyle = 'None', marker = '^', c = 'b')
plt.title('4d dimension, first component')
plt.xlabel('t')
plt.legend(('Intensity 1', 'Jumps 1'))
plt.ylim(0, np.max(intensities_1) * 1.2)
fig = plt.gcf()
fig.set_size_inches((12, 8))
plt.savefig('4dimensions_1.png', dpi = 300)
plt.close()

# Plot the intensity of the second component
plt.plot(targets_2, np.ones(len(targets_2)) * mus[1], linestyle = '--', c = 'g')
plt.plot(targets_2, intensities_2, c = 'g')
plt.plot(jumps_2, np.max(intensities_2) * 1.1 * np.ones(len(jumps_2)), linestyle = 'None', marker = '^', c = 'g')
plt.title('4d dimension, second component')
plt.xlabel('t')
plt.legend(('Intensity 2', 'Jumps 2'))
plt.ylim(0, np.max(intensities_2) * 1.2)
fig = plt.gcf()
fig.set_size_inches((12, 8))
plt.savefig('4dimensions_2.png', dpi = 300)
plt.close()

# Plot the intensity of the third component
plt.plot(targets_3, np.ones(len(targets_3)) * mus[2], linestyle = '--', c = 'r')
plt.plot(targets_3, intensities_3, c = 'r')
plt.plot(jumps_3, np.max(intensities_3) * 1.1 * np.ones(len(jumps_3)), linestyle = 'None', marker = '^', c = 'r')
plt.title('4d dimension, third component')
plt.xlabel('t')
plt.legend(('Intensity 3', 'Jumps 3'))
plt.ylim(0, np.max(intensities_3) * 1.2)
fig = plt.gcf()
fig.set_size_inches((12, 8))
plt.savefig('4dimensions_3.png', dpi = 300)
plt.close()

# Plot the intensity of the fourth component
plt.plot(targets_4, np.ones(len(targets_4)) * mus[3], linestyle = '--', c = 'violet')
plt.plot(targets_4, intensities_4, c = 'violet')
plt.plot(jumps_4, np.max(intensities_4) * 1.1 * np.ones(len(jumps_4)), linestyle = 'None', marker = '^', c = 'violet')
plt.title('4d dimension, fourth component')
plt.xlabel('t')
plt.legend(('Intensity 4', 'Jumps 4'))
plt.ylim(0, np.max(intensities_4) * 1.2)
fig = plt.gcf()
fig.set_size_inches((12, 8))
plt.savefig('4dimensions_4.png', dpi = 300)
plt.close()
