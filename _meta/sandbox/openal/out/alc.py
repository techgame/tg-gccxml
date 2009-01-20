#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from _ctypes_openal import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Code generated from:
#~   "/System/Library/Frameworks/OpenAL.framework/Headers/alc.h"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ALC_API = extern

#~ line: 22, skipped: 6 ~~~~~~

ALC_APIENTRY = None # empty

#~ line: 29, skipped: 7 ~~~~~~

ALC_VERSION_0_1 = 1

class ALCdevice_struct(Structure):
    _fields_ = [
        ]
# typedef ALCdevice
ALCdevice = ALCdevice_struct
class ALCcontext_struct(Structure):
    _fields_ = [
        ]
# typedef ALCcontext
ALCcontext = ALCcontext_struct

#~ line: 36, skipped: 4 ~~~~~~

# typedef ALCboolean
ALCboolean = c_char

# typedef ALCchar
ALCchar = c_char

#~ line: 54, skipped: 15 ~~~~~~

# typedef ALCint
ALCint = c_int

# typedef ALCuint
ALCuint = c_uint

# typedef ALCsizei
ALCsizei = c_int

# typedef ALCenum
ALCenum = c_int

#~ line: 72, skipped: 9 ~~~~~~

# typedef ALCvoid
ALCvoid = None

#~ line: 78, skipped: 6 ~~~~~~

ALC_INVALID = 0

ALC_FALSE = 0

ALC_TRUE = 1

#~ line: 89, skipped: 5 ~~~~~~

ALC_FREQUENCY = 0x1007

#~ line: 94, skipped: 5 ~~~~~~

ALC_REFRESH = 0x1008

#~ line: 99, skipped: 5 ~~~~~~

ALC_SYNC = 0x1009

#~ line: 104, skipped: 5 ~~~~~~

ALC_MONO_SOURCES = 0x1010

#~ line: 109, skipped: 5 ~~~~~~

ALC_STEREO_SOURCES = 0x1011

#~ line: 118, skipped: 9 ~~~~~~

ALC_NO_ERROR = 0 # = ALC_FALSE

#~ line: 123, skipped: 5 ~~~~~~

ALC_INVALID_DEVICE = 0xA001

#~ line: 128, skipped: 5 ~~~~~~

ALC_INVALID_CONTEXT = 0xA002

#~ line: 133, skipped: 5 ~~~~~~

ALC_INVALID_ENUM = 0xA003

#~ line: 138, skipped: 5 ~~~~~~

ALC_INVALID_VALUE = 0xA004

#~ line: 143, skipped: 5 ~~~~~~

ALC_OUT_OF_MEMORY = 0xA005

#~ line: 149, skipped: 6 ~~~~~~

ALC_DEFAULT_DEVICE_SPECIFIER = 0x1004
ALC_DEVICE_SPECIFIER = 0x1005
ALC_EXTENSIONS = 0x1006

ALC_MAJOR_VERSION = 0x1000
ALC_MINOR_VERSION = 0x1001

ALC_ATTRIBUTES_SIZE = 0x1002
ALC_ALL_ATTRIBUTES = 0x1003

#~ line: 162, skipped: 5 ~~~~~~

ALC_CAPTURE_DEVICE_SPECIFIER = 0x310
ALC_CAPTURE_DEFAULT_DEVICE_SPECIFIER = 0x311
ALC_CAPTURE_SAMPLES = 0x312

#~ line: 172, skipped: 8 ~~~~~~

@bind(POINTER(ALCcontext), [POINTER(ALCdevice), POINTER(ALCint)])
def alcCreateContext(device, attrlist, _api_=None): 
    """alcCreateContext(device, attrlist)
    
        device : POINTER(ALCdevice)
        attrlist : POINTER(ALCint)
    """
    return _api_(device, attrlist)
    

@bind(ALCboolean, [POINTER(ALCcontext)])
def alcMakeContextCurrent(context, _api_=None): 
    """alcMakeContextCurrent(context)
    
        context : POINTER(ALCcontext)
    """
    return _api_(context)
    

@bind(None, [POINTER(ALCcontext)])
def alcProcessContext(context, _api_=None): 
    """alcProcessContext(context)
    
        context : POINTER(ALCcontext)
    """
    return _api_(context)
    

@bind(None, [POINTER(ALCcontext)])
def alcSuspendContext(context, _api_=None): 
    """alcSuspendContext(context)
    
        context : POINTER(ALCcontext)
    """
    return _api_(context)
    

@bind(None, [POINTER(ALCcontext)])
def alcDestroyContext(context, _api_=None): 
    """alcDestroyContext(context)
    
        context : POINTER(ALCcontext)
    """
    return _api_(context)
    

@bind(POINTER(ALCcontext), [])
def alcGetCurrentContext(_api_=None): 
    """alcGetCurrentContext()
    
        
    """
    return _api_()
    

@bind(POINTER(ALCdevice), [POINTER(ALCcontext)])
def alcGetContextsDevice(context, _api_=None): 
    """alcGetContextsDevice(context)
    
        context : POINTER(ALCcontext)
    """
    return _api_(context)
    

#~ line: 190, skipped: 6 ~~~~~~

@bind(POINTER(ALCdevice), [POINTER(ALCchar)])
def alcOpenDevice(devicename, _api_=None): 
    """alcOpenDevice(devicename)
    
        devicename : POINTER(ALCchar)
    """
    return _api_(devicename)
    

@bind(ALCboolean, [POINTER(ALCdevice)])
def alcCloseDevice(device, _api_=None): 
    """alcCloseDevice(device)
    
        device : POINTER(ALCdevice)
    """
    return _api_(device)
    

#~ line: 199, skipped: 7 ~~~~~~

@bind(ALCenum, [POINTER(ALCdevice)])
def alcGetError(device, _api_=None): 
    """alcGetError(device)
    
        device : POINTER(ALCdevice)
    """
    return _api_(device)
    

#~ line: 207, skipped: 8 ~~~~~~

@bind(ALCboolean, [POINTER(ALCdevice), POINTER(ALCchar)])
def alcIsExtensionPresent(device, extname, _api_=None): 
    """alcIsExtensionPresent(device, extname)
    
        device : POINTER(ALCdevice)
        extname : POINTER(ALCchar)
    """
    return _api_(device, extname)
    

@bind(c_void_p, [POINTER(ALCdevice), POINTER(ALCchar)])
def alcGetProcAddress(device, funcname, _api_=None): 
    """alcGetProcAddress(device, funcname)
    
        device : POINTER(ALCdevice)
        funcname : POINTER(ALCchar)
    """
    return _api_(device, funcname)
    

@bind(ALCenum, [POINTER(ALCdevice), POINTER(ALCchar)])
def alcGetEnumValue(device, enumname, _api_=None): 
    """alcGetEnumValue(device, enumname)
    
        device : POINTER(ALCdevice)
        enumname : POINTER(ALCchar)
    """
    return _api_(device, enumname)
    

#~ line: 217, skipped: 6 ~~~~~~

@bind(POINTER(ALCchar), [POINTER(ALCdevice), ALCenum])
def alcGetString(device, param, _api_=None): 
    """alcGetString(device, param)
    
        device : POINTER(ALCdevice)
        param : ALCenum
    """
    return _api_(device, param)
    

@bind(None, [POINTER(ALCdevice), ALCenum, ALCsizei, POINTER(ALCint)])
def alcGetIntegerv(device, param, size, data, _api_=None): 
    """alcGetIntegerv(device, param, size, data)
    
        device : POINTER(ALCdevice)
        param : ALCenum
        size : ALCsizei
        data : POINTER(ALCint)
    """
    return _api_(device, param, size, data)
    

#~ line: 225, skipped: 6 ~~~~~~

@bind(POINTER(ALCdevice), [POINTER(ALCchar), ALCuint, ALCenum, ALCsizei])
def alcCaptureOpenDevice(devicename, frequency, format, buffersize, _api_=None): 
    """alcCaptureOpenDevice(devicename, frequency, format, buffersize)
    
        devicename : POINTER(ALCchar)
        frequency : ALCuint
        format : ALCenum
        buffersize : ALCsizei
    """
    return _api_(devicename, frequency, format, buffersize)
    

@bind(ALCboolean, [POINTER(ALCdevice)])
def alcCaptureCloseDevice(device, _api_=None): 
    """alcCaptureCloseDevice(device)
    
        device : POINTER(ALCdevice)
    """
    return _api_(device)
    

@bind(None, [POINTER(ALCdevice)])
def alcCaptureStart(device, _api_=None): 
    """alcCaptureStart(device)
    
        device : POINTER(ALCdevice)
    """
    return _api_(device)
    

@bind(None, [POINTER(ALCdevice)])
def alcCaptureStop(device, _api_=None): 
    """alcCaptureStop(device)
    
        device : POINTER(ALCdevice)
    """
    return _api_(device)
    

@bind(None, [POINTER(ALCdevice), POINTER(ALCvoid), ALCsizei])
def alcCaptureSamples(device, buffer, samples, _api_=None): 
    """alcCaptureSamples(device, buffer, samples)
    
        device : POINTER(ALCdevice)
        buffer : POINTER(ALCvoid)
        samples : ALCsizei
    """
    return _api_(device, buffer, samples)
    


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ End of code generated from:
#~   "/System/Library/Frameworks/OpenAL.framework/Headers/alc.h"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

