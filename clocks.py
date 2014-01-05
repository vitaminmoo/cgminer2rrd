#!/usr/bin/env python

import time
import os
from itertools import product
import api
import sys

csv='mhs.csv'
card = 1

mem_min = 1250
mem_max = 1500
mem_step = 5
core_min = 780
core_max = 800
core_step = 5

skip = []
try:
    with open(csv, 'r') as output:
        for mem, core, mhz in [_.split(',') for _ in output]:
            skip.append('%s,%s' % (mem,core))
except IOError:
    with open(csv, 'w') as output:
    	output.write('mem,core,mhs')
    pass

with open(csv, 'a') as output:
    for mem, core in product(range(mem_min, mem_max, mem_step), range(core_min, core_max, core_step)):
        if not '%i,%i' % (mem, core) in skip:
            os.system('aticonfig --adapter=all --odsc=%i,%i >/dev/null' % (core,mem))
            time.sleep(15)
            mhs = api.devs()[card]['MHS 5s']
            output.write('%i,%i,%f\n' % (mem, core, mhs))
            output.flush()
            print '%i,%i,%f' % (mem, core, mhs)
            sys.stdout.flush()
