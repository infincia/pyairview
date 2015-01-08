#!/usr/bin/env python

from __future__ import print_function, division


""" libairview test

    Copyright 2014 Infincia LLC
    
    See LICENSE file for license information
    
	Usage:  Install the libraries in requirements.txt, then just plug in your
            Airview2 stick, set the serial port manually if autodetection fails, 
            and run this script from the terminal.
            
            The script initializes the device using libairview, then sends it 
            the proper command to start a constant RF scan, returning RSSI info
            in a callback.
            
            This is simply an example of how to use the library, in your own
            code, only 5-6 lines are necessary to use libairview properly.

"""

__author__ = 'Stephen Oliver'
__maintainer__ = 'Stephen Oliver <steve@infincia.com>'
__version__ = '0.1-prerelease'
__license__ = 'MIT'



import logging
import logging.handlers
import platform
import sys

import libairview as airview




log = logging.getLogger()
mainHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
mainHandler.setFormatter(logging.Formatter('%(levelname)s %(asctime)s - %(module)s - %(funcName)s: %(message)s'))
log.addHandler(mainHandler)



def scan_callback(rssi_list=None):
    log.info('RSSI levels received: %s', rssi_list)

if __name__ == '__main__':
    log.info('Starting Airview')
    system_name = platform.system()
    logging.info('Running on: %s' % system_name)
    if system_name == 'Linux':
        port = '/dev/ttyACM0' # arbitrary, need a way to detect/configure
    elif system_name == 'Darwin': # OS X
        port = '/dev/tty.usbmodem411' # this seems arbitrary too, but consistent
    else:
        # Note: Need to find out what the device name will be on FreeBSD and others,
        #       but this is just the test, the library will work as-is everywhere,
        #       even on Windows thanks to PySerial
        log.error('Unknown platform')
        sys.exit(1)
    try:
        log.info('Initializing device')
        airview.connect(port=port)
        initialized = airview.initialize()
        if initialized:
            log.info('Starting background scan')
            airview.start_background_scan(callback=scan_callback)
        else:
            log.info('Initialization failed!')
    except KeyboardInterrupt as e:
        log.info('Cancelling scan')
        airview.stop_background_scan()
    finally:
        log.info('Exiting')





