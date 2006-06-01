##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2005  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import xml.sax
import xml.sax.handler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ModelAtomVisitor(object):
    # root reference
    def onRoot(self, item, *args, **kw): pass

    # file references
    def onFile(self, item, *args, **kw): pass

    # simple types
    def onType(self, item, *args, **kw): pass
    def onFundamentalType(self, item, *args, **kw): pass
    def onCvQualifiedType(self, item, *args, **kw): pass
    def onEnumeration(self, item, *args, **kw): pass
    def onEnumValue(self, item, *args, **kw): pass

    # complex types and pointers
    def onTypedef(self, item, *args, **kw): pass
    def onPointerType(self, item, *args, **kw): pass
    def onReferenceType(self, item, *args, **kw): pass
    def onArrayType(self, item, *args, **kw): pass

    # context elements
    def onContext(self, item, *args, **kw): pass
    def onNamespace(self, item, *args, **kw): pass
    def onUnion(self, item, *args, **kw): pass
    def onStruct(self, item, *args, **kw): pass
    def onClass(self, item, *args, **kw): pass

    # context members
    def onVariable(self, item, *args, **kw): pass
    def onField(self, item, *args, **kw): pass

    # sub elements of Callables
    def onArgument(self, item, *args, **kw): pass
    def onEllipsis(self, item, *args, **kw): pass

    # callables
    def onCallable(self, item, *args, **kw): pass
    def onFunction(self, item, *args, **kw): pass
    def onFunctionType(self, item, *args, **kw): pass
    def onMethod(self, item, *args, **kw): pass
    def onConstructor(self, item, *args, **kw): pass
    def onDestructor(self, item, *args, **kw): pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ModelAtom(object):
    def isCallable(self): return False
    def isArgument(self): return False
    def isType(self): return False
    def isPointerType(self): return False
    def isReferenceType(self): return False
    def isArrayType(self): return False
    def isTypedef(self): return False
    def isVariable(self): return False
    def isContext(self): return False
    def isCvQualifiedType(self): return False
    def isCompositeType(self): return False
    def isField(self): return False
    def isPreprocessor(self): return False
    def isFile(self): return False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def visit(self, visitor, *args, **kw):
        self._visitSpecial(visitor, *args, **kw)
        return self._visit(visitor, *args, **kw)
    def _visit(self, visitor, *args, **kw):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def visitChildren(self, visitor, *args, **kw):
        for child in self.iterVisitChildren(visitor):
            child.visit(visitor, *args, **kw)
    def visitAll(self, visitor, *args, **kw):
        self.visit(visitor, *args, **kw)
        for child in self.iterVisitChildren(visitor):
            child.visitAll(visitor, *args, **kw)
    def iterVisitChildren(self, visitor):
        return iter([])

    def _visitSpecial(self, visitor, *args, **kw):
        if self.isType():
            visitor.onType(self, *args, **kw)
        if self.isContext():
            visitor.onContext(self, *args, **kw)
        elif self.isCallable():
            visitor.onCallable(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Types
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LocatedElement(ModelAtom):
    file = None # reference to a File instance
    line = 0

class CType(LocatedElement):
    def isType(self):
        return True

class FundamentalType(CType):
    name = ''
    align = 0
    size = 0

    def _visit(self, visitor, *args, **kw):
        return visitor.onFundamentalType(self, *args, **kw)

class CvQualifiedType(CType):
    type = None
    const = False
    volatile = False
    
    def isCvQualifiedType(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onCvQualifiedType(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Enumeration Type
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Enumeration(CType):
    name = ''
    align = 0
    size = 0
    artificial = False
    context = None

    _enumValues = None
    def getEnumValues(self):
        if self._enumValues is None:
            self.setEnumValues([])
        return self._enumValues
    def setEnumValues(self, enumValues):
        self._enumValues = enumValues
    enumValues = property(getEnumValues, setEnumValues)

    def _visit(self, visitor, *args, **kw):
        return visitor.onEnumeration(self, *args, **kw)

    def iterVisitChildren(self, visitor):
        return iter(self.enumValues)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EnumValue(ModelAtom):
    name = ''
    value = ''
    
    def isEnumValue(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onEnumValue(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Typedefs, pointers, and arrays
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Typedef(CType):
    name = ''
    type = None # index into typemap
    context = None # index into composite type

    def isTypedef(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onTypedef(self, *args, **kw)

class PointerType(CType):
    align = 0
    size = 0
    type = None # index into typemap

    def isPointerType(self): return True
    def _visit(self, visitor, *args, **kw):
        return visitor.onPointerType(self, *args, **kw)

class ReferenceType(CType):
    align = 0
    size = 0
    type = None # index into typemap

    def isReferenceType(self): return True
    def _visit(self, visitor, *args, **kw):
        return visitor.onReferenceType(self, *args, **kw)

class ArrayType(CType):
    type = None # index into typemap
    align = 0
    size = 0
    min = 0
    max = None

    def isArrayType(self): return True
    def _visit(self, visitor, *args, **kw):
        return visitor.onArrayType(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Contexts, Structures, Unions, and Fields
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Namespace(LocatedElement):
    name = ''
    mangled = ''
    members = None # list of composite members
    context = None

    def isContext(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onNamespace(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CompositeType(CType):
    name = ''
    mangled = ''
    size = 0
    align = 0

    context = None # index into composite type
    bases = None # list of base clases
    members = None # list of composite members


    _fields = None
    def getFields(self):
        if self._fields is None:
            self.setFields([])
        return self._fields
    def setFields(self, fields):
        self._fields = fields
    fields = property(getFields, setFields)

    def addField(self, field):
        self.fields.append(field)

    def isCompositeType(self):
        return True
    def isContext(self):
        return True

    def iterVisitChildren(self, visitor):
        return iter(self.fields)

class Union(CompositeType):
    def _visit(self, visitor, *args, **kw):
        return visitor.onUnion(self, *args, **kw)

class Struct(CompositeType):
    incomplete = False
    artificial = False

    def _visit(self, visitor, *args, **kw):
        return visitor.onStruct(self, *args, **kw)

class Class(Struct):
    def _visit(self, visitor, *args, **kw):
        return visitor.onClass(self, *args, **kw)


class Base(ModelAtom):
    type = None
    access = ''
    virtual = False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Variable
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Variable(LocatedElement):
    name = ""
    type = None # index into typemap
    context = None # index into composite type

    artificial = False
    extern = False

    value = ''

    def isVariable(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onVariable(self, *args, **kw)

class Field(LocatedElement):
    name = ""
    mangled = '' # mangled name
    access = ''

    bits = None
    offset = None

    type = None # index into typemap
    context = None # index into composite type

    def isField(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onField(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Callable Types & Argument
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Argument(LocatedElement):
    name = ''
    type = None # index into typemap

    def isArgument(self): 
        return True
    def isEllipsisArgument(self):
        return False

    def _visit(self, visitor, *args, **kw):
        return visitor.onArgument(self, *args, **kw)

class Ellipsis(ModelAtom):
    def isArgument(self): 
        return True
    def isEllipsisArgument(self): 
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onEllipsis(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Callable(LocatedElement):
    def isCallable(self): 
        return True

    _arguments = None
    def getArguments(self):
        if self._arguments is None:
            self.setArguments([])
        return self._arguments
    def setArguments(self, arguments):
        self._arguments = arguments
    arguments = property(getArguments, setArguments)

    def iterVisitChildren(self, visitor):
        return iter(self.arguments)

class FunctionType(Callable):
    returns = None # index into typemap

    def _visit(self, visitor, *args, **kw):
        return visitor.onFunctionType(self, *args, **kw)

class Function(Callable):
    name = ''
    mangled = ''
    endline = None

    returns = None # index into typemap
    context = None # index into typemap
    
    inline = False
    extern = False

    attributes = None # list of string attributes
    throw = None # list of references

    def _visit(self, visitor, *args, **kw):
        return visitor.onFunction(self, *args, **kw)

class Method(Function):
    access = ''
    virtual = False

    def _visit(self, visitor, *args, **kw):
        return visitor.onMethod(self, *args, **kw)

class Constructor(Method):
    explicit = False
    artificial = False

    def _visit(self, visitor, *args, **kw):
        return visitor.onConstructor(self, *args, **kw)

class Destructor(Method):
    def _visit(self, visitor, *args, **kw):
        return visitor.onDestructor(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ File references
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class File(ModelAtom):
    name = ''

    def isFile(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onFile(self, *args, **kw)


