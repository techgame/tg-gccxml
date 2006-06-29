#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from ctypes import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Code generated from:
#~   "/usr/local/include/freetype2/freetype/ftimage.h"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FT_Pos(c_long):
    """typedef FT_Pos"""

class FT_Vector_(Structure):
    _fields_ = [
        ("x", FT_Pos),
        ("y", FT_Pos),
        ]

FT_Vector = FT_Vector_ # typedef FT_Vector

class FT_BBox_(Structure):
    _fields_ = [
        ("xMin", FT_Pos),
        ("yMin", FT_Pos),
        ("xMax", FT_Pos),
        ("yMax", FT_Pos),
        ]

FT_BBox = FT_BBox_ # typedef FT_BBox

class FT_Bitmap_(Structure):
    _fields_ = [
        ("rows", c_int),
        ("width", c_int),
        ("pitch", c_int),
        ("buffer", POINTER(c_ubyte)),
        ("num_grays", c_short),
        ("pixel_mode", c_char),
        ("palette_mode", c_char),
        ("palette", c_void_p),
        ]

FT_Bitmap = FT_Bitmap_ # typedef FT_Bitmap

class FT_Outline_(Structure):
    _fields_ = [
        ("n_contours", c_short),
        ("n_points", c_short),
        ("points", POINTER(FT_Vector)),
        ("tags", POINTER(c_char)),
        ("contours", POINTER(c_short)),
        ("flags", c_int),
        ]

FT_Outline = FT_Outline_ # typedef FT_Outline

class FT_Glyph_Format_(c_int):
    FT_GLYPH_FORMAT_NONE = 0
    FT_GLYPH_FORMAT_COMPOSITE = 1668246896
    FT_GLYPH_FORMAT_BITMAP = 1651078259
    FT_GLYPH_FORMAT_OUTLINE = 1869968492
    FT_GLYPH_FORMAT_PLOTTER = 1886154612

FT_Glyph_Format = FT_Glyph_Format_ # typedef FT_Glyph_Format

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ End of code generated from:
#~   "/usr/local/include/freetype2/freetype/ftimage.h"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

