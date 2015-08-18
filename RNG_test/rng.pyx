'''
Created on 3 nov. 2013

Wrapping class for the mt19937 c code
Execute python setup.py build_ext --inplace prior in order to compile.

@author: francois  belletti
'''

#from libc.stdlib cimport rand
import numpy as np
cimport numpy as np

# Types for conversion of numpy array to c pointers
DTYPE = np.float
ctypedef np.float_t DTYPE_t

# Linking with the c code
cdef extern from "mt19937.h":
    void init_genrand(unsigned long s)
    double genrand_real3()

# Generate an array of n uniformly distributed numbers on (0, 1)
# with the mt19937 Mersenne Twister
def gen_array(n, seed):
    init_genrand(<unsigned long> seed)
    cdef int c_n = n
    cdef np.ndarray h = np.zeros(c_n, dtype = DTYPE)
    cdef DTYPE_t temp
    for i in range(n):
        temp = <DTYPE_t> genrand_real3()# / float(RAND_MAX)
        h[i] = temp
    return h