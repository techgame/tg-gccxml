#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from _ctypes_openal import *
from altypes import *
from alctypes import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Code generated from:
#~   "/System/Library/Frameworks/OpenAL.framework/Headers/alc.h"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ALCAPI = None # empty
ALCAPIENTRY = None # empty
# typedef ALCdevice
ALCdevice = ALCvoid
# typedef ALCcontext
ALCcontext = ALCvoid

#~ line: 34, skipped: 5 ~~~~~~

@bind(POINTER(c_ubyte), [c_void_p, ALCenum])
def alcGetString(device, param, _api_=None): 
    """alcGetString(device, param)
    
        device : c_void_p
        param : ALCenum
    """
    return _api_(device, param)
    
@bind(ALCvoid, [c_void_p, ALCenum, ALCsizei, POINTER(c_int)])
def alcGetIntegerv(device, param, size, data, _api_=None): 
    """alcGetIntegerv(device, param, size, data)
    
        device : c_void_p
        param : ALCenum
        size : ALCsizei
        data : POINTER(c_int)
    """
    return _api_(device, param, size, data)
    

@bind(c_void_p, [POINTER(c_ubyte)])
def alcOpenDevice(deviceName, _api_=None): 
    """alcOpenDevice(deviceName)
    
        deviceName : POINTER(c_ubyte)
    """
    return _api_(deviceName)
    
@bind(ALCvoid, [c_void_p])
def alcCloseDevice(device, _api_=None): 
    """alcCloseDevice(device)
    
        device : c_void_p
    """
    return _api_(device)
    

@bind(c_void_p, [c_void_p, POINTER(c_int)])
def alcCreateContext(device, attrList, _api_=None): 
    """alcCreateContext(device, attrList)
    
        device : c_void_p
        attrList : POINTER(c_int)
    """
    return _api_(device, attrList)
    
@bind(ALCboolean, [c_void_p])
def alcMakeContextCurrent(context, _api_=None): 
    """alcMakeContextCurrent(context)
    
        context : c_void_p
    """
    return _api_(context)
    
@bind(ALCvoid, [c_void_p])
def alcProcessContext(context, _api_=None): 
    """alcProcessContext(context)
    
        context : c_void_p
    """
    return _api_(context)
    
@bind(c_void_p, [])
def alcGetCurrentContext(_api_=None): 
    """alcGetCurrentContext()
    
        
    """
    return _api_()
    
@bind(c_void_p, [c_void_p])
def alcGetContextsDevice(context, _api_=None): 
    """alcGetContextsDevice(context)
    
        context : c_void_p
    """
    return _api_(context)
    
@bind(ALCvoid, [c_void_p])
def alcSuspendContext(context, _api_=None): 
    """alcSuspendContext(context)
    
        context : c_void_p
    """
    return _api_(context)
    
@bind(ALCvoid, [c_void_p])
def alcDestroyContext(context, _api_=None): 
    """alcDestroyContext(context)
    
        context : c_void_p
    """
    return _api_(context)
    

@bind(ALCenum, [c_void_p])
def alcGetError(device, _api_=None): 
    """alcGetError(device)
    
        device : c_void_p
    """
    return _api_(device)
    

@bind(ALCboolean, [c_void_p, POINTER(c_ubyte)])
def alcIsExtensionPresent(device, extName, _api_=None): 
    """alcIsExtensionPresent(device, extName)
    
        device : c_void_p
        extName : POINTER(c_ubyte)
    """
    return _api_(device, extName)
    
@bind(c_void_p, [c_void_p, POINTER(c_ubyte)])
def alcGetProcAddress(device, funcName, _api_=None): 
    """alcGetProcAddress(device, funcName)
    
        device : c_void_p
        funcName : POINTER(c_ubyte)
    """
    return _api_(device, funcName)
    
@bind(ALCenum, [c_void_p, POINTER(c_ubyte)])
def alcGetEnumValue(device, enumName, _api_=None): 
    """alcGetEnumValue(device, enumName)
    
        device : c_void_p
        enumName : POINTER(c_ubyte)
    """
    return _api_(device, enumName)
    


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ End of code generated from:
#~   "/System/Library/Frameworks/OpenAL.framework/Headers/alc.h"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

