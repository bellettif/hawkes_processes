'''
Created on 3 nov. 2013

This script computes an histogram of the values simulated
by the mt19937 pseudo random generator.

@author: francois belletti
'''

from matplotlib import pyplot as plt
from datetime import datetime
import rng
import time

# Test of the Mersenne-Twister mt19937

n_sims = 1000000
start_time = time.clock()
now_time = datetime.now()
n_micros = (now_time.day * 24 * 60 * 60 + now_time.second) * 1e6 \
                                                    + now_time.microsecond
temp = rng.gen_array(n_sims, n_micros)
elapsed_time = time.clock() - start_time
print 'Elapsed time %.2f' % (time.clock() - start_time)

plt.hist(temp, bins = 10000)
plt.title('mt19937 rng (%d sims, %.2f secs)' % (n_sims, elapsed_time))
plt.xlabel('genrand_real3')
plt.savefig('Rng_analysis_mt19937.png', dpi = 300)
plt.close()