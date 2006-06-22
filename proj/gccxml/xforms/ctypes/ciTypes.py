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

class TypeCodeItem(CodeItem):
    typeRefTemplate = '%s'

    def typeRef(self):
        return self.typeRefTemplate % (self.typeDecl(),)

    def typeDecl(self):
        return self.typeRefFor(self.item.type)

    def writeTo(self, stream):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIFundamentalType(TypeCodeItem):
    typeRefTemplate = '%s'

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

    def typeDecl(self):
        return self.typeMapping[self.item.name]

    def writeTo(self, stream):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CICvQualifiedType(TypeCodeItem):
    typeRefTemplate = '%s'

class CIPointerType(TypeCodeItem):
    typeRefTemplate = 'POINTER(%s)'

class CIReferenceType(CIPointerType):
    typeRefTemplate = 'REFERENCE(%s)'

class CIArrayType(TypeCodeItem):
    typeRefTemplate = 'ARRAY(%s)'
    # TODO: Implement CIArrayType

class CITypedef(TypeCodeItem):
    typeRefTemplate = '%s'
    template = 'class %(typedefName)s(%(typeRef)s): pass'

    def typeDecl(self):
        return self.item.name

    def writeTo(self, stream):
        print >> stream, self.typedefDecl()

    def typedefDecl(self):
        typeRef = self.typeRefFor(self.item.type)

        # TODO: handle typedef of void more elegantly
        if typeRef != 'None':
            return self.template % dict(
                    typedefName=self.item.name,
                    typeRef=typeRef,)
        else:
            return '%s = %s' % (self.item.name, typeRef)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIEnumeration(TypeCodeItem):
    typeRefTemplate = 'ENUM(%s)'
    # TODO: Implement CIEnumeration Type

class CIEnumValue(CodeItem):
    pass
    # TODO: Implement CIEnumValue

