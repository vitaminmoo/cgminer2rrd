#!/usr/bin/env python2.7

# Copyright 2013 Setkeh Mkfr
# Copyright 2013 Graham Forest <vitaminmoo@wza.us>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.  See COPYING for more details.

# Original example written by: setkeh <https://github.com/setkeh>
# Thanks to Jezzz for all his Support.
# Updated to be a python library by Graham Forest

import socket
import json

def _linesplit(socket):
    buffer = socket.recv(4096)
    done = False
    while not done:
        more = socket.recv(4096)
        if not more:
            done = True
        else:
            buffer = buffer+more
    if buffer:
        return buffer

def command(command, parameter=None, ip='127.0.0.1', port=4028):
    
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip,int(port)))
    if parameter:
        s.send(json.dumps({"command": command, "parameter": parameter}))
    else:
        s.send(json.dumps({"command": command}))
    
    response = _linesplit(s)
    response = response.replace('\x00','')
    response = json.loads(response)
    s.close()
    return response

def summary():
    response = command('summary')
    if 'SUMMARY' in response:
        return response['SUMMARY'][0]
    elif 'STATUS' in response:
        return response['STATUS'][0]
    else:
        sys.exit(1)

def devs():
    response = command('devs')
    if 'DEVS' in response:
        return response['DEVS']
    elif 'STATUS' in response:
        return response['STATUS'][0]
    else:
        sys.exit(1)
