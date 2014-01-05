#!/usr/bin/env python

import time
import os
from itertools import product
import pprint
import api
import sys

mem_min = 1250
mem_max = 1500
mem_step = 5
core_min = 800
core_max = 890
core_step = 5

existing = open('first.csv', 'r')

skip = []
for mem, core, mhz in [_.split(',') for _ in existing]:
    skip.append('%s.%s' % (mem,core))

for mem, core in product(range(mem_min, mem_max, mem_step), range(core_min, core_max, core_step)):
    if not '%i.%i' % (mem, core) in skip:
        os.system('aticonfig --adapter=all --odsc=%i,%i >/dev/null' % (core,mem))
        time.sleep(15)
        mhs = api.devs()[1]['MHS 5s']
        print '%i,%i,%f' % (mem, core, mhs)
        sys.stdout.flush()
