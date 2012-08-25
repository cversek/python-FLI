"""
 FLI.camera.py 
 
 Object-orienting interface for handling FLI USB cameras
 
 author:       Craig Wm. Versek, Yankee Environmental Systems 
 author_email: cwv@yesinc.com
"""

__author__ = 'Craig Wm. Versek'
__date__ = '2012-08-08'

import sys, time

try:
    from collections import OrderedDict
except ImportError:
    from odict import OrderedDict

from ctypes import pointer, POINTER, byref, sizeof, Structure, c_char,\
                   c_char_p, c_long, c_ubyte, c_uint16, c_double


import numpy

from lib import FLILibrary, FLIError, FLIWarning, flidomain_t, flidev_t,\
                fliframe_t, FLIDOMAIN_USB, FLIDEVICE_CAMERA,\
                FLI_FRAME_TYPE_NORMAL, FLI_FRAME_TYPE_DARK, FLI_MODE_8BIT,\
                FLI_MODE_16BIT

from device import USBDevice
###############################################################################
DEBUG = False
###############################################################################
class USBCamera(USBDevice):
    #load the DLL
    _libfli = FLILibrary.getDll(debug=DEBUG)
    _domain = flidomain_t(FLIDOMAIN_USB | FLIDEVICE_CAMERA)
    
    def __init__(self, dev_name, model):
        USBDevice.__init__(self, dev_name = dev_name, model = model)
        self.hbin  = 1
        self.vbin  = 1
   
    def get_info(self):
        info = OrderedDict()        
        tmp1, tmp2, tmp3, tmp4   = (c_long(),c_long(),c_long(),c_long())
        d1, d2                   = (c_double(),c_double())        
        self._libfli.FLIGetHWRevision(self._dev, byref(tmp1))
        info['Hardware Rev'] = tmp1.value
        self._libfli.FLIGetFWRevision(self._dev, byref(tmp1))
        info['Firmware Rev'] = tmp1.value
        self._libfli.FLIGetPixelSize(self._dev, byref(d1), byref(d2))
        info['Pixel Size'] = (d1.value,d2.value)
        self._libfli.FLIGetArrayArea(self._dev, byref(tmp1), byref(tmp2), byref(tmp3), byref(tmp4))
        info['Array Area'] = (tmp1.value,tmp2.value,tmp3.value,tmp4.value)
        self._libfli.FLIGetVisibleArea(self._dev, byref(tmp1), byref(tmp2), byref(tmp3), byref(tmp4))
        info['Visible Area'] = (tmp1.value,tmp2.value,tmp3.value,tmp4.value)        
        return info

    def get_image_size(self):
        "returns (row_width, img_rows, img_size)"
        left, top, right, bottom   = (c_long(),c_long(),c_long(),c_long())        
        self._libfli.FLIGetVisibleArea(self._dev, byref(left), byref(top), byref(right), byref(bottom))    
        row_width = (right.value - left.value)/self.hbin
        img_rows  = (bottom.value - top.value)/self.vbin
        img_size = img_size = img_rows * row_width * sizeof(c_uint16)
        return (row_width, img_rows, img_size)

    def set_image_area(self, ul_x, ul_y, lr_x, lr_y):
        self._libfli.FLISetImageArea(self._dev, c_long(ul_x), c_long(ul_y), c_long(lr_x), c_long(lr_y))
    
    def set_image_binning(self, hbin = 1, vbin = 1):
        left, top, right, bottom   = (c_long(),c_long(),c_long(),c_long())        
        self._libfli.FLIGetVisibleArea(self._dev, byref(left), byref(top), byref(right), byref(bottom))    
        row_width = (right.value - left.value)/hbin
        img_rows  = (bottom.value - top.value)/vbin
        self._libfli.FLISetImageArea(self._dev, left, top, left.value + row_width, top.value + img_rows)
        self._libfli.FLISetHBin(self._dev, hbin)
        self._libfli.FLISetVBin(self._dev, vbin)
        self.hbin = hbin
        self.vbin = vbin
    
    def set_flushes(self, num):
        "set the number of flushes to the CCD before taking exposure"
        self._libfli.FLISetNFlushes(self._dev, num)

    def set_temperature(self, T):
        "set the camera's temperature target in degrees Celcius"
        self._libfli.FLISetTemperature(self._dev, T)
                
    def get_temperature(self):
        "gets the camera's temperature in degrees Celcius"
        T = c_double()         
        self._libfli.FLIGetTemperature(self._dev, byref(T))
        return T.value

    def set_exposure(self, exptime, frametype = "normal"):
        """set the exposure time, 'exptime' in milliseconds and the 
           'frametype' as 'normal' or 'dark'"""
        exptime = c_long(exptime)        
        if frametype == "normal":
            frametype = fliframe_t(FLI_FRAME_TYPE_NORMAL)
        elif frametype == "dark":
            frametype = fliframe_t(FLI_FRAME_TYPE_DARK)
        else:
            raise ValueError("'frametype' must be either 'normal' or 'dark'")
        self._libfli.FLISetExposureTime(self._dev, exptime)
        self._libfli.FLISetFrameType(self._dev, frametype)

    def set_bit_depth(self, bitdepth='8bit'):
        if bitdepth == '8bit':
            self._libfli.FLISetBitDepth(self._dev, FLI_MODE_8BIT)
        elif bitdepth == '16bit':
            self._libfli.FLISetBitDepth(self._dev, FLI_MODE_16BIT)
        else:
            raise ValueError("'bitdepth' must be either '8bit' or '16bit'")

    def take_photo(self):
        "expose the frame and return as an ndarray object"
        row_width, img_rows, img_size  = self.get_image_size()        
        #allocate numpy array to store image
        img_array = numpy.zeros((img_rows, row_width), dtype=numpy.uint16)
        #get pointer to array's data space
        img_ptr   = img_array.ctypes.data_as(POINTER(c_uint16))
        #take exposure and wait for completion
        timeleft = c_long()
        self._libfli.FLIExposeFrame(self._dev)
        while True:
            self._libfli.FLIGetExposureStatus(self._dev,byref(timeleft))
            if timeleft.value == 0:
                break            
            time.sleep(timeleft.value/1000.0) #sleep for milliseconds
        #aquire image row by row
        for row in range(img_rows):
            offset = row*row_width*sizeof(c_uint16)
            self._libfli.FLIGrabRow(self._dev, byref(img_ptr.contents,offset), row_width)
        return img_array
        
###############################################################################
#  TEST CODE
###############################################################################
if __name__ == "__main__":
    cams = USBCamera.find_devices()
    cam0 = cams[0]
    print "info:", cam0.get_info()
    print "image size:", cam0.get_image_size()
    print "temperature:", cam0.get_temperature()
    cam0.set_image_binning(2,2)
    cam0.set_bit_depth("16bit")
    cam0.set_exposure(5)
    img = cam0.take_photo()
    print img
    
