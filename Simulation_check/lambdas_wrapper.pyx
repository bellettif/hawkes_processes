'''
Created on 3 nov. 2013

This wrapper is dedicated to the computation of the normalized times
for self-exciting point processes.
The core of the computation is done with C code in lambdas.c
Execute python setup.py build_ext --inplace prior in order to compile.

@author: francois belletti
'''

import numpy as np
cimport numpy as np
cimport libc.stdlib
import ctypes

# Types for conversion of numpy array to c pointers
# Numpy matrices are considered as one-dimensional c arrays
DTYPE = np.double
ctypedef np.double_t DTYPE_t
ITYPE = np.int32
ctypedef np.int32_t ITYPE_t

# Linking with the c code
cdef extern from "lambdas.h":
    void compute_lambdas(double * simulation, double * lambda_result,
                         double * mus, double * alphas, double * betas,
                         int dim,
                         int target_index,
                         int * current_indices,
                         int n_points)

# Simulation contains the 2 dimensional numpy array of simulated jumps
# Target_index is the index of the component for which the normalized
# durations between consecutive jumps will be computed.
# Current indices are the indices of the last jumps of the multidimensional
# process.
# Mus, alphas and betas should be the parameters used for the simulation.
def get_lambdas(np.ndarray simulation, target_index,
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
    cdef np.ndarray[DTYPE_t, ndim = 1, mode = 'c'] result_lambdas = np.ascontiguousarray(np.zeros(n_points - 1, dtype = DTYPE))
    compute_lambdas(<double*> c_simulation.data, <double*> result_lambdas.data,
                    <double*> c_mus.data, <double*> c_alphas.data, <double*> c_betas.data,
                    c_dim, c_target_index,
                    <int*> c_current_indices.data,
                    c_n_points)
    return result_lambdas[:current_indices[target_index]]