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
    #_required = False
    typeRefTemplate = '%s'
    ciTypedefs = ()

    def typeRef(self, require=True):
        if require: self.require()

        result = self.typeRefFromTypedef()
        if result: return result

        return self.typeRefNoTypedef()

    def typeRefNoTypedef(self):
        return self.typeRefTemplate % (self._typeDecl(),)

    def _typeDecl(self):
        return self.typeRefFor(self.item.type)

    def ptrTypeRefFrom(self, ciPtrType):
        typeRef = self.typeRef(False)
        if typeRef is None:
            return 'c_void_p'
        else:
            return 'POINTER(%s)' % (typeRef,)

    def getCIBasicType(self):
        return self.item.basicType.codeItem

    def typeRefFromTypedef(self):
        if self.ciTypedefs:
            return self.ciTypedefs[0].typeRef()
    def addTypedef(self, ciTypedef):
        if not self.ciTypedefs:
            self.ciTypedefs = [ciTypedef]
        else:
            self.ciTypedefs.append(ciTypedef)

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
        'char *': 'c_char_p',

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

    def isValidCodeItem(self):
        return True

    def _typeDecl(self):
        return self._typeDeclFor(self.item.name)
    def _typeDeclFor(klass, typeName):
        return klass.typeMapping[typeName]

    def ptrTypeRefFrom(self, ciPtrType):
        typeName = self.item.name
        r = self._ptrTypeRefFor(typeName)
        if r is None:
            typeRef = self._typeDeclFor(typeName)
            r = self.pointerTempalte % (typeRef,)
        return r
    def _ptrTypeRefFor(klass, typeName):
        return klass.typeMapping.get(typeName+' *', None)

    def typeRefFromTypedef(self):
        # we might have multiple typedefs for fundamental types
        return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def writeTo(self, stream):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CICvQualifiedType(TypeCodeItem):
    typeRefTemplate = '%s'

    def isValidCodeItem(self):
        return True

    def _typeDecl(self):
        return self.typeRefFor(self.item.type)

    def ptrTypeRefFrom(self, ciPtrType):
        return self.ptrTypeRefFor(self.item.type, ciPtrType)
        

class CIPointerType(TypeCodeItem):
    typeRefTemplate = '%s'

    def isValidCodeItem(self):
        return True

    _forwardType = False
    def getForwardType(self):
        return self._forwardType
    def setForwardType(self, forwardType=True):
        self._forwardType = forwardType
    isForwardType = property(getForwardType, setForwardType)

    def _typeDecl(self):
        ptrTypeRef = self.ptrTypeRefFor(self.item.type, self)
        return ptrTypeRef

# In case someone uses references in C code accidentally
CIReferenceType = CIPointerType

class CIArrayType(TypeCodeItem):
    typeRefTemplate = '%s'

    def _typeDecl(self):
        itype = TypeCodeItem._typeDecl(self)
        return '(%d*%s)' % (self.item.size, itype)

    def ptrTypeRefFrom(self, ciPtrType):
        return self.ptrTypeRefFor(self.item.type, ciPtrType)

class CITypedef(TypeCodeItem):
    typeRefTemplate = '%s'
    typedefTemplate = '# %(comment)s\n%(name)s = %(typeRef)s'
    fundamentTypeTemplate = typedefTemplate
    #fundamentTypeTemplate = 'class %(name)s(%(typeRef)s):\n    """%(comment)s"""'
    
    comment = 'typedef %(name)s'
    missingComment = ' as %(basicTypeRef)s for absent %(origTypeRef)s'

    def _typeDecl(self):
        return self.item.name

    def writeTo(self, stream):
        print >> stream, self.typedefDecl()

        ciBasicType = self.getCIBasicType()
        if not ciBasicType.ciTypedefs:
            ciBasicType.ciTypedefs = [self]
        else:
            ciBasicType.ciTypedefs.append(self)

    def ptrTypeRefFrom(self, ciPtrType):
        if self.item.type.isFundamentalType():
            return self.ptrTypeRefFor(self.item.type, ciPtrType)
        else:
            return TypeCodeItem.ptrTypeRefFrom(self, ciPtrType)

    def typedefDecl(self, itemType=None):
        if itemType is None:
            itemType = self.item.type
            if itemType is None:
                print self.item.name

        if itemType.isFundamentalType():
            return self.typedefDeclFundamentalType(itemType)
        elif itemType.isPointerType():
            return self.typedefDeclPointerType(itemType)
        else:
            return self.typedefDeclSimple(itemType)

    def typedefDeclSimple(self, itemType):
        if not getattr(itemType, 'codeItem', None):
            return self.typedefDeclMissingType(itemType)

        kw = dict(
                name=self._typeDecl(),
                typeRef=self.typeRefFor(itemType),)
        kw.update(comment=self.comment % kw)

        return self.typedefTemplate % kw

    def typedefDeclFundamentalType(self, itemType):
        if itemType.isVoidType():
            return self.typedefDeclSimple(itemType)

        kw = dict(
                name=self._typeDecl(),
                typeRef=self.typeRefFor(itemType),)
        kw.update(comment=self.comment % kw)
        return self.fundamentTypeTemplate % kw

    def typedefDeclPointerType(self, itemType):
        ciPointer = itemType.codeItem

        basicType = itemType.type.basicType
        if basicType.file is self.file:
            if basicType.line > self.line:
                ciPointer.setForwardType()
        return self.typedefDeclSimple(itemType)

    def typedefDeclMissingType(self, itemType):
        basicItemType = itemType.basicType
        if basicItemType is itemType:
            kw = dict(name=self._typeDecl(), itemType=itemType)
            return '# WARNING: typedef %(name)s for missing type %(itemType)r' % kw
            
        kw = dict(
                origTypeRef=self.typeRefFor(itemType), 
                basicTypeRef=self.typeRefFor(basicItemType))
        self.comment += self.missingComment % kw
        return self.typedefDecl(basicItemType)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIEnumeration(TypeCodeItem):
    typeRefTemplate = '%s'
    template = "class %(enumName)s(c_int):\n    '''enum %(enumName)s''' "

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

