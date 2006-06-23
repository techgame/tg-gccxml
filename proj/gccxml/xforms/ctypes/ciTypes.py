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
    _required = False
    typeRefTemplate = '%s'

    def typeRef(self, require=True):
        if require: self.require()
        return self.typeRefTemplate % (self._typeDecl(),)

    def ptrTypeRef(self):
        typeRef = self.typeRef(False)
        if typeRef is None:
            return 'c_void_p'
        else:
            return 'POINTER(%s)' % (typeRef,)

    def _typeDecl(self):
        return self.typeRefFor(self.item.type)

    def writeTo(self, stream):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIFundamentalType(TypeCodeItem):
    pointerTempalte = 'POINTER(%s)'
    typeRefTemplate = '%s'

    typeMapping = {
        # gccxml name: ctypes

        # void
        'void': None,
        'void *': 'c_void_p',

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

    def _typeDecl(self):
        return self._typeDeclFor(self.item.name)
    def _typeDeclFor(klass, typeName):
        return klass.typeMapping[typeName]

    def ptrTypeRef(self):
        typeName = self.item.name
        r = self._ptrTypeRefFor(typeName)
        if r is None:
            typeRef = self._typeDeclFor(typeName)
            r = self.pointerTempalte % (typeRef,)
        return r
    def _ptrTypeRefFor(klass, typeName):
        return klass.typeMapping.get(typeName+' *', None)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def writeTo(self, stream):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CICvQualifiedType(TypeCodeItem):
    typeRefTemplate = '%s'

class CIPointerType(TypeCodeItem):
    typeRefTemplate = '%s'

    def _typeDecl(self):
        return self.ptrTypeRefFor(self.item.type)

class CIReferenceType(CIPointerType):
    typeRefTemplate = 'REFERENCE(%s)'

class CIArrayType(TypeCodeItem):
    typeRefTemplate = 'ARRAY(%s)'
    # TODO: Implement CIArrayType

class CITypedef(TypeCodeItem):
    typeRefTemplate = '%s'
    template = 'class %(typedefName)s(%(typeRef)s): pass'

    def _typeDecl(self):
        return self.item.name

    def writeTo(self, stream):
        print >> stream, self.typedefDecl()

    def typedefDecl(self):
        itemType = self.item.type
        typeRef = self.typeRefFor(itemType)
        if itemType.isFundamentalType():
            if typeRef not in ('None', None):
                return self.template % dict(
                        typedefName=self._typeDecl(),
                        typeRef=typeRef,)

        return '%s = %s # typedef' % (self._typeDecl(), typeRef)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIEnumeration(TypeCodeItem):
    typeRefTemplate = '%s'
    template = 'class %(enumName)s(c_int):'

    def _typeDecl(self):
        return self.item.name

    def writeTo(self, stream):
        print >> stream, self.enumDecl()
        stream.indent()
        for enum in self.item.enumValues:
            enum.codeItem.writeTo(stream)
        stream.dedent()

    def enumDecl(self):
        return self.template % dict(
                enumName=self._typeDecl(),
                typeRef=self.typeRef,)
    
    def add(self, ciEnumValue):
        pass

class CIEnumValue(CodeItem):
    def writeTo(self, stream):
        print >> stream, '%s = %s' % (self.item.name, self.item.value)

    def getHostCI(self):
        return self.item.host.codeItem

