#!/usr/bin/env python

from __future__ import print_function, division


""" libairview test

    Copyright 2014 Infincia LLC
    
    See LICENSE file for license information
    
	Usage:  Install the libraries in requirements.txt, then just plug in your
            Airview2 stick, and run ./test.py -h to see the command options.
            
            The only mandatory option is the port (-p /dev/tty*), and a command,
            either 'scan' or 'fuzzer'.
            
            Note that this is simply an example of how to use the libairview 
            library in your own code. Typically only 5-6 lines of code are needed
            in order to use libairview for RSSI scanning.

    Command: fuzzer

            Sends every possible command to the device, up to 12 characters long
            by default (-l 6 changes it to stop at 6, etc).
            
            Periodically results are printed to the terminal, and at the end of 
            testing or if the test is canceled, the final results are printed on 
            the terminal as well.
            
            This script explicitly ignores the 'bs' command because it is both
            already known, and it initiates a stream response that requires 
            proper handling of the response, rather than a single response which
            is what we're testing for anyway to discover other commands.
            
    Command: scan
    
            Demonstrates the RSSI scan stream function, no arguments are needed.

"""

__author__ = 'Stephen Oliver'
__maintainer__ = 'Stephen Oliver <steve@infincia.com>'
__license__ = 'MIT'



import logging
import logging.handlers
import sys
import argparse
import itertools


import libairview




log = logging.getLogger()
mainHandler = logging.StreamHandler()
log.setLevel(logging.INFO)
mainHandler.setFormatter(logging.Formatter('%(levelname)s %(asctime)s - %(module)s - %(funcName)s: %(message)s'))
log.addHandler(mainHandler)


def scan_callback(rssi_list=None):
    log.info('RSSI levels received: %s', rssi_list)


def scan(args):
    log.info('Starting Airview RSSI scan')
    try:
        libairview.start_background_scan(callback=scan_callback)
    except KeyboardInterrupt as e:
        log.info('Cancelling scan')
        libairview.stop_background_scan()
    finally:
        log.info('Exiting')



def fuzzer(args):
    log.info('Starting Airview API Fuzzer')
    try:
        log.info('Beginning API search for commands up to %d letters', args.length)
        found_commands = {}
        check_count = 0

        for length in xrange(args.length):
            for command in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=length):
                check_count = check_count + 1
                command_string = ''.join(command)
                # ignore 'bs' because we know about it already and it starts a streaming response
                if command_string == 'bs':
                    continue
                log.info('Checking: %s', command_string)
                response = libairview.arbitrary_command(command_string)
                if response is not None:
                    log.info('Found command! %s: %s', command_string, response)
                    found_commands[command_string] = response
                if check_count % 100 == 0:
                    log.info('--------------------------------------------------------------------------------------')
                    log.info('Checked %d commands so far, got %d valid responses: %s', check_count, len(found_commands), found_commands)
                    log.info('--------------------------------------------------------------------------------------')

    except KeyboardInterrupt as e:
        log.info('Canceling API search due to keyboard interrupt')
    finally:
        log.info('Checked %d commands total and got %d valid responses: %s', check_count, len(found_commands), found_commands)
        log.info('Exiting')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Airview2 test program')
    arg_parser.add_argument('-p', '--port', help='The serial port of the Airview2 device (/dev/tty*)', required=True)

    subparsers = arg_parser.add_subparsers()
    parser_fuzzer = subparsers.add_parser('fuzzer')
    parser_fuzzer.add_argument('-l', '--length', type=int, default=6, help='The length of command strings to check (default: 6)')
    parser_fuzzer.set_defaults(func=fuzzer)

    parser_scan = subparsers.add_parser('scan')
    parser_scan.set_defaults(func=scan)

    args = arg_parser.parse_args()

    connected = libairview.connect(port=args.port)
    if not connected:
        log.error('Port already in use')
        sys.exit(1)
    log.info('Initializing device')
    initialized = libairview.initialize()
    if initialized:
        args.func(args)
    else:
        log.info('Initialization failed!')





