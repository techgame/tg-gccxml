#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from _ctypes_freetype import *
from fttypes import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Code generated from:
#~   "/usr/local/include/freetype2/freetype/ftsystem.h"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# typedef FT_Memory
FT_Memory = POINTER("FT_MemoryRec_")

# typedef FT_Alloc_Func
FT_Alloc_Func = c_void_p

# typedef FT_Free_Func
FT_Free_Func = c_void_p

# typedef FT_Realloc_Func
FT_Realloc_Func = c_void_p

class FT_MemoryRec_(Structure):
    _fields_ = [
        ("user", c_void_p),
        ("alloc", FT_Alloc_Func),
        ("free", FT_Free_Func),
        ("realloc", FT_Realloc_Func),
        ]
FT_Memory.set_type(FT_MemoryRec_)

# typedef FT_Stream
FT_Stream = POINTER("FT_StreamRec_")

class FT_StreamDesc_(Union):
    _fields_ = [
        ("value", c_long),
        ("pointer", c_void_p),
        ]

# typedef FT_StreamDesc
FT_StreamDesc = FT_StreamDesc_

# typedef FT_Stream_IoFunc
FT_Stream_IoFunc = POINTER(c_ulong)

# typedef FT_Stream_CloseFunc
FT_Stream_CloseFunc = c_void_p

class FT_StreamRec_(Structure):
    _fields_ = [
        ("base", POINTER(c_ubyte)),
        ("size", c_ulong),
        ("pos", c_ulong),
        ("descriptor", FT_StreamDesc),
        ("pathname", FT_StreamDesc),
        ("read", FT_Stream_IoFunc),
        ("close", FT_Stream_CloseFunc),
        ("memory", FT_Memory),
        ("cursor", POINTER(c_ubyte)),
        ("limit", POINTER(c_ubyte)),
        ]
FT_Stream.set_type(FT_StreamRec_)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ End of code generated from:
#~   "/usr/local/include/freetype2/freetype/ftsystem.h"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

