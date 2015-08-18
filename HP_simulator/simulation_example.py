'''
Created on 3 nov. 2013

Example of Self-exciting Point Process simulation

@author: francois belletti
'''

from datetime import datetime
import numpy as np

import HP_wrapper

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
betas = [[0.0, 0.11],
         [0.11, 0.0]]
mus = np.asanyarray(mus, dtype = np.double)
alphas = np.asanyarray(alphas, dtype = np.double)
betas = np.asanyarray(betas, dtype = np.double)

# Run one simulation
example_sim = HP_wrapper.generate_sim(n_seconds, dim, mus, alphas, betas)

# Parse the result
simulation = example_sim['simulation'] # Bi-dimensional array of jumps (trim with current_indices)
current_indices = example_sim['current_indices'] # Last indices of valid jumps

print 'Simulation result (untrimmed)'
print simulation
print '\n'

print 'Trimming indices'
print current_indices
print '\n'

print 'Trimmed simulation'
for i in range(len(simulation)):
    print 'Beginning of component %d' % i
    print simulation[i,:current_indices[i]][:10]
    print 'End of component %d ' % i
    print simulation[i,:current_indices[i]][-10:]
    print '\n'

print'Done'