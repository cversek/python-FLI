python-FLI
==========

Python bindings for Finger Lakes Instrumentation (FLI) cameras and peripherals.

Install with "python setup.py install".

Tested on Linux kernel 2.6.32-41-generic #89-Ubuntu SMP.
Requires FLI SDK >= 1.104 and FLI Linux Kernel Module >= 1.3 from 
http://www.flicamera.com/software/index.html

The SDK library should be built as a shared object, named 'libfli.so', and 
located in a standard library path, such as /usr/local/lib, or placed in the
Python package folder after installation. (See the issue [Preparing the FLI SDK Dependency](https://github.com/cversek/python-FLI/issues/1))

Those interested in better Windows API compatibility and a more comprehensive feature set
should take a look at Charles Harris's Cython based wrappers: https://github.com/charris/pyfli
