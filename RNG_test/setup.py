'''
Created on 3 nov. 2013

compile with command line 
python setup.py build_ext --inplace

@author: francois belletti
'''

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy as np

sourcefiles = ["rng.pyx", "mt19937.c"]

setup(
      cmdclass = {'build_ext' : build_ext},
      ext_modules = [Extension("rng", sourcefiles, include_dirs = [np.get_include()])],
)