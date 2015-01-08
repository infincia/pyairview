#!/usr/bin/env python

from __future__ import print_function, division


""" Airview2 "fuzzer" (more of a random tester, we're not looking for bugs just APIs)

    Copyright 2015 Infincia LLC
    
    See LICENSE file for license information
    
	Usage:  Install the libraries in requirements.txt, then run this script.
    
            It sends every possible 6-digit [a-z] command to the device, checking 
            for a response and recording the results as it goes. 
            
            At the end of testing, the results are printed on the terminal.
            
            This script explicitly ignores the 'bs' command because it is both
            already known, and it initiates a stream response that requires 
            proper handling of the response, rather than a single response which
            is what we're testing for anyway to discover other commands.
            
            NOTE: itertools is currently NOT generating every possible permutation
            of the [a-z] character set, for instance it misses 'init' which is a
            known command. I'm investigating the reason.

"""

__author__ = 'Stephen Oliver'
__maintainer__ = 'Stephen Oliver <steve@infincia.com>'
__version__ = '0.1-prerelease'
__license__ = 'MIT'

import platform
import sys
import logging
import logging.handlers
import itertools


import libairview as airview




log = logging.getLogger()
mainHandler = logging.StreamHandler()
log.setLevel(logging.INFO)
mainHandler.setFormatter(logging.Formatter('%(levelname)s %(asctime)s - %(module)s - %(funcName)s: %(message)s'))
log.addHandler(mainHandler)



if __name__ == '__main__':
    log.info('Starting Airview API Fuzzer')
    system_name = platform.system()
    logging.info('Running on: %s' % system_name)
    if system_name == 'Linux':
        port = '/dev/ttyACM0' # arbitrary, need a way to detect/configure
    elif system_name == 'Darwin': # OS X
        port = '/dev/tty.usbmodem411' # this seems arbitrary too, but consistent
    else:
        """
                Note: Need to find out what the device name will be on FreeBSD 
                and others, but this is just the command discovery automator, the 
                library will still work as-is everywhere that PySerial does.

        """
        log.error('Unknown platform')
        sys.exit(1)
    try:
        log.info('Beginning API command search')
        found_commands = {}
        airview.connect(port=port)
        for length in xrange(12): # limit to 12 for now, most known commands are 4 bytes
            for command in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=length):
                command_string = ''.join(command)
                # ignore 'bs' because we know about it already and it starts a streaming response
                if command_string == 'bs':
                    continue
                response = airview.arbitrary_command(command_string)
                if response is not None:
                    log.info('Found command! %s: %s', command_string, response)
                    found_commands[command_string] = response

    except KeyboardInterrupt as e:
        log.info('Canceling API search due to keyboard interrupt')
    finally:
        log.info('Found %d commands: %s', len(found_commands), found_commands)
        log.info('Exiting')





