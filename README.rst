============================
PyAirview
============================

.. image:: https://pypip.in/license/pyairview/badge.svg
    :target: https://pypi.python.org/pypi/pyairview/
    :alt: License

.. image:: https://pypip.in/py_versions/pyairview/badge.svg
    :target: https://pypi.python.org/pypi/pyairview/
    :alt: Supported Python versions

.. image:: https://pypip.in/status/pyairview/badge.svg
    :target: https://pypi.python.org/pypi/pyairview/
    :alt: Development Status

.. image:: https://travis-ci.org/infincia/pyairview.svg?branch=master
    :target: https://travis-ci.org/infincia/pyairview

PyAirview is a very simple Python library for the Ubiquiti Airview2 2.4GHz
spectrum analyzer, which has an undocumented device API.

PyAirview allows the Airview device to be used by 3rd party applications.

The library works pretty well for the intended purpose :)

Once I have the basics written and documented I may port it to C for use in other
languages and so that there is a common low level library available, but it's 
simple enough that even a high level port to Ruby or C# would probably take no 
more than a day.

Device API documentation
----------------------------------

See the DEVICE_API.md_ file included in this repository

Usage
----------------------------------

.. code-block:: python

    from __future__ import print_function
    from time import sleep

    import pyairview

    # open the proper serial port
    pyairview.connect(port="/dev/ttyACM0")

    # retrieve device-specific information like RF frequency range and channel size
    device_info = pyairview.get_device_info()
    print('Device info: %s', device_info)

    """
        start RSSI scanning in a background thread. callback should take a parameter
        named 'rssi_list', which will be a list of rssi values. Use information
        obtained in device_info to interpret the RSSI values and pair them with
        exact frequencies.

    """
    def scan_callback(rssi_list):
        print('Received %d RSSI level readings: %s', len(rssi_list), rssi_list)

    pyairview.start_scan(callback=scan_callback)

    some_condition = False
    while pyairview.is_scanning():
        sleep(0.1) # or do something else, change some_condition, etc
        if some_condition == True:
            pyairview.stop_scan()

Airview2 hardware
----------------------------------

The Airview2 devices were very cheap ($29-39) and originally came with a Java 
app for visualizing usage of that frequency band, for Wi-Fi network planning, 
discovering rogue hotspots, diagnosing Bluetooth issues, etc.

Inside, the device is basically just a simple microcontroller (A CC2011_)
with an integrated 2.4GHz radio and a USB interface. It uses the standard USB 
CDC-ACM serial interface to connect to a PC.

The firmware running on the device is likely custom built by Ubiquiti Networks,
I don't possess a copy of it outside my own Airview2 device, even in dumped binary 
form, so I don't know much about it but it seems to be a simple command/response
loop coupled with a function to use the native RSSI power level scanning provided
by the chip.

Library development and reverse engineering
----------------------------------

This library was created after hours and hours of manual testing with ``gtkterm``
and ``screen``, guessing the proper commands to use the device API. None of the
information used to create this library came from decompiling the device firmware
or the original Java application. 

*DO NOT* create github issues containing, or send me the following things:

- Dumped firmware from the device
- Decompiled firmware or code derived from it
- Decompiled versions of the original software or code derived from it
- API related code of any kind (aside from documented 'clean room' efforts)
- Etc.

I have not seen those things, and I do not want to see them as it would prevent 
me from being able to write code for this library anymore.

I'm not even sure how to go about using clean room documentation properly, if 
someone were to provide it to me, so while it would probably help and I would
appreciate the help of course, please don't post or send documentation either 
without discussing it with me first.

If you want to help, feel free to review the code for flaws, or open a terminal 
connected to your Airview device and guess some commands as I have done :)




.. _CC2011: http://www.ti.com/product/cc2511
.. _DEVICE_API.md: https://github.com/infincia/pyairview/blob/master/DEVICE_API.md