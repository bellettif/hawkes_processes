'''
Created on 3 nov. 2013

This is a wrapper for the c code that takes two jump processes
and computes their difference so as to generate a mean reverting
stock price.

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

# Linking with the c code
cdef extern from "add_traj.h":
    void add_traj(double * minus_traj,
                  double * plus_traj,
                  double * result_ts,
                  double * result_values,
                  int minus_length,
                  int plus_length)

# Compute the difference between two jump processes.
# The difference that will be computed is plus_traj - minus_traj.
# The simulation algorithm we use garanties that no jumps are simultaneous.
# The number of jumps in the result will therefore be the sum of the number
# of jumps in minus_traj and the number of jumps in plus_traj
#
# minus_traj is a 1d np.array of np.double
# plus_traj is a 1d np.array of np.double
#
# The result is a 2d np.array with 2 rows.
# The first row contains the timestamps of the jumps.
# The second row contains the values corresponding to the timestamps
# (cumulative sum of plus_traj - cumulative sum of minus_traj)
#
def add_trajectories(minus_traj, plus_traj):
    minus_traj = filter((lambda x : x > 0), minus_traj)
    plus_traj = filter((lambda x : x > 0), plus_traj)
    minus_traj = np.asarray(minus_traj, dtype = DTYPE)
    plus_traj = np.asarray(plus_traj, dtype = DTYPE)
    minus_length = len(minus_traj)
    plus_length = len(plus_traj)
    assert minus_traj.dtype == DTYPE and plus_traj.dtype == DTYPE
    cdef np.ndarray[DTYPE_t, ndim = 1, mode = 'c'] c_minus_traj = np.ascontiguousarray(minus_traj)
    cdef np.ndarray[DTYPE_t, ndim = 1, mode = 'c'] c_plus_traj = np.ascontiguousarray(plus_traj)
    cdef np.ndarray[DTYPE_t, ndim = 1, mode = 'c'] result_ts = np.ascontiguousarray(np.zeros(minus_length + plus_length), dtype = DTYPE)
    cdef np.ndarray[DTYPE_t, ndim = 1, mode = 'c'] result_values = np.ascontiguousarray(np.zeros(minus_length + plus_length), dtype = DTYPE)
    add_traj(<double *> c_minus_traj.data,
             <double *> c_plus_traj.data,
             <double *> result_ts.data,
             <double *> result_values.data,
             minus_length, plus_length)
    return np.asanyarray([result_ts, result_values])