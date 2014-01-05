#!/usr/bin/env python

import time
import os
from itertools import product
import api
import sys

csv='mhs.csv'
card = 0

mem_min = 1250
mem_max = 1500
mem_step = 5
core_min = 780
core_max = 800
core_step = 5
desired_accuracy_in_mhs = 0.001
infinity = 1.0e24

import numpy as np
import scipy as sp
import scipy.stats

def mean_confidence(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    if n == 0:
      print "infinity"
      return infinity
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    print "h: " + str(h)
    return h



skip = []
try:
    with open(csv, 'r') as output:
        for mem, core, mhz in [_.split(',') for _ in output]:
            skip.append('%s,%s' % (mem,core))
except IOError:
    with open(csv, 'w') as output:
    	output.write('mem,core,mhs\n')
    pass

with open(csv, 'a') as output:
    for mem, core in product(range(mem_min, mem_max, mem_step), range(core_min, core_max, core_step)):
        if not '%i,%i' % (mem, core) in skip:
            os.system('aticonfig --adapter=all --odsc=%i,%i >/dev/null' % (core,mem))
            samples = []
            while len(samples) < 3 and mean_confidence(samples) > desired_accuracy_in_mhs:
              time.sleep(5)
              sample = api.devs()[card]['MHS 5s']
              samples.extend([sample])
              print samples
            mhs = np.mean(np.array(samples))
            output.write('%i,%i,%f\n' % (mem, core, mhs))
            output.flush()
            print '%i,%i,%f' % (mem, core, mhs)
            sys.stdout.flush()
