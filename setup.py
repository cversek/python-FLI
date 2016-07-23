#!/usr/bin/python
"""   
desc:  Setup script for 'FLI' package.
auth:  Craig Wm. Versek (cwv@yesinc.com)
date:  7/25/2012
notes: Install with "python setup.py install".
       Requires FLI SDK and Linux Kernel Module 
       from http://www.flicamera.com/software/index.html
       The SDK library should be built as a shared object, named 'libfli.so',
       and located in a standard library path, such as /usr/local/lib
"""
import platform, os, shutil


    
PACKAGE_SOURCE_DIR = 'src'
PACKAGE_NAME       = 'FLI'
PACKAGE_PATH  = os.path.abspath(os.sep.join((PACKAGE_SOURCE_DIR,PACKAGE_NAME)))

PACKAGE_METADATA = {
    'name'         : PACKAGE_NAME,
    'version'      : 'dev',
    'author'       : "Craig Versek",
    'author_email' : "cwv@yesinc.com",
}
 
if __name__ == "__main__":
    from setuptools import setup, find_packages
    setup(
          packages         = find_packages(PACKAGE_SOURCE_DIR),
          package_dir      = {'':PACKAGE_SOURCE_DIR},
          
          #non-source files
          package_data     =   {'': ['*.so', '*.dll']},

          **PACKAGE_METADATA
         )

