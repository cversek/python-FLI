#!/usr/bin/python
"""   
desc:  Setup script for 'FLI' package.
auth:  Craig Wm. Versek (cwv@yesinc.com)
date:  7/25/2012
notes: install with "python setup.py install"
"""
import platform, os, shutil

PACKAGE_METADATA = {
    'name'         : 'FLI',
    'version'      : 'dev',
    'author'       : "Craig Versek",
    'author_email' : "cwv@yesinc.com",
}
    
PACKAGE_SOURCE_DIR = 'src'
MAIN_PACKAGE_DIR   = 'FLI'
MAIN_PACKAGE_PATH  = os.path.abspath(os.sep.join((PACKAGE_SOURCE_DIR,MAIN_PACKAGE_DIR)))
 
if __name__ == "__main__":
    from setuptools import setup, find_packages    
    setup(package_dir      = {'':PACKAGE_SOURCE_DIR},
          packages         = find_packages(PACKAGE_SOURCE_DIR),
          
          #non-code files
          package_data     =   {'': ['*.so']},

          **PACKAGE_METADATA
         )
     

