#!/usr/bin/env python

import rrdtool
import os

devs = [0,1,2,3]
colors = ['#00B25C','#0A67A3','#FF8E00','#FF4100']

srrd = 'status.rrd'
crrds = ['dev-%i.rrd' % _ for _ in devs]

def cdefs(ds):
    return ['DEF:ds%i=%s:%s:AVERAGE' % (i, crrds[i], ds) for i in devs]
    
def lines(ds):
    return ['LINE1:ds%i%s:Device %i' % (i,colors[i], i) for i in devs]

graphs = [
    {
        'ds': 'Temperature',
        'vertical-label': 'Degrees Celcius',
    },
    {
        'ds': 'Intensity',
        'vertical-label': 'Intensity',
    },
    {
        'ds': 'MHS_5s',
        'vertical-label': 'Hashes/s',
        'lines': lambda x: ['%s:STACK' % _ for _ in lines(x['ds'])],
    },
    {
        'ds': 'Total_MH',
        'vertical-label': 'Hashes/s',
        'lines': lambda x: ['%s:STACK' % _ for _ in lines(x['ds'])],
    },
    {
        'ds': 'Rejected',
        'vertical-label': 'Hashes/s',
    },
    {
        'ds': 'Accepted',
        'vertical-label': 'Hashes/s',
    },
]


for start in [-3600,-86400,-604800,-2592000,-31536000]:
    for graph in graphs:
        file_name = '%s%s.png' % (graph['ds'], start)
        rrdtool.graph(
            '%s.tmp' % file_name,
            '--imgformat', 'PNG',
            '--width', '720',
            '--height', '200',
            '--start', str(start),
            '--end', "-1",
            '--vertical-label', graph['vertical-label'],
            '--title', "Device %s" % graph['ds'],
            graph['cdefs'](graph) if 'cdefs' in graph else cdefs(graph['ds']),
            graph['lines'](graph) if 'lines' in graph else lines(graph['ds']),
        )
        os.rename('%s.tmp' % (file_name), file_name)
