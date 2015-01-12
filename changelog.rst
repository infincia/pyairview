Changelog
=========

.. currentmodule:: PyAirview


Release 0.1a1
-------------

- Rename libairview module to pyairview to match project name (same for test app)

- Automatic testing with Travis-CI. Just tests importing the pyairview module
  for now, but that is enough to discover certain simple bugs. Code to simulate
  a serial connection to an actual Airview device will be added soon, which is
  necessary in order to actually test anything in the library itself

- Make start_scan() command non-blocking, caller is expected to handle managing
  the library as part of a runloop etc.

- Add disconnect() command to close the serial port if needed

- Allow calling code to safely start and stop scanning whenever needed

- Handle situations where partial responses are left in the serial buffer

- Add support for newly discovered 'es' command to instruct Airview to end the
  current scan

- Add automatic parsing of device info from 'gdi' command, each element is put
  into a dictionary with public module constants provided for each key


Release 0.1a0
-------------

- Support for Python 2.7 only for now, 3.2+ is being worked on

- Initial alpha release