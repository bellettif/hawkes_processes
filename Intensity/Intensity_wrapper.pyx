'''
Created on 3 nov. 2013

This wrapper computes the intensity of a simulated process.
It wraps the Intensity C code.

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
cdef extern from "Intensity.h":
    void compute_intensities(double * simulation,
                               double * targets,
                               double * result,
                               double * mus, double * alphas, double * betas,
                               int dim,
                               int target_index,
                               int * current_indices,
                               int n_points,
                               int n_targets)

# Compute the intensity of simulation (multi-dimensional process)
# for the component of index target_index
# Current_indices are the trimming indices of the simulation
# Mus, alphas and betas are the simulation parameters
#
# The targets are the instants at which the intensity should be computed
#
# The result is a numpy array containing the intensity of the target_index component
#
# simulation is a 2d numpy array of np.double
# targets is a 1d numpy array of np.double
# target_index is an int
# current_indices is a 1d numpy array of np.int32
# mus is a 1d numpy array of np.double
# alphas and betas are 2d numpy array of np.double
def get_intensities(np.ndarray simulation,
                   np.ndarray targets,
                   target_index,
                   np.ndarray current_indices,
                   np.ndarray mus, np.ndarray alphas, np.ndarray betas):
    assert mus.dtype == DTYPE and alphas.dtype == DTYPE and betas.dtype == DTYPE \
        and current_indices.dtype == ITYPE
    dim = len(simulation)
    cdef int c_dim = dim
    n_points = len(simulation[0])
    cdef int c_n_points = n_points
    cdef int c_n_targets = len(targets)
    cdef int c_target_index = target_index
    cdef np.ndarray[DTYPE_t, ndim = 1, mode = 'c'] c_mus = np.ascontiguousarray(mus)
    cdef np.ndarray[DTYPE_t, ndim = 2, mode = 'c'] c_alphas = np.ascontiguousarray(alphas)
    cdef np.ndarray[DTYPE_t, ndim = 2, mode = 'c'] c_betas = np.ascontiguousarray(betas)
    cdef np.ndarray[DTYPE_t, ndim = 2, mode = 'c'] c_simulation = np.ascontiguousarray(simulation)
    cdef np.ndarray[DTYPE_t, ndim = 1, mode = 'c'] c_targets = np.ascontiguousarray(targets)
    cdef np.ndarray[DTYPE_t, ndim = 1, mode = 'c'] c_results = np.ascontiguousarray(np.zeros(c_n_targets, dtype = DTYPE))
    cdef np.ndarray[ITYPE_t, ndim = 1, mode = 'c'] c_current_indices = np.ascontiguousarray(current_indices)
    compute_intensities(<double*> c_simulation.data,
                              <double*> c_targets.data,
                              <double*> c_results.data,
                              <double*> c_mus.data, <double*> c_alphas.data, <double*> c_betas.data,
                              c_dim, c_target_index,
                              <int*> c_current_indices.data,
                              c_n_points,
                              c_n_targets)
    return c_results;