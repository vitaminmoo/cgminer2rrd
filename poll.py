#!/usr/bin/env python

import api
import json
import os
import re
import rrdtool
import sys

def sanitize(key):
    key = re.sub(r'%$', r'_Per', key)
    key = re.sub(r'\W', r'_', key)
    return key

def sanitize_val(key, val):
    if re.match(r'Difficulty ', key):
        return int(val)
    elif key == 'Total MH':
        return int(val * 1000000)
    else:
        return val

def categorize(key):
    if key.endswith('%') or key.endswith(' Percent'):
        return 'GAUGE:20:0:100'
    elif key.endswith(' 5s') or key.endswith(' av'):
        return 'GAUGE:20:U:U'
    elif key.startswith('GPU'):
        return 'GAUGE:20:U:U'
    elif key == 'Work Utility' or key == 'Utility':
        return 'GAUGE:20:0:U'
    elif key == 'Intensity':
        return 'GAUGE:20:8:U'
    elif key == 'Fan Speed' or key == 'Temperature':
        return 'GAUGE:20:0:U'
    elif key == 'Last Share Difficulty':
        return 'GAUGE:20:0:U'
    else:
        return 'COUNTER:20:U:U'

def key_filter(key):
    if key in [
        'Enabled',
        'GPU',
        'Last Share Pool',
        'Last Share Time',
        'Last Valid Work',
        'Status',
    ]:
        return False
    else:
        return True

def get_items(data):
    return dict([(sanitize(_), categorize(_)) for _ in data if key_filter(_)])

def get_data_sources(items):
    return [str('DS:%s:%s' % (_[0:18], items[_])) for _ in sorted(items.keys())]

def get_values(data):
    return [str(sanitize_val(_, data[_])) for _ in sorted(data) if key_filter(_)]

# first do the summary shit
summary = api.summary()

if not os.path.exists('summary.rrd'):
    # create
    items = get_items(summary)
    
    data_sources = get_data_sources(items)
    print "summary bs:"
    print json.dumps(data_sources, indent=2)
    rrdtool.create(
        'summary.rrd',
        '--step', '5',
        data_sources,
        'RRA:AVERAGE:0.5:1:720',     # 1h
        'RRA:AVERAGE:0.5:120:720',   # 1d
        'RRA:AVERAGE:0.5:840:720',   # 7d
        'RRA:AVERAGE:0.5:3600:720',  # 30d
        'RRA:AVERAGE:0.5:43800:720', # 365d
    )
else:
    # update
    items = get_values(summary)
    rrdtool.update('summary.rrd','N:%s' % ':'.join(items))

# now handle each card
devs = api.devs()

# create
for dev in devs:
    rrd = 'dev-%s.rrd' % dev["GPU"]
    if not os.path.exists(rrd):
        items = get_items(dev)
        data_sources = get_data_sources(items)
        print "creating file '%s'" % rrd
        print json.dumps(data_sources, indent=2)
        rrdtool.create(
            rrd,
            '--step', '5',
            data_sources,
            'RRA:AVERAGE:0.5:1:720',     # 1h
            'RRA:AVERAGE:0.5:120:720',   # 1d
            'RRA:AVERAGE:0.5:840:720',   # 7d
            'RRA:AVERAGE:0.5:3600:720',  # 30d
            'RRA:AVERAGE:0.5:43800:720', # 365d
        )
    else:
        # update
        values = get_values(dev)
        rrdtool.update(rrd, 'N:%s' % ':'.join(values))
