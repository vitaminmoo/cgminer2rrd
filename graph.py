#!/usr/bin/env python

import rrdtool
import os
import sys
from glob import glob
from itertools import chain, izip

spans = {
    'Hour':  -3600,
    'Day':   -86400,
    'Week':  -604800,
    'Month': -2592000,
    'Year':  -31536000,
}

colors = ['#00B25C','#0A67A3','#FF8E00','#FF4100']
devs = range(len(glob('dev-*.rrd')))
crrds = ['dev-%i.rrd' % _ for _ in devs]
srrd = 'status.rrd'

def cdefs(ds):
    return ['DEF:ds%i=%s:%s:AVERAGE' % (i, crrds[i], ds) for i in devs]

def vdefs(ds):
    return ['VDEF:ds%iavg=ds%i,AVERAGE' % (i, i) for i in devs]
    
def lines(ds):
    return ['LINE1:ds%i%s:Device %i' % (i,colors[i], i) for i in devs]

def prints(ds):
    return ['GPRINT:ds%iavg:%%6.2lf%%S AVERAGE\l' % (i) for i in devs]


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
    {
        'ds': 'Fan_Speed',
        'vertical-label': 'RPM',
    },
    {
        'ds': 'Utility',
        'vertical-label': 'Utility',
    },
]


for span, start in spans.iteritems():
    for graph in graphs:
        file_name = '%s_%s.png' % (graph['ds'], span)

        rrdtool.graph(
            '%s.tmp' % file_name,
            '--imgformat', 'PNG',
            '--width', '720',
            '--height', '200',
            '--start', str(start),
            '--end', "-1",
            '--vertical-label', graph['vertical-label'],
            '--title', "Device %s - 1 %s" % (graph['ds'], span),
            graph['cdefs'](graph) if 'cdefs' in graph else cdefs(graph['ds']),
            graph['vdefs'](graph) if 'vdefs' in graph else vdefs(graph['ds']),
            list(chain.from_iterable(izip(
                graph['lines'](graph) if 'lines' in graph else lines(graph['ds']),
                graph['prints'](graph) if 'prints' in graph else prints(graph['ds'])
            )))
        )
        os.rename('%s.tmp' % (file_name), file_name)
