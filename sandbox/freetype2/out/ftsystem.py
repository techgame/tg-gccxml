#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from _ctypes_freetype import *
from fttypes import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Code generated from:
#~   "/usr/local/include/freetype2/freetype/ftsystem.h"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

FT_Memory = POINTER("FT_MemoryRec_") # typedef FT_Memory

FT_Alloc_Func = POINTER(CFUNCTYPE(FT_Pointer, FT_Memory, FT_Fixed)) # typedef FT_Alloc_Func

FT_Free_Func = POINTER(CFUNCTYPE(None, FT_Memory, FT_Pointer)) # typedef FT_Free_Func

FT_Realloc_Func = POINTER(CFUNCTYPE(FT_Pointer, FT_Memory, FT_Fixed, FT_Fixed, FT_Pointer)) # typedef FT_Realloc_Func

class FT_MemoryRec_(Structure):
    _fields_ = [
        ("user", FT_Pointer),
        ("alloc", FT_Alloc_Func),
        ("free", FT_Free_Func),
        ("realloc", FT_Realloc_Func),
        ]
FT_Memory.set_type(FT_MemoryRec_)

FT_Stream = POINTER("FT_StreamRec_") # typedef FT_Stream

class FT_StreamDesc_(Union):
    _fields_ = [
        ("value", FT_Fixed),
        ("pointer", FT_Pointer),
        ]

FT_StreamDesc = FT_StreamDesc_ # typedef FT_StreamDesc

FT_Stream_IoFunc = POINTER(CFUNCTYPE(FT_ULong, FT_Stream, FT_ULong, POINTER(c_ubyte), FT_ULong)) # typedef FT_Stream_IoFunc

FT_Stream_CloseFunc = POINTER(CFUNCTYPE(None, FT_Stream)) # typedef FT_Stream_CloseFunc

class FT_StreamRec_(Structure):
    _fields_ = [
        ("base", POINTER(c_ubyte)),
        ("size", FT_ULong),
        ("pos", FT_ULong),
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

