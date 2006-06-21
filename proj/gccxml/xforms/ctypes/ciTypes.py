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
        return self.typeMapping[self.item.name]
    def codeDef(self):
        return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CICvQualifiedType(CodeItem):
    def codeRef(self):
        return self.refFor(self.item.type)
    def codeDef(self):
        return self.codeFor(self.item.type)

class CIPointerType(CodeItem):
    template = (
        '%(name)s.ptr = POINTER(%(name)s)'
        )

    def codeRef(self):
        itemType = self.item.type
        ref = self.refFor(itemType)
        if hasattr(itemType, 'name'):
            return ref + '.ptr'
        else:
            return 'POINTER(%s)' % (ref,)
    def codeDef(self):
        itemType = self.item.type
        ref = self.refFor(itemType)
        if hasattr(itemType, 'name'):
            return self.template % dict(
                    name=ref,
                    )
        else:
            return None

class CIReferenceType(CIPointerType):
    pass

class CITypedef(CodeItem):
    template = 'class %(name)s(%(typeName)s): pass'

    def codeRef(self):
        return self.item.name
    def codeDef(self):
        item = self.item
        if item.type.isFundamentalType():
            return self.template % dict(
                    name=self.ref(), 
                    typeName=self.refFor(item.type),
                    )

class CIArrayType(CodeItem):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIEnumeration(CodeItem):
    pass

class CIEnumValue(CodeItem):
    pass

