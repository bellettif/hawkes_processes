'''
Created on 3 nov. 2013

Wrapping script for the C HP_simulator

Execute python setup.py build_ext --inplace prior in order to compile.

@author: francois belletti
'''

import numpy as np
cimport numpy as np
cimport libc.stdlib
import ctypes

# Maximum number of jumps simulated per component
# If the number is reached, the C code will print a warning
cdef int MAX_POINTS = 50000

# Types for conversion of numpy array to c pointers
# Numpy matrices are considered as one-dimensional c arrays
DTYPE = np.double
ctypedef np.double_t DTYPE_t
ITYPE = np.int32
ctypedef np.int32_t ITYPE_t

# Linking with the c code
cdef extern from "hp_simulator.h":
    void init_exp_genrand(unsigned long seed)
    void next_simulation(double n_seconds,
                         int dim,
                         double * mus,
                         double * alphas,
                         double * betas,
                         int * current_indices,
                         int max_points,
                         double * result)

# Set the seed of the mt19937 pseudo random number generator
def set_seed(seed):
    init_exp_genrand(<unsigned long> seed)

# Generate one simulation
# n_seconds is the total time of the simulation
# dim is the number of components that will be simulated
# mus, alphas and betas are the simulation parameters
#
# The result is a dictionary
# The current_indices field contains the indices needed to trim
# down the simulated jumps. It is 1d np.array of np.int32.
# The jumps can be found in the simulation filed. They are in a 2 dimensional
# numpy array of dimension [dim, MAX_POINTS] of np.double.
#
# n_seconds is a double
# dim is an int
# mus is a 1d numpy array of np.double
# alphas and betas are 2d numpy array of np.double
def generate_sim(n_seconds,
                 dim,
                 np.ndarray mus,
                 np.ndarray alphas,
                 np.ndarray betas):
    cdef int c_dim = <int> dim
    cdef double c_n_seconds = <double> n_seconds
    assert mus.dtype == DTYPE and alphas.dtype == DTYPE and betas.dtype == DTYPE
    cdef np.ndarray[DTYPE_t, ndim = 1, mode = 'c'] c_mus = mus
    cdef np.ndarray[DTYPE_t, ndim = 2, mode = 'c'] c_alphas = np.ascontiguousarray(alphas)
    cdef np.ndarray[DTYPE_t, ndim = 2, mode = 'c'] c_betas = np.ascontiguousarray(betas)
    cdef np.ndarray[DTYPE_t, ndim = 2, mode = 'c'] result = np.ascontiguousarray(np.zeros((dim, MAX_POINTS), dtype = DTYPE))
    cdef np.ndarray[ITYPE_t, ndim = 1, mode = 'c'] current_indices = np.ascontiguousarray(np.zeros(dim, dtype = ITYPE))
    next_simulation(c_n_seconds,
                    c_dim,
                    <double*> c_mus.data,
                    <double*> c_alphas.data,
                    <double*> c_betas.data,
                    <int*> current_indices.data,
                    MAX_POINTS,
                    <double*> result.data)
    return {'current_indices' : current_indices,
            'simulation' : result[:,:max(current_indices)]}