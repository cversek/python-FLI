python-FLI
==========

Python bindings for Finger Lakes Instrumentation (FLI) cameras and peripherals.

Install with "python setup.py install".

Tested on Linux kernel 2.6.32-41-generic #89-Ubuntu SMP.
Requires FLI SDK and Linux Kernel Module from 
http://www.flicamera.com/software/index.html

The SDK library should be built as a shared object, named 'libfli.so', and 
located in a standard library path, such as /usr/local/lib, or placed in the
Python package folder after installation.
