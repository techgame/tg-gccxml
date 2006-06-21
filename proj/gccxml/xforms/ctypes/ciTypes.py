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

from ciBase import CodeItem

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CIFundamentalType = None
CICvQualifiedType = None
CIEnumeration = None
CIEnumValue = None
CITypedef = None
CIPointerType = None
CIReferenceType = None
CIArrayType = None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Specific Code Item Generators
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIFundamentalType(CodeItem):
    typeMapping = {
        # gccxml name: ctypes

        # void
        'void': None,

        # char
        'char': 'c_char',

        'signed char': 'c_byte',
        'unsigned char': 'c_ubyte',

        # short
        'short int': 'c_short',
        'short unsigned int': 'c_ushort',

        # int
        'int': 'c_int',
        'unsigned int': 'c_uint',

        # long int
        'long int': 'c_long',
        'long unsigned int': 'c_ulong',

        # long longs
        'long long': 'c_longlong',
        'long long unsigned long': 'c_ulonglong',


        # float & double
        'float': 'c_float',
        'double': 'c_double',

        # a temporary ctypes oversite?
        'long double': None,


        # how do these come about?
        'complex float': None,
        'complex double': None,
        'complex long double': None,
    }
    def codeRef(self):
        return self.item.name
    def codeDef(self):
        return self.item.name

class CIDecorated(CodeItem):
    def codeRef(self):
        return self.referenceFor(self.item.type)
    def codeDef(self):
        return ''

class CIPointer(CodeItem):
    def codeRef(self):
        itemType = self.item.type
        ref = self.referenceFor(itemType)
        if hasattr(itemType, 'name'):
            return ref + '.ptr'
        else:
            return 'POINTER(%s)' % (ref,)
    def codeDef(self):
        ref = self.referenceFor(self.item.type)
        return '%s.ptr = POINTER(%s)\n' % (ref, ref)

class CITypedef(CodeItem):
    def codeRef(self):
        return self.item.name
    def codeDef(self):
        item = self.item
        if item.type.isFundamentalType():
            return 'class %(name)s(%(typeName)): pass' % dict(name=item.name, typeName=item.type.name)

