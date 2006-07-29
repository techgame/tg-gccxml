#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from _ctypes_openal import *
from altypes import *
from alctypes import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Code generated from:
#~   "/System/Library/Frameworks/OpenAL.framework/Headers/alut.h"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ALUTAPI = None # empty
ALUTAPIENTRY = None # empty

#~ line: 39, skipped: 14 ~~~~~~

@bind(ALvoid, [POINTER(c_int), c_char_p])
def alutInit(argc, argv, _api_=None): 
    """alutInit(argc, argv)
    
        argc : POINTER(c_int)
        argv : c_char_p
    """
    return _api_(argc, argv)
    
@bind(ALvoid, [])
def alutExit(_api_=None): 
    """alutExit()
    
        
    """
    return _api_()
    
@bind(ALvoid, [c_char_p, POINTER(c_int), c_void_p, POINTER(c_uint), POINTER(c_uint)])
def alutLoadWAVFile(file, format, data, size, freq, _api_=None): 
    """alutLoadWAVFile(file, format, data, size, freq)
    
        file : c_char_p
        format : POINTER(c_int)
        data : c_void_p
        size : POINTER(c_uint)
        freq : POINTER(c_uint)
    """
    return _api_(file, format, data, size, freq)
    
@bind(ALvoid, [c_char_p, POINTER(c_int), c_void_p, POINTER(c_uint), POINTER(c_uint)])
def alutLoadWAVMemory(memory, format, data, size, freq, _api_=None): 
    """alutLoadWAVMemory(memory, format, data, size, freq)
    
        memory : c_char_p
        format : POINTER(c_int)
        data : c_void_p
        size : POINTER(c_uint)
        freq : POINTER(c_uint)
    """
    return _api_(memory, format, data, size, freq)
    
@bind(ALvoid, [ALenum, c_void_p, ALsizei, ALsizei])
def alutUnloadWAV(format, data, size, freq, _api_=None): 
    """alutUnloadWAV(format, data, size, freq)
    
        format : ALenum
        data : c_void_p
        size : ALsizei
        freq : ALsizei
    """
    return _api_(format, data, size, freq)
    


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ End of code generated from:
#~   "/System/Library/Frameworks/OpenAL.framework/Headers/alut.h"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

