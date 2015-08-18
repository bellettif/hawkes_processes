'''
Created on 3 nov. 2013

This is the wrapper for the log-likelihood calculator written is C.
This computes the likelihood of a given component of a Self-exciting
point process trajectory.

Execute python setup.py build_ext --inplace prior in order to compile.

@author: francois belletti
'''

import numpy as np
cimport numpy as np
cimport libc.stdlib
import ctypes

# Types for conversion of numpy array to c pointers
DTYPE = np.double
ctypedef np.double_t DTYPE_t
ITYPE = np.int32
ctypedef np.int32_t ITYPE_t

# Linking with the c code
cdef extern from "MLE.h":
    double compute_likelihood(double * simulation,
                           double * mus, double * alphas, double * betas,
                           int dim,
                           int target_index,
                           int * current_indices,
                           int n_points)

# Compute the log-likelihood
# Simulation is the simulated multidimensional trajectory
# Current_indices are the trimming indices of the simualtion
# Mus, alphas and betas are the candidates for the current likelihood
# computation.
#
# simulation is a 2d numpy array of np.double
# target_index is an int
# current_indices is a 1d numpy array of np.int32
# mus is a 1d numpy array of np.double
# alphas and betas are 2d numpy array of np.double
def get_likelihood(np.ndarray simulation, target_index,
                np.ndarray current_indices,
                np.ndarray mus, np.ndarray alphas, np.ndarray betas):
    assert mus.dtype == DTYPE and alphas.dtype == DTYPE and betas.dtype == DTYPE \
        and current_indices.dtype == ITYPE
    dim = len(simulation)
    cdef int c_dim = dim
    n_points = len(simulation[0])
    cdef int c_n_points = n_points
    cdef int c_target_index = target_index
    cdef np.ndarray[DTYPE_t, ndim = 1, mode = 'c'] c_mus = np.ascontiguousarray(mus)
    cdef np.ndarray[DTYPE_t, ndim = 2, mode = 'c'] c_alphas = np.ascontiguousarray(alphas)
    cdef np.ndarray[DTYPE_t, ndim = 2, mode = 'c'] c_betas = np.ascontiguousarray(betas)
    cdef np.ndarray[DTYPE_t, ndim = 2, mode = 'c'] c_simulation = np.ascontiguousarray(simulation)
    cdef np.ndarray[ITYPE_t, ndim = 1, mode = 'c'] c_current_indices = np.ascontiguousarray(current_indices)
    return compute_likelihood(<double*> c_simulation.data,
                    <double*> c_mus.data, <double*> c_alphas.data, <double*> c_betas.data,
                    c_dim, c_target_index,
                    <int*> c_current_indices.data,
                    c_n_points)