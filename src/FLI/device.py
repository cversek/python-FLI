"""
 FLI.device.py 
 
 Object-orienting base interface for handling FLI USB devices
 
 author:       Craig Wm. Versek, Yankee Environmental Systems 
 author_email: cwv@yesinc.com
"""

__author__ = 'Craig Wm. Versek'
__date__   = '2012-08-16'

import sys, time

import ctypes
from ctypes import pointer, POINTER, byref, c_char, c_char_p, c_long, c_ubyte, c_double, c_size_t


import numpy

from lib import FLILibrary, FLIError, FLIWarning, flidomain_t, flidev_t,\
                FLIDOMAIN_USB
###############################################################################
DEBUG = False
BUFFER_SIZE = 64
###############################################################################
class USBDevice(object):
    """ base class for all FLI USB devices"""
    #load the DLL
    _libfli = FLILibrary.getDll(debug=DEBUG)
    _domain = flidomain_t(FLIDOMAIN_USB)

    def __init__(self, dev_name, model):
        self.dev_name = dev_name
        self.model  = model
        #open the device
        self._dev = flidev_t()
        self._libfli.FLIOpen(byref(self._dev),dev_name,self._domain)
   
    def __del__(self):
        self._libfli.FLIClose(self._dev)
        
    def get_serial_num(self):
        serial = ctypes.create_string_buffer(BUFFER_SIZE)
        self._libfli.FLIGetSerialString(self._dev,serial,c_size_t(BUFFER_SIZE))
        return serial.value
    
    @classmethod    
    def find_devices(cls):
        "locates all FLI USB devices and returns a list of USBDevice objects"

        tmplist = POINTER(c_char_p)()      
        cls._libfli.FLIList(cls._domain, byref(tmplist)) #allocates memory
        devs = []        
        i = 0        
        while not tmplist[i] is None:
            dev_name, model = tmplist[i].split(";")
            devs.append(cls(dev_name=dev_name,model=model))   #create device objects         
            i += 1
        cls._libfli.FLIFreeList(tmplist)            #frees memory   
        return devs
###############################################################################
#  TEST CODE
###############################################################################
if __name__ == "__main__":
    devs = USBDevice.find_devices()
