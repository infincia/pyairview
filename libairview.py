#!/usr/bin/env python

from __future__ import print_function

"""
    libairview is a very simple Python library for the Ubiquiti Airview2 2.4GHz
    spectrum analyzer, which has an undocumented device API. It allows the 
    Airview device to be used by 3rd party applications.
    
    Copyright 2013 Infincia LLC


    Library usage
    ----------------------------------------------------------------------------
    
        from __future__ import print_function

        import libairview

        # open the proper serial port
        libairview.connect(port="/dev/ttyACM0")

        # initialize the device
        libairview.initialize()

        # retrieve device-specific information like RF frequency range and channel size
        device_info = libairview.get_device_info()

        '''
            start RSSI scanning in a background thread. callback should take a parameter
            named 'rssi_list', which will be a list of rssi values. Use information
            obtained in device_info to interpret the RSSI values and pair them with
            exact frequencies.

        '''
        def scan_callback(rssi_list=None):
            print('RSSI levels received: %s', rssi_list)

        libairview.start_background_scan(callback=scan_callback)



	Device API documentation
    ----------------------------------------------------------------------------
            
            See the DEVICE_API.md file included with this code.


"""

__author__ = 'Stephen Oliver'
__maintainer__ = 'Stephen Oliver <steve@infincia.com>'
__license__ = 'MIT'


import time
import string
import logging
import threading
import sys
import re
try:
    import serial
except ImportError:
    print('libairview requires the PySerial library to function')
    sys.exit(1)





###########
# globals #
###########

""" 
    Regex to match command responses with named capture groups. Refer to the
    included README.md file for the structure of responses.
    
    Aside from the pipe ("|") and the comma separator, everything else is 
    captured.
        
    command_id: 
        
        Intended to capture the first variable length string of alphanumeric 
        characters. In practice, it's always 4 [a-z] characters, but other 
        undiscovered commands may be different lengths.
    
    command_info: 
        
        Intended to capture a variable length string between the pipe and first
        comma, consisting of alphanumeric characters with possible whitespace
    
    response_data: 
        
        Intended to capture *everything* after the first comma, including:
        
        * Strings which contain multiple additional commas
        * Backslashes
        * Periods
        * Colons
        * Dashes
    
"""
RESPONSE_REGEX_PATTERN = "^(?P<command_id>\w+)\|(?P<command_info>[\w\s]+),(?P<response_data>.+)"


"""
    Known commands
   
    These are documented in the included README.md file, but kept as constants
    for organization purposes here
    
"""
AIRVIEW_COMMAND_INITIALIZE = 'init'
AIRVIEW_COMMAND_GET_DEVICE_INFO = 'gdi'
AIRVIEW_COMMAND_BACKGROUND_SCAN = 'bs'



# global serial port for the Airview
serial_port = None

# background thread exit event
rx_thread_stop = threading.Event()

log = logging.getLogger(__name__)



# internal helper commands

def _send_command(command_string):
    """
        Send the given command over the serial port

    """
    log.debug('Sending command: %s', command_string)
    serial_port.write(command_string + '\r\n')
    serial_port.flushOutput()


def _read_response():
    """
        Read a response from the serial port, looping until either a complete
        message is received, or the timeout expires
        
        Returns the complete message

    """
    log.debug('Reading command response')
    buffer = ''
    valid_response = False
    while True:
        raw = serial_port.read()
        if len(raw) == 0:
            log.debug('Got incomplete or no response message: %s', buffer)
            break
        buffer += raw
        if buffer[-1:] == '\n':
            valid_response = True
            log.debug('Got proper response end')
            break
    if valid_response:
        log.debug('Got complete response message: %s', buffer)
        return buffer
    return None


def _parse_command_response(buffer):
    """
        Parses command responses using a regex that matches the currently known
        command response format, separating the important parts in to named
        groups.
        
        Returns a tuple of all three important response components.

    """
    match = re.match(RESPONSE_REGEX_PATTERN, buffer)
    if match:
        command_id = match.group('command_id')
        command_info = match.group('command_info')
        response_data = match.group('response_data')

        log.debug('Command ID: %s', command_id)
        log.debug('Command Info: %s', command_info)
        log.debug('Response Data: %s', response_data)
        return command_id, command_info, response_data
    return None, None, None


def _background_scan_loop(callback, thread_stop):
    """
        Initiate the primary feature of the device: continuous RF power level 
        scanning across the covered RF range. 
        
        Currently must be run in a background thread.

        Returns RSSI information incrementally in a callback at the moment, but 
        it may be better to yield instead and possibly find a solutiont that 
        avoids the need for threading altogether.

    """
    log.debug('Background scan thread running')


    _send_command(AIRVIEW_COMMAND_BACKGROUND_SCAN)
    log.debug('Background scan command sent to device')

    while not thread_stop.is_set():
        buffer = _read_response()
        if buffer is not None:
            log.debug('Got scan response message: %s', buffer)
            command_id, command_info, response_data = _parse_command_response(buffer)
            if command_id == 'scan':
                raw_samples = response_data.split()
                log.debug('---------------------------------------')
                log.debug('raw samples: %s', raw_samples)
                log.debug('---------------------------------------')
                cleaned_list = list()
                for rssi_level in raw_samples:
                    cleaned_list.append(int(rssi_level))
                log.debug('---------------------------------------')
                log.debug('Length of sample list: %d', len(cleaned_list))
                log.debug('Cleaned rssi list: %s', cleaned_list)
                log.debug('---------------------------------------')
                callback(rssi_list=cleaned_list)
            else:
                log.debug('Got unknown response during scan: %s', buffer)
                continue
        else:
            log.debug('No serial buffer received during scan')
            break
    log.debug('Closing serial port')
    serial_port.close()
    log.debug('Background scan thread loop ended')






# public API

def connect(port=None):
    """
        Connects to the given serial port, must be called before anything else.
        
        Returns True if the connection was successful

    """
    global serial_port
    try:
        log.debug('Opening port: %s' % port)
        serial_port = serial.Serial(
            port = port,
            baudrate = 9600,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE,
            timeout = 0.5)
        return True
    except serial.serialutil.SerialException:
        log.exception('Serial port already open or unavailable')
        return False





def arbitrary_command(command_string):
    """
        Send arbitrary command and return the full response

    """
    _send_command(command_string)
    log.debug('Arbitrary command "%s" sent to device', command_string)
    buffer = _read_response()
    if buffer is not None:
        log.debug('Got "%s" command response message: %s', command_string, buffer)
        return buffer
    log.debug('Received no response during "%s" command request', command_string)




def initialize():
    """
        Send the initialize command to the device and verify the proper response.
        
        This may need to be rewritten to deal with partial overlapping responses,
        for instance when 'bs' and then 'init' are called, currently it's possible
        for the last parts of the 'bs' command responses to be read as part of the
        'init' response, which the response regex will miss as it checks the start 
        of the buffer. Perhaps simply checking for the proper response string in
        the buffer instead of using the regex parser is the easiest solution for
        now.

    """
    _send_command(AIRVIEW_COMMAND_INITIALIZE)
    log.debug('Initialization command sent to device')
    buffer = _read_response()
    if buffer is not None:
        log.debug('Got final initialization response: %s', buffer)
        command_id, command_info, response_data = _parse_command_response(buffer)
        if command_id == 'stat':
            log.debug('Airview device initialized')
            return True
        else:
            log.error('Unknown response to initialization command!!!')
            return False
    log.debug('Got no buffer during initialize request')
    return False





def get_device_info():
    """
        Retrieve device-specific information about the hardware, the RF range
        the firmware version etc. See the included README.md file for more info.

    """
    _send_command(AIRVIEW_COMMAND_GET_DEVICE_INFO)
    log.debug('Device info command sent to device')
    buffer = _read_response()
    if buffer is not None:
        log.debug('Got device info response message: %s', buffer)
        command_id, command_info, response_data = _parse_command_response(buffer)
        if command_id == 'devi':
            log.debug('Airview device info: %s', response)
            return response_data
        else:
            log.error('Unknown response to device info command!!!')
            return None
    log.debug('Got no buffer during device info request')
    return None






def start_background_scan(callback=None):
    """
        Start the background scan thread and block the caller until the thread
        gracefully exits. Call stop_background_scan() to do that.

    """
    log.debug('Starting scan in background thread')
    rx_thread = threading.Thread(target=_background_scan_loop, args=(callback, rx_thread_stop))
    rx_thread.daemon = True
    rx_thread.start()
    while rx_thread.isAlive:
        rx_thread.join(5)





def stop_background_scan():
    """
        Should cause the rx_thread to stop looping and gracefully exit. Should.
        It may not at the moment depending on how exceptions are handled and
        various other things.
    
    """
    rx_thread_stop.set()
