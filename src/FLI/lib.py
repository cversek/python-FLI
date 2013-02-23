"""
 FLI.lib.py 
 
 Python interface to the FLI (Finger Lakes Instrumentation) API
 
 author:       Craig Wm. Versek, Yankee Environmental Systems 
 author_email: cwv@yesinc.com
"""

__author__ = 'Craig Wm. Versek'
__date__ = '2012-07-25'

import sys
from ctypes import cdll, c_char, c_char_p, c_long, c_ubyte
###############################################################################
# library definitions

#   An opaque handle used by library functions to refer to FLI
#   hardware.

FLI_INVALID_DEVICE = -1

flidev_t = c_long

#   The domain of an FLI device.  This consists of a bitwise ORed
#   combination of interface method and device type.  Valid interfaces
#   are \texttt{FLIDOMAIN_PARALLEL_PORT}, \texttt{FLIDOMAIN_USB},
#   \texttt{FLIDOMAIN_SERIAL}, and \texttt{FLIDOMAIN_INET}.  Valid
#   device types are \texttt{FLIDEVICE_CAMERA},
#   \texttt{FLIDOMAIN_FILTERWHEEL}, and \texttt{FLIDOMAIN_FOCUSER}.
#   @see FLIOpen
#   @see FLIList

flidomain_t = c_long

FLIDOMAIN_NONE           = 0x00
FLIDOMAIN_PARALLEL_PORT  = 0x01
FLIDOMAIN_USB            = 0x02
FLIDOMAIN_SERIAL         = 0x03
FLIDOMAIN_INET           = 0x04
FLIDOMAIN_SERIAL_19200   = 0x05
FLIDOMAIN_SERIAL_1200    = 0x06

FLIDEVICE_NONE           = 0x000
FLIDEVICE_CAMERA         = 0x100
FLIDEVICE_FILTERWHEEL    = 0x200
FLIDEVICE_FOCUSER        = 0x300
FLIDEVICE_HS_FILTERWHEEL          = 0x0400
FLIDEVICE_RAW                     = 0x0f00
FLIDEVICE_ENUMERATE_BY_CONNECTION = 0x8000

#   The frame type for an FLI CCD camera device.  Valid frame types are
#   \texttt{FLI_FRAME_TYPE_NORMAL} and \texttt{FLI_FRAME_TYPE_DARK}.
#   @see FLISetFrameType

fliframe_t = c_long

FLI_FRAME_TYPE_NORMAL = 0
FLI_FRAME_TYPE_DARK   = 1
FLI_FRAME_TYPE_FLOOD  = 2
FLI_FRAME_TYPE_RBI_FLUSH = FLI_FRAME_TYPE_FLOOD | FLI_FRAME_TYPE_DARK

#   The gray-scale bit depth for an FLI camera device.  Valid bit
#   depths are \texttt{FLI_MODE_8BIT} and \texttt{FLI_MODE_16BIT}.
#   @see FLISetBitDepth

flibitdepth_t = c_long

FLI_MODE_8BIT  = 0
FLI_MODE_16BIT = 1

#   Type used for shutter operations for an FLI camera device.  Valid
#   shutter types are \texttt{FLI_SHUTTER_CLOSE},
#   \texttt{FLI_SHUTTER_OPEN},
#   \texttt{FLI_SHUTTER_EXTERNAL_TRIGGER},
#   \texttt{FLI_SHUTTER_EXTERNAL_TRIGGER_LOW}, and
#   \texttt{FLI_SHUTTER_EXTERNAL_TRIGGER_HIGH}.
#   @see FLIControlShutter

flishutter_t = c_long

FLI_SHUTTER_CLOSE                     = 0x0000
FLI_SHUTTER_OPEN                      = 0x0001
FLI_SHUTTER_EXTERNAL_TRIGGER          = 0x0002
FLI_SHUTTER_EXTERNAL_TRIGGER_LOW      = 0x0002
FLI_SHUTTER_EXTERNAL_TRIGGER_HIGH     = 0x0004
FLI_SHUTTER_EXTERNAL_EXPOSURE_CONTROL = 0x0008

#   Type used for background flush operations for an FLI camera device.  Valid
#   bgflush types are \texttt{FLI_BGFLUSH_STOP} and
#   \texttt{FLI_BGFLUSH_START}.
#   @see FLIControlBackgroundFlush

flibgflush_t = c_long

FLI_BGFLUSH_STOP  = 0x0000
FLI_BGFLUSH_START = 0x0001

#   Type used to determine which temperature channel to read.  Valid
#   channel types are \texttt{FLI_TEMPERATURE_INTERNAL} and
#   \texttt{FLI_TEMPERATURE_EXTERNAL}.
#   @see FLIReadTemperature

flichannel_t = c_long

FLI_TEMPERATURE_INTERNAL = 0x0000
FLI_TEMPERATURE_EXTERNAL = 0x0001
FLI_TEMPERATURE_CCD      = 0x0000
FLI_TEMPERATURE_BASE     = 0x0001

#   Type specifying library debug levels.  Valid debug levels are
#   \texttt{FLIDEBUG_NONE}, \texttt{FLIDEBUG_INFO},
#   \texttt{FLIDEBUG_WARN}, and \texttt{FLIDEBUG_FAIL}.
#   @see FLISetDebugLevel

flidebug_t    = c_long
flimode_t     = c_long
flistatus_t   = c_long
flitdirate_t  = c_long
flitdiflags_t = c_long

# Status settings 
FLI_CAMERA_STATUS_UNKNOWN             = 0xffffffff
FLI_CAMERA_STATUS_MASK                = 0x00000003
FLI_CAMERA_STATUS_IDLE                = 0x00
FLI_CAMERA_STATUS_WAITING_FOR_TRIGGER = 0x01
FLI_CAMERA_STATUS_EXPOSING            = 0x02
FLI_CAMERA_STATUS_READING_CCD         = 0x03
FLI_CAMERA_DATA_READY                 = 0x80000000

FLI_FOCUSER_STATUS_UNKNOWN     = 0xffffffff
FLI_FOCUSER_STATUS_HOMING      = 0x00000004
FLI_FOCUSER_STATUS_MOVING_IN   = 0x00000001
FLI_FOCUSER_STATUS_MOVING_OUT  = 0x00000002
FLI_FOCUSER_STATUS_MOVING_MASK = 0x00000007
FLI_FOCUSER_STATUS_HOME        = 0x00000080
FLI_FOCUSER_STATUS_LIMIT       = 0x00000040
FLI_FOCUSER_STATUS_LEGACY      = 0x10000000

FLI_FILTER_WHEEL_PHYSICAL        = 0x100
FLI_FILTER_WHEEL_VIRTUAL         = 0
FLI_FILTER_WHEEL_LEFT            = FLI_FILTER_WHEEL_PHYSICAL | 0x00
FLI_FILTER_WHEEL_RIGHT           = FLI_FILTER_WHEEL_PHYSICAL | 0x01
FLI_FILTER_STATUS_MOVING_CCW     = 0x01
FLI_FILTER_STATUS_MOVING_CW      = 0x02
FLI_FILTER_POSITION_UNKNOWN      = 0xff
FLI_FILTER_POSITION_CURRENT      = 0x200
FLI_FILTER_STATUS_HOMING         = 0x00000004
FLI_FILTER_STATUS_HOME           = 0x00000080
FLI_FILTER_STATUS_HOME_LEFT      = 0x00000080
FLI_FILTER_STATUS_HOME_RIGHT     = 0x00000040
FLI_FILTER_STATUS_HOME_SUCCEEDED = 0x00000008

FLIDEBUG_NONE = 0x00
FLIDEBUG_INFO = 0x01
FLIDEBUG_WARN = 0x02
FLIDEBUG_FAIL = 0x04
FLIDEBUG_IO   = 0x08
FLIDEBUG_ALL  = FLIDEBUG_INFO | FLIDEBUG_WARN | FLIDEBUG_FAIL

FLI_IO_P0 = 0x01
FLI_IO_P1 = 0x02
FLI_IO_P2 = 0x04
FLI_IO_P3 = 0x08

FLI_FAN_SPEED_OFF = 0x00
FLI_FAN_SPEED_ON  = 0xffffffff

FLI_EEPROM_USER      = 0x00
FLI_EEPROM_PIXEL_MAP = 0x01

FLI_PIXEL_DEFECT_COLUMN       = 0x00
FLI_PIXEL_DEFECT_CLUSTER      = 0x10
FLI_PIXEL_DEFECT_POINT_BRIGHT = 0x20
FLI_PIXEL_DEFECT_POINT_DARK   = 0x30
###############################################################################
import warnings

class FLIError(Exception):
    pass

class FLIWarning(Warning):
    pass


###############################################################################
LIBVERSIZ = 1024

class FLILibrary:
    __dll = None
    @staticmethod
    def getDll(debug = False):
        if FLILibrary.__dll is None:
            if sys.platform == 'linux2':
                FLILibrary.__dll = cdll.LoadLibrary("libfli.so")
            elif sys.platform == 'win32': #FIXME this hasn't been tested yet
                from ctypes import windll
                FLILibrary.__dll = windll.LoadLibrary("libfli")
            else:
                raise RuntimeError("Platform not supported")
        if debug:
            FLILibrary.__dll.FLISetDebugLevel(None, FLIDEBUG_ALL)
        return FLILibrary.__dll
    @staticmethod
    def getVersion():
        libfli = FLILibrary.getDll()
        c_buff = c_char*LIBVERSIZ
        libver = c_buff()
        libfli.FLIGetLibVersion(libver,LIBVERSIZ)
        return libver.value

###############################################################################
#  TEST CODE
###############################################################################
if __name__ == "__main__":
    libfli = FLILibrary.getDll(debug=True)
