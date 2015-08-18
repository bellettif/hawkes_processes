'''
Created on 3 nov. 2013

Mean reverting price model

Heat map of the likelihood for a fixed mu and varying alphas
and betas

@author: francois belletti
'''

from datetime import datetime
from matplotlib import pyplot as plt
from scipy.optimize import minimize as minimize
import numpy as np

import HP_simulator.HP_wrapper as HP_wrapper
import MLE_wrapper

current_time = datetime.now()
current_micro = (current_time.day * 24 * 3600 + current_time.hour * 3600 + current_time.minute * 60 + current_time.second) * 100000 + current_time.microsecond

# Initialize the seed of the pseudo random number generator
HP_wrapper.set_seed(current_micro)

# How many seconds will be simulated
n_seconds =  5 * 7 * 3600

# Parameters of the simulation
dim = 2
exact_mu = 0.20
exact_alpha = 0.025
exact_beta = 0.17
mus = [exact_mu, exact_mu]
alphas = [[0.0, exact_alpha],
          [exact_alpha, 0.0]]
betas = [[0.0, exact_beta],
         [exact_beta, 0.0]]
mus = np.asanyarray(mus, dtype = np.double)
alphas = np.asanyarray(alphas, dtype = np.double)
betas = np.asanyarray(betas, dtype = np.double)

# Run one simulation
example_sim = HP_wrapper.generate_sim(n_seconds, dim, mus, alphas, betas)

# Parse the result
simulation = example_sim['simulation']
current_indices = example_sim['current_indices']

# Wrapper of the likelihood function, it sums the log likelihoods of all dimensions
def get_lk(alpha, beta):
    current_mus = [exact_mu, exact_mu]
    current_alphas = [[0.0, alpha],
                      [alpha, 0.0]]
    current_betas = [[0.0, beta],
                     [exact_beta, 0.0]]
    current_mus  = np.asanyarray(current_mus)
    current_alphas = np.asanyarray(current_alphas)
    current_betas = np.asanyarray(current_betas)
    lk_0 = MLE_wrapper.get_likelihood(simulation,
                                 0,
                                 current_indices,
                                 current_mus,
                                 current_alphas,
                                 current_betas)
    lk_1 = MLE_wrapper.get_likelihood(simulation,
                                 1,
                                 current_indices,
                                 current_mus,
                                 current_alphas,
                                 current_betas)
    return lk_0 + lk_1

# Yet another wrapper
def get_likelihood(params):
    current_mu = exact_mu
    current_alpha = params[0]
    current_beta = params[1]
    current_mus = current_mu * np.ones(dim)
    current_alphas = np.zeros((dim, dim))
    current_alphas[0, 1] = current_alpha
    current_alphas[1, 0] = current_alpha
    current_betas = np.zeros((dim, dim))
    current_betas[0, 1] = current_beta
    current_betas[1, 0] = current_beta
    lk_0 = MLE_wrapper.get_likelihood(simulation,
                                 0,
                                 current_indices,
                                 current_mus,
                                 current_alphas,
                                 current_betas)
    lk_1 = MLE_wrapper.get_likelihood(simulation,
                                 1,
                                 current_indices,
                                 current_mus,
                                 current_alphas,
                                 current_betas)
    result = - lk_1 - lk_0
    return result              
    
# Example of maximum research (we cheat as we use the actual values in the initialization)
# The Nelder-Mead method does not has enough points in its polygon here
mu_0 = 0.13
alpha_0 = 0.015
beta_0 = 0.015
params_0 = [alpha_0, beta_0]

solution = minimize(get_likelihood, params_0, method = 'Nelder-Mead', options = {'ftol' : 1e-10,
                                                                                'xtol' : 1e-10})


print solution.x

# Preparing the heat map
alpha_values = np.linspace(0.005, 0.030, 100) * 10
beta_values = np.linspace(0.05, 0.30, 100)
z = [[get_lk(x * 0.1, y) for x in alpha_values] for y in beta_values]
z = np.asanyarray(z)

alpha_min = min(alpha_values)
alpha_max = max(alpha_values)
beta_min = min(beta_values)
beta_max = max(beta_values)

# Plotting
extent = alpha_min, alpha_max, beta_max, beta_min
p = plt.imshow(z, extent = extent)
fig = plt.gcf()
plt.plot([10 * exact_alpha], [exact_beta], marker = 'x', markersize = 10, mfc = 'k', c = 'white')
plt.ylabel('Beta')
plt.xlabel('10 x alpha')
plt.clim()
plt.savefig('Log-likelihood_heat_map.png')