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

PyAirview is a very simple Python library for the Ubiquiti Airview2 2.4GHz
spectrum analyzer, which has an undocumented device API.

PyAirview allows the Airview device to be used by 3rd party applications.

The library works pretty well for the intended purpose :)

Once I have the basics written and documented I may port it to C for use in other
languages and so that there is a common low level library available, but it's 
simple enough that even a high level port to Ruby or C# would probably take no 
more than a day.

Usage
----------------------------------

.. code-block:: python

    from __future__ import print_function

    import libairview

    # open the proper serial port
    libairview.connect(port="/dev/ttyACM0")

    # initialize the device
    libairview.initialize()

    # retrieve device-specific information like RF frequency range and channel size
    device_info = libairview.get_device_info()

    """
        start RSSI scanning in a background thread. callback should take a parameter
        named 'rssi_list', which will be a list of rssi values. Use information
        obtained in device_info to interpret the RSSI values and pair them with
        exact frequencies.

    """
    def scan_callback(rssi_list=None):
        print('RSSI levels received: %s', rssi_list)

    libairview.start_background_scan(callback=scan_callback)