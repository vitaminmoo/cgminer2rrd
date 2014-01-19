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

class SGMinerError(Exception):
    def __init__(self, response):
        self.message = response['STATUS'][0]['Msg']
        self.status = response['STATUS'][0]['STATUS']
    def __str__(self):
        return '%s: %s' % (self.status, self.message)

class SGMiner():

    def __init__(self, ip='127.0.0.1', port=4028):
        self.ip = ip
        self.port = int(port)

    def _linesplit(self, socket):
        """
        Utility function to handle incoming socket data from API
        """
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
    
    def _is_success(self, response):
        """
        Determine if a response from the API was successful
        """
        if not 'STATUS' in response or \
           not response['STATUS'] or \
           not 'STATUS' in response['STATUS'][0]:
            raise Exception('Unknown error connecting to API at %s:%i' % \
                    (self.ip, self.port))
        return response['STATUS'][0]['STATUS'] in ('S', 'I')
    
    def command(self, command, parameter=None):
        """
        Generic API command handler
        """
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        if parameter:
            s.send(json.dumps({"command": command, "parameter": parameter}))
        else:
            s.send(json.dumps({"command": command}))
        
        response = self._linesplit(s)
        response = response.replace('\x00','')
        response = json.loads(response)
        s.close()
        return response

    def command_safe(self, command, parameter=None):
        """ 
        Handle common case of commands that should except on failure 
        """
        response = self.command(command)
        if not self._is_success(response):
            raise SGMinerError(response)
        return response

    def command_with_reply(self, command, reply, parameter=None):
        """ 
        Handle common case of commands that return named data
        """
        response = self.command_safe(command, parameter=parameter)
        if not reply in response:
            raise Exception("Reply key '%s' not found in returned data: %s" \
                    % (reply, response))
        return response[reply][0] if len(response[reply]) == 1 else response[reply]

    def command_with_caps_reply(self, command, parameter=None):
        """ 
        Handle common case of commands that return data with capitalized name
        """
        return self.command_with_reply(command, reply=command.upper(), parameter=parameter)
        
    def version(self):
        return self.command_with_caps_reply('version')

    def config(self):
        return self.command_with_caps_reply('config')
    
    def summary(self):
        return self.command_with_caps_reply('summary')

    def pools(self):
        return self.command_with_caps_reply('pools')

    def devs(self):
        return self.command_with_caps_reply('devs')

    def gpu(self, number=None):
        return self.command_with_caps_reply('gpu', parameter=number)

    def pga(self, number=None):
        return self.command_with_caps_reply('pga', parameter=number)

    def gpucount(self):
        return self.command_with_reply(command='gpucount', reply='GPUS')

    def pgacount(self):
        return self.command_with_reply(command='pgacount', reply='PGAS')
