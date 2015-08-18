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

sourcefiles = ["HP_wrapper.pyx", "mt19937.c", "hp_simulator.c"]

setup(
      #ext_modules = cythonize("rng.pyx", sources = ["addition.c"], language = "c++", include_dirs = [np.get_include()])
      cmdclass = {'build_ext' : build_ext},
      ext_modules = [Extension("HP_wrapper",
                               sourcefiles,
                               include_dirs = [".", np.get_include()])]
)