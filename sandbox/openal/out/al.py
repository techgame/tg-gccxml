#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from _ctypes_openal import *
from altypes import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Code generated from:
#~   "/System/Library/Frameworks/OpenAL.framework/Headers/al.h"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ALAPI = None # empty
ALAPIENTRY = None # empty
AL_CALLBACK = None # empty

#~ line: 62, skipped: 16 ~~~~~~

@bind(ALvoid, [ALenum])
def alEnable(capability, _api_=None): 
    """alEnable(capability)
    
        capability : ALenum
    """
    return _api_(capability)
    
@bind(ALvoid, [ALenum])
def alDisable(capability, _api_=None): 
    """alDisable(capability)
    
        capability : ALenum
    """
    return _api_(capability)
    
@bind(ALboolean, [ALenum])
def alIsEnabled(capability, _api_=None): 
    """alIsEnabled(capability)
    
        capability : ALenum
    """
    return _api_(capability)
    

@bind(ALvoid, [ALenum, ALenum])
def alHint(target, mode, _api_=None): 
    """alHint(target, mode)
    
        target : ALenum
        mode : ALenum
    """
    return _api_(target, mode)
    

@bind(ALboolean, [ALenum])
def alGetBoolean(param, _api_=None): 
    """alGetBoolean(param)
    
        param : ALenum
    """
    return _api_(param)
    
@bind(ALint, [ALenum])
def alGetInteger(param, _api_=None): 
    """alGetInteger(param)
    
        param : ALenum
    """
    return _api_(param)
    
@bind(ALfloat, [ALenum])
def alGetFloat(param, _api_=None): 
    """alGetFloat(param)
    
        param : ALenum
    """
    return _api_(param)
    
@bind(ALdouble, [ALenum])
def alGetDouble(param, _api_=None): 
    """alGetDouble(param)
    
        param : ALenum
    """
    return _api_(param)
    
@bind(ALvoid, [ALenum, c_char_p])
def alGetBooleanv(param, data, _api_=None): 
    """alGetBooleanv(param, data)
    
        param : ALenum
        data : c_char_p
    """
    return _api_(param, data)
    
@bind(ALvoid, [ALenum, POINTER(c_int)])
def alGetIntegerv(param, data, _api_=None): 
    """alGetIntegerv(param, data)
    
        param : ALenum
        data : POINTER(c_int)
    """
    return _api_(param, data)
    
@bind(ALvoid, [ALenum, POINTER(c_float)])
def alGetFloatv(param, data, _api_=None): 
    """alGetFloatv(param, data)
    
        param : ALenum
        data : POINTER(c_float)
    """
    return _api_(param, data)
    
@bind(ALvoid, [ALenum, POINTER(c_double)])
def alGetDoublev(param, data, _api_=None): 
    """alGetDoublev(param, data)
    
        param : ALenum
        data : POINTER(c_double)
    """
    return _api_(param, data)
    
@bind(POINTER(c_ubyte), [ALenum])
def alGetString(param, _api_=None): 
    """alGetString(param)
    
        param : ALenum
    """
    return _api_(param)
    

@bind(ALvoid, [ALenum, ALint])
def alSetInteger(pname, value, _api_=None): 
    """alSetInteger(pname, value)
    
        pname : ALenum
        value : ALint
    """
    return _api_(pname, value)
    
@bind(ALvoid, [ALenum, ALdouble])
def alSetDouble(pname, value, _api_=None): 
    """alSetDouble(pname, value)
    
        pname : ALenum
        value : ALdouble
    """
    return _api_(pname, value)
    

#~ line: 87, skipped: 6 ~~~~~~

@bind(ALenum, [])
def alGetError(_api_=None): 
    """alGetError()
    
        
    """
    return _api_()
    

#~ line: 95, skipped: 8 ~~~~~~

@bind(ALboolean, [POINTER(c_ubyte)])
def alIsExtensionPresent(fname, _api_=None): 
    """alIsExtensionPresent(fname)
    
        fname : POINTER(c_ubyte)
    """
    return _api_(fname)
    

#~ line: 103, skipped: 8 ~~~~~~

@bind(c_void_p, [POINTER(c_ubyte)])
def alGetProcAddress(fname, _api_=None): 
    """alGetProcAddress(fname)
    
        fname : POINTER(c_ubyte)
    """
    return _api_(fname)
    

#~ line: 110, skipped: 7 ~~~~~~

@bind(ALenum, [POINTER(c_ubyte)])
def alGetEnumValue(ename, _api_=None): 
    """alGetEnumValue(ename)
    
        ename : POINTER(c_ubyte)
    """
    return _api_(ename)
    

#~ line: 130, skipped: 20 ~~~~~~

@bind(ALvoid, [ALenum, ALint])
def alListeneri(param, value, _api_=None): 
    """alListeneri(param, value)
    
        param : ALenum
        value : ALint
    """
    return _api_(param, value)
    

#~ line: 137, skipped: 7 ~~~~~~

@bind(ALvoid, [ALenum, ALfloat])
def alListenerf(param, value, _api_=None): 
    """alListenerf(param, value)
    
        param : ALenum
        value : ALfloat
    """
    return _api_(param, value)
    

#~ line: 145, skipped: 8 ~~~~~~

@bind(ALvoid, [ALenum, ALfloat, ALfloat, ALfloat])
def alListener3f(param, v1, v2, v3, _api_=None): 
    """alListener3f(param, v1, v2, v3)
    
        param : ALenum
        v1 : ALfloat
        v2 : ALfloat
        v3 : ALfloat
    """
    return _api_(param, v1, v2, v3)
    

#~ line: 154, skipped: 9 ~~~~~~

@bind(ALvoid, [ALenum, POINTER(c_float)])
def alListenerfv(param, values, _api_=None): 
    """alListenerfv(param, values)
    
        param : ALenum
        values : POINTER(c_float)
    """
    return _api_(param, values)
    

@bind(ALvoid, [ALenum, POINTER(c_int)])
def alGetListeneri(param, value, _api_=None): 
    """alGetListeneri(param, value)
    
        param : ALenum
        value : POINTER(c_int)
    """
    return _api_(param, value)
    
@bind(ALvoid, [ALenum, POINTER(c_float)])
def alGetListenerf(param, value, _api_=None): 
    """alGetListenerf(param, value)
    
        param : ALenum
        value : POINTER(c_float)
    """
    return _api_(param, value)
    
@bind(ALvoid, [ALenum, POINTER(c_float), POINTER(c_float), POINTER(c_float)])
def alGetListener3f(param, v1, v2, v3, _api_=None): 
    """alGetListener3f(param, v1, v2, v3)
    
        param : ALenum
        v1 : POINTER(c_float)
        v2 : POINTER(c_float)
        v3 : POINTER(c_float)
    """
    return _api_(param, v1, v2, v3)
    
@bind(ALvoid, [ALenum, POINTER(c_float)])
def alGetListenerfv(param, values, _api_=None): 
    """alGetListenerfv(param, values)
    
        param : ALenum
        values : POINTER(c_float)
    """
    return _api_(param, values)
    

#~ line: 174, skipped: 15 ~~~~~~

@bind(ALvoid, [ALsizei, POINTER(c_uint)])
def alGenSources(n, sources, _api_=None): 
    """alGenSources(n, sources)
    
        n : ALsizei
        sources : POINTER(c_uint)
    """
    return _api_(n, sources)
    

@bind(ALvoid, [ALsizei, POINTER(c_uint)])
def alDeleteSources(n, sources, _api_=None): 
    """alDeleteSources(n, sources)
    
        n : ALsizei
        sources : POINTER(c_uint)
    """
    return _api_(n, sources)
    

@bind(ALboolean, [ALuint])
def alIsSource(id, _api_=None): 
    """alIsSource(id)
    
        id : ALuint
    """
    return _api_(id)
    

@bind(ALvoid, [ALuint, ALenum, ALint])
def alSourcei(source, param, value, _api_=None): 
    """alSourcei(source, param, value)
    
        source : ALuint
        param : ALenum
        value : ALint
    """
    return _api_(source, param, value)
    
@bind(ALvoid, [ALuint, ALenum, ALfloat])
def alSourcef(source, param, value, _api_=None): 
    """alSourcef(source, param, value)
    
        source : ALuint
        param : ALenum
        value : ALfloat
    """
    return _api_(source, param, value)
    
@bind(ALvoid, [ALuint, ALenum, ALfloat, ALfloat, ALfloat])
def alSource3f(source, param, v1, v2, v3, _api_=None): 
    """alSource3f(source, param, v1, v2, v3)
    
        source : ALuint
        param : ALenum
        v1 : ALfloat
        v2 : ALfloat
        v3 : ALfloat
    """
    return _api_(source, param, v1, v2, v3)
    
@bind(ALvoid, [ALuint, ALenum, POINTER(c_float)])
def alSourcefv(source, param, values, _api_=None): 
    """alSourcefv(source, param, values)
    
        source : ALuint
        param : ALenum
        values : POINTER(c_float)
    """
    return _api_(source, param, values)
    

@bind(ALvoid, [ALuint, ALenum, POINTER(c_int)])
def alGetSourcei(source, param, value, _api_=None): 
    """alGetSourcei(source, param, value)
    
        source : ALuint
        param : ALenum
        value : POINTER(c_int)
    """
    return _api_(source, param, value)
    
@bind(ALvoid, [ALuint, ALenum, POINTER(c_float)])
def alGetSourcef(source, param, value, _api_=None): 
    """alGetSourcef(source, param, value)
    
        source : ALuint
        param : ALenum
        value : POINTER(c_float)
    """
    return _api_(source, param, value)
    
@bind(ALvoid, [ALuint, ALenum, POINTER(c_float), POINTER(c_float), POINTER(c_float)])
def alGetSource3f(source, param, v1, v2, v3, _api_=None): 
    """alGetSource3f(source, param, v1, v2, v3)
    
        source : ALuint
        param : ALenum
        v1 : POINTER(c_float)
        v2 : POINTER(c_float)
        v3 : POINTER(c_float)
    """
    return _api_(source, param, v1, v2, v3)
    
@bind(ALvoid, [ALuint, ALenum, POINTER(c_float)])
def alGetSourcefv(source, param, values, _api_=None): 
    """alGetSourcefv(source, param, values)
    
        source : ALuint
        param : ALenum
        values : POINTER(c_float)
    """
    return _api_(source, param, values)
    

@bind(ALvoid, [ALsizei, POINTER(c_uint)])
def alSourcePlayv(n, sources, _api_=None): 
    """alSourcePlayv(n, sources)
    
        n : ALsizei
        sources : POINTER(c_uint)
    """
    return _api_(n, sources)
    
@bind(ALvoid, [ALsizei, POINTER(c_uint)])
def alSourcePausev(n, sources, _api_=None): 
    """alSourcePausev(n, sources)
    
        n : ALsizei
        sources : POINTER(c_uint)
    """
    return _api_(n, sources)
    
@bind(ALvoid, [ALsizei, POINTER(c_uint)])
def alSourceStopv(n, sources, _api_=None): 
    """alSourceStopv(n, sources)
    
        n : ALsizei
        sources : POINTER(c_uint)
    """
    return _api_(n, sources)
    
@bind(ALvoid, [ALsizei, POINTER(c_uint)])
def alSourceRewindv(n, sources, _api_=None): 
    """alSourceRewindv(n, sources)
    
        n : ALsizei
        sources : POINTER(c_uint)
    """
    return _api_(n, sources)
    

@bind(ALvoid, [ALuint])
def alSourcePlay(source, _api_=None): 
    """alSourcePlay(source)
    
        source : ALuint
    """
    return _api_(source)
    

#~ line: 206, skipped: 6 ~~~~~~

@bind(ALvoid, [ALuint])
def alSourcePause(source, _api_=None): 
    """alSourcePause(source)
    
        source : ALuint
    """
    return _api_(source)
    

#~ line: 215, skipped: 9 ~~~~~~

@bind(ALvoid, [ALuint])
def alSourceStop(source, _api_=None): 
    """alSourceStop(source)
    
        source : ALuint
    """
    return _api_(source)
    

#~ line: 222, skipped: 7 ~~~~~~

@bind(ALvoid, [ALuint])
def alSourceRewind(source, _api_=None): 
    """alSourceRewind(source)
    
        source : ALuint
    """
    return _api_(source)
    

#~ line: 240, skipped: 18 ~~~~~~

@bind(ALvoid, [ALsizei, POINTER(c_uint)])
def alGenBuffers(n, buffers, _api_=None): 
    """alGenBuffers(n, buffers)
    
        n : ALsizei
        buffers : POINTER(c_uint)
    """
    return _api_(n, buffers)
    
@bind(ALvoid, [ALsizei, POINTER(c_uint)])
def alDeleteBuffers(n, buffers, _api_=None): 
    """alDeleteBuffers(n, buffers)
    
        n : ALsizei
        buffers : POINTER(c_uint)
    """
    return _api_(n, buffers)
    
@bind(ALboolean, [ALuint])
def alIsBuffer(buffer, _api_=None): 
    """alIsBuffer(buffer)
    
        buffer : ALuint
    """
    return _api_(buffer)
    

#~ line: 251, skipped: 9 ~~~~~~

@bind(ALvoid, [ALuint, ALenum, c_void_p, ALsizei, ALsizei])
def alBufferData(buffer, format, data, size, freq, _api_=None): 
    """alBufferData(buffer, format, data, size, freq)
    
        buffer : ALuint
        format : ALenum
        data : c_void_p
        size : ALsizei
        freq : ALsizei
    """
    return _api_(buffer, format, data, size, freq)
    

@bind(ALvoid, [ALuint, ALenum, POINTER(c_int)])
def alGetBufferi(buffer, param, value, _api_=None): 
    """alGetBufferi(buffer, param, value)
    
        buffer : ALuint
        param : ALenum
        value : POINTER(c_int)
    """
    return _api_(buffer, param, value)
    
@bind(ALvoid, [ALuint, ALenum, POINTER(c_float)])
def alGetBufferf(buffer, param, value, _api_=None): 
    """alGetBufferf(buffer, param, value)
    
        buffer : ALuint
        param : ALenum
        value : POINTER(c_float)
    """
    return _api_(buffer, param, value)
    

#~ line: 264, skipped: 9 ~~~~~~

@bind(ALvoid, [ALuint, ALsizei, POINTER(c_uint)])
def alSourceQueueBuffers(source, n, buffers, _api_=None): 
    """alSourceQueueBuffers(source, n, buffers)
    
        source : ALuint
        n : ALsizei
        buffers : POINTER(c_uint)
    """
    return _api_(source, n, buffers)
    
@bind(ALvoid, [ALuint, ALsizei, POINTER(c_uint)])
def alSourceUnqueueBuffers(source, n, buffers, _api_=None): 
    """alSourceUnqueueBuffers(source, n, buffers)
    
        source : ALuint
        n : ALsizei
        buffers : POINTER(c_uint)
    """
    return _api_(source, n, buffers)
    

#~ line: 270, skipped: 5 ~~~~~~

@bind(ALvoid, [ALenum])
def alDistanceModel(value, _api_=None): 
    """alDistanceModel(value)
    
        value : ALenum
    """
    return _api_(value)
    
@bind(ALvoid, [ALfloat])
def alDopplerFactor(value, _api_=None): 
    """alDopplerFactor(value)
    
        value : ALfloat
    """
    return _api_(value)
    
@bind(ALvoid, [ALfloat])
def alDopplerVelocity(value, _api_=None): 
    """alDopplerVelocity(value)
    
        value : ALfloat
    """
    return _api_(value)
    


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ End of code generated from:
#~   "/System/Library/Frameworks/OpenAL.framework/Headers/al.h"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

