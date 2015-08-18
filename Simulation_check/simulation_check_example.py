'''
Created on 3 nov. 2013

Example of simulation verification with a QQ plot

@author: francois belletti
'''

from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np

import HP_simulator.HP_wrapper as HP_wrapper
import lambdas_wrapper

# We initialize the simulator
current_time = datetime.now()
current_micro = (current_time.day * 24 * 3600 + current_time.hour * 3600 + current_time.minute * 60 + current_time.second) * 100000 + current_time.microsecond
HP_wrapper.set_seed(current_micro)

# Simulation parameters
n_seconds = 3600
dim = 2
mus = [0.12, 0.13]
alphas = [[0.0, 0.018],
          [0.021, 0.0]]
betas = [[0.00, 0.11],
         [0.15, 0.00]]
mus = np.asanyarray(mus, dtype = np.double)
alphas = np.asanyarray(alphas, dtype = np.double)
betas = np.asanyarray(betas, dtype = np.double)

# We generate a batch of 100 trajectories and plot
for i in xrange(100):
    example_sim = HP_wrapper.generate_sim(n_seconds, dim, mus, alphas, betas)
    simulation = example_sim['simulation']
    current_indices = example_sim['current_indices']
    target_index = 0
    lambdas = lambdas_wrapper.get_lambdas(simulation,
                                          target_index,
                                          current_indices,
                                          mus,
                                          alphas,
                                          betas)
    target_percentiles = np.linspace(1, 99, 100)
    theoretical_percentiles = - np.log(1.0 - target_percentiles * 0.01)
    empirical_percentiles = np.asarray([np.percentile(lambdas, x) for x in target_percentiles])
    plt.plot(theoretical_percentiles, empirical_percentiles, linestyle = 'None', marker = 'x', color = 'r')
    
plt.plot(theoretical_percentiles, theoretical_percentiles)
plt.title('QQ plot of normalized durations')
plt.ylabel('Empirical percentiles')
plt.xlabel('Theoretical percentiles')
fig = plt.gcf()
fig.set_size_inches((12, 8))
plt.savefig('QQ_plot_check.png', dpi = 300)

print'Done'