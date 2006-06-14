##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2006  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import ctypes

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class c_void(ctypes.c_int): 
    pass

basicTypeCodeMap = {
    # gccxml name: ctypes
    'void': c_void,

    'char': ctypes.c_char,

    'signed char': ctypes.c_byte,
    'unsigned char': ctypes.c_ubyte,

    'short int': ctypes.c_short,
    'short unsigned int': ctypes.c_ushort,

    'int': ctypes.c_int,
    'unsigned int': ctypes.c_uint,

    'long int': ctypes.c_long,
    'long unsigned int': ctypes.c_ulong,

    'long long': ctypes.c_longlong,
    'long long unsigned long': ctypes.c_ulonglong,

    'float': ctypes.c_float,
    'double': ctypes.c_double,

    # a temporary ctypes oversite?
    'long double': None,

    # how do these come about?
    'complex float': None,
    'complex double': None,
    'complex long double': None,
    }

