#PyAirview

[![License](https://pypip.in/license/pyairview/badge.svg)](https://pypi.python.org/pypi/pyairview/)
[![Supported Python versions](https://pypip.in/py_versions/pyairview/badge.svg)](https://pypi.python.org/pypi/pyairview/)
[![Development Status](https://pypip.in/status/pyairview/badge.svg)](https://pypi.python.org/pypi/pyairview/)

PyAirview is a very simple Python library for the Ubiquiti Airview2 2.4GHz
spectrum analyzer, which has an undocumented device API.

PyAirview allows the Airview device to be used by 3rd party applications.

The library works pretty well for the intended purpose :)

Once I have the basics written and documented I may port it to C for use in other
languages and so that there is a common low level library available, but it's 
simple enough that even a high level port to Ruby or C# would probably take no 
more than a day. 

##Airview2 hardware

The Airview2 devices were very cheap ($29-39) and originally came with a Java 
app for visualizing usage of that frequency band, for Wi-Fi network planning, 
discovering rogue hotspots, diagnosing Bluetooth issues, etc.

Inside, the device is basically just a simple microcontroller (A [CC2011](http://www.ti.com/product/cc2511)) 
with an integrated 2.4GHz radio and a USB interface. It uses the standard USB 
CDC-ACM serial interface to connect to a PC.

The firmware running on the device is likely custom built by Ubiquiti Networks,
I don't possess a copy of it outside my own Airview2 device, even in dumped binary 
form, so I don't know much about it but it seems to be a simple command/response
loop coupled with a function to use the native RSSI power level scanning provided
by the chip.

##Library development and reverse engineering

This library was created after hours and hours of manual testing with `gtkterm`
and `screen`, guessing the proper commands to use the device API. None of the 
information used to create this library came from decompiling the device firmware
or the original Java application. 

*DO NOT* create github issues containing, or send me the following things:

* Dumped firmware from the device
* Decompiled firmware or code derived from it
* Decompiled versions of the original software or code derived from it
* API related code of any kind (aside from documented 'clean room' efforts)
* Etc.

I have not seen those things, and I do not want to see them as it would prevent 
me from being able to write code for this library anymore.

I'm not even sure how to go about using clean room documentation properly, if 
someone were to provide it to me, so while it would probably help and I would
appreciate the help of course, please don't post or send documentation either 
without discussing it with me first.

If you want to help, feel free to review the code for flaws, or open a terminal 
connected to your Airview device and guess some commands as I have done :)
