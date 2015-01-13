#!/usr/bin/env python

import sys
import os
from os.path import join, abspath, basename, dirname
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup



py = sys.version_info
print('Python version: %s', py)
if py < (2,7) and py < (3,2):
    raise NotImplementedError("PyAirview requires Python 2.7 or Python 3.2+")

def read_file(name, *args):
    try:
        return open(join(dirname(__file__), name)).read(*args)
    except OSError:
        return ''


setup(name='pyairview',
    version='0.1a2',
    description='PyAirview is a very simple Python library for the Ubiquiti Airview2 2.4GHz spectrum analyzer, which has an undocumented device API.',
    long_description=read_file('README.rst'),
    author='Stephen Oliver',
    author_email='steve@infincia.com',
    url='http://infincia.github.io/pyairview/',
    scripts=['pyairview_test.py'],
    py_modules=['pyairview'],
    license='MIT',
    keywords='airview ubiquiti airview2 spectrum analyzer',
    platforms = 'any',
    install_requires = ['PySerial'],
    classifiers=['Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Hardware :: Hardware Drivers',
    ],
)


