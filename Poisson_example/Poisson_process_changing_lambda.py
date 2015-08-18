'''
Created on 3 nov. 2013

Simulating a constant intensity Poisson Process with Python.
Lambda varies deterministically with t.

@author: francois belletti
'''

import numpy as np
from matplotlib import pyplot as plt



def lambda_t(a, b, t):
    return a*t + b
    
def generate_jumps(T, a, b):
    current_t = 0
    jumps = []
    while(current_t < T):
        capping_lambda = lambda_t(a, b, current_t)
        next_jump = np.random.exponential(1.0 / capping_lambda)
        current_t += next_jump
        current_lambda = lambda_t(a, b, current_t)
        if(np.random.random() < current_lambda / capping_lambda):
            jumps.append(current_t)
        capping_lambda = current_lambda
    jumps = np.asarray(jumps)
    return jumps

n_seconds = 3000

t_axis = np.linspace(0, n_seconds, 100)

lambda_0 = 0.50
decrease_rate = 0.00016
jumps_0 = generate_jumps(n_seconds, -decrease_rate, lambda_0)
intensities_0 = [lambda_t(-decrease_rate, lambda_0, x) for x in t_axis]

plt.plot(t_axis, intensities_0, c = 'r')
plt.plot(jumps_0, 0.05 * np.ones(len(jumps_0)), linestyle = 'None', marker = '^', c = 'r')
plt.ylim(0, 0.5)
plt.title('Poisson process, %d jumps, deterministic intensity' % len(jumps_0))
plt.xlabel('t')
plt.legend(('Intensity', 'Jumps'))
fig = plt.gcf()
fig.set_size_inches((12, 8))
plt.savefig('PoissonAffineLambda.png', dpi = 300)
plt.close()