'''
Created on 3 nov. 2013

Simulating a 2-dimension constant intensity Poisson Process with Python

@author: francois belletti
'''

import numpy as np
from matplotlib import pyplot as plt

n_seconds = 360

lambda_0 = 0.12
lambda_1 = 0.25

targets_0 = np.random.exponential(1.0 / lambda_0, 100000)
targets_1 = np.random.exponential(1.0 / lambda_1, 100000)

targets_0 = np.cumsum(targets_0)
targets_1 = np.cumsum(targets_1)

jumps_0 = filter((lambda x : x < n_seconds), targets_0)
jumps_1 = filter((lambda x : x < n_seconds), targets_1)

t_axis = np.linspace(0, n_seconds, 100)
intensities_0 = lambda_0 * np.ones(len(t_axis))
intensities_1 = lambda_1 * np.ones(len(t_axis))

gap = 0.1

plt.plot(t_axis, intensities_0, c = 'r')
plt.plot(jumps_0, 0.05 * np.ones(len(jumps_0)), linestyle = 'None', marker = '^', c = 'r')
plt.plot(t_axis, intensities_1, c = 'b')
plt.plot(jumps_1, - 0.05 * np.ones(len(jumps_1)), linestyle = 'None', marker = 'v', c = 'b')
plt.ylim(-0.3, 0.3)
plt.title('2 dimensional Poisson process')
plt.xlabel('t')
plt.legend(('Intensity 1', 'Jumps 1', 'Intensity 2', 'Jumps 2'))
fig = plt.gcf()
fig.set_size_inches((12, 8))
plt.savefig('Poisson2dimensions.png', dpi = 300)
plt.close()