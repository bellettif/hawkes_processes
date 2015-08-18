'''
Created on 3 nov. 2013

Simulating a constant intensity Poisson Process with Python

@author: francois belletti
'''

import numpy as np
from matplotlib import pyplot as plt

n_seconds = 3000

t_axis = np.linspace(0, n_seconds, 100)

lambda_0 = 0.10
targets_0 = np.random.exponential(1.0 / lambda_0, 1000000)
targets_0 = np.cumsum(targets_0)
jumps_0 = filter((lambda x : x < n_seconds), targets_0)
delta_t_0 = np.diff(jumps_0)
intensities_0 = lambda_0 * np.ones(len(t_axis))

lambda_1 = 0.40
targets_1 = np.random.exponential(1.0 / lambda_1, 1000000)
targets_1 = np.cumsum(targets_1)
jumps_1 = filter((lambda x : x < n_seconds), targets_1)
delta_t_1 = np.diff(jumps_1)
intensities_1 = lambda_1 * np.ones(len(t_axis))

plt.subplot(211)
plt.plot(t_axis, intensities_0, c = 'r')
plt.plot(jumps_0, 0.05 * np.ones(len(jumps_0)), linestyle = 'None', marker = '^', c = 'r')
plt.ylim(0, 0.5)
plt.title('Poisson process, %d jumps, %.2f intensity' % (len(jumps_0), lambda_0))
plt.xlabel('t')
plt.legend(('Intensity', 'Jumps'))
plt.subplot(212)
plt.hist(delta_t_0, bins = 100)
plt.title('Time between jumps histogram')
fig = plt.gcf()
fig.set_size_inches((12, 12))
plt.savefig('Poisson1dimension_%.2f.png' % lambda_0, dpi = 300)
plt.close()

plt.subplot(211)
plt.plot(t_axis, intensities_1, c = 'r')
plt.plot(jumps_1, 0.05 * np.ones(len(jumps_1)), linestyle = 'None', marker = '^', c = 'r')
plt.ylim(0, 0.5)
plt.title('Poisson process, %d jumps, %.2f intensity' % (len(jumps_1), lambda_1))
plt.xlabel('t')
plt.legend(('Intensity', 'Jumps'))
plt.subplot(212)
plt.hist(delta_t_1, bins = 100)
plt.title('Time between jumps histogram')
fig = plt.gcf()
fig.set_size_inches((12, 12))
plt.savefig('Poisson1dimension_%.2f.png' % lambda_1, dpi = 300)
plt.close()