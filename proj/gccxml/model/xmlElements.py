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

class Element(object):
    def __init__(self, attrs):
        self.setXMLAttrs(attrs)

    def __repr__(self):
        r = '<' + self.__class__.__name__
        name = getattr(self, 'name', '')
        if name:
            r+= ' "%s"' % name

        id = getattr(self, 'id', '')
        if id:
            r+= ' id:' + id

        if self.file:
            r+= ' loc:%s+%s' % (self.file, self.line)
        return r + '>'
    @classmethod
    def getXMLElementName(klass):
        return klass.__name__

    def setXMLAttrs(self, attrs):
        for n,v in attrs.items():
            setattr(self, n, v)

    def startElement(self, name, attrs):
        factory = self.getChildTypes().get(name, None)
        if factory is not None:
            elem = factory(attrs)
        else:
            elem = None
        return elem
    def endElement(self, elem):
        if elem is not None:
            self.addElement(elem)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    file = '' # index into file list

    # make line an integer so we can compare with it
    _line = None
    def getLine(self):
        return self._line
    def setLine(self, line):
        if line:
            self._line = int(line)
        else: self._line = None
    line = property(getLine, setLine)

    # location is a duplicate of file & line
    location = property(lambda s:None, lambda s, v:None)

    def addElement(self, elem):
        raise Exception("Unexpected child element: %s for: %s" % (elem, self))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def isCallable(self): 
        return False
    def isArgument(self): 
        return False
    def isType(self): 
        return False
    def isPointerType(self): 
        return False
    def isTypedef(self):
        return False
    def isVariable(self):
        return False
    def isContext(self):
        return False
    def isModifiedType(self):
        return False
    def isCompositeType(self):
        return False
    def isField(self):
        return False
    def isPreprocessor(self):
        return False
    def isFile(self):
        return False

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
        if self.isCallable():
            visitor.onCallable(self, *args, **kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Child Elements Types
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def getChildTypes(klass):
        return klass._elemTypeMap
    @classmethod
    def setChildTypes(klass, elementTypes):
        klass._elemTypeMap = dict((et.getXMLElementName(), et) for et in elementTypes)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ElementVisitor(object):
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
#~ File references
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class File(Element):
    name = ''

    def isFile(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onFile(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Types
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CType(Element):
    id = None # key in identmap

    def isType(self):
        return True

class AlignedType(CType):
    _align = None
    def getAlign(self):
        return self._align
    def setAlign(self, align):
        self._align = int(align)
    align = property(getAlign, setAlign)

class SizedType(AlignedType):
    _size = None
    def getSize(self):
        return self._size
    def setSize(self, size):
        self._size = int(size)
    size = property(getSize, setSize)

class FundamentalType(SizedType):
    name = ''

    def _visit(self, visitor, *args, **kw):
        return visitor.onFundamentalType(self, *args, **kw)

class CvQualifiedType(CType):
    type = None # index into typemap

    _const = False
    def getConst(self):
        return self._const
    def setConst(self, const):
        self._const = bool(int(const or 0))
    const = property(getConst, setConst)

    _volatile = False
    def getVolatile(self):
        return self._volatile
    def setVolatile(self, volatile):
        self._volatile =  bool(int(volatile or 0))
    volatile = property(getVolatile, setVolatile)
    
    def isModifiedType(self):
        return True
    def _visit(self, visitor, *args, **kw):
        return visitor.onCvQualifiedType(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Enumeration Type
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Enumeration(SizedType):
    name = ''
    context = None

    _enumValues = None
    def getEnumValues(self):
        if self._enumValues is None:
            self.setEnumValues([])
        return self._enumValues
    def setEnumValues(self, enumValues):
        self._enumValues = enumValues
    enumValues = property(getEnumValues, setEnumValues)

    def addElement(self, elem):
        if elem.isEnumValue():
            self.enumValues.append(elem)
        else:
            raise Exception("Unexpected child element: %s for: %s" % (elem, self))

    def _visit(self, visitor, *args, **kw):
        return visitor.onEnumeration(self, *args, **kw)

    def iterVisitChildren(self, visitor):
        return iter(self.enumValues)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EnumValue(Element):
    name = ''

    _init = 0
    def getInit(self):
        return self._init
    def setInit(self, init):
        self._init = int(init or 0)
    init = property(getInit, setInit)
    
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

class PointerType(SizedType):
    type = None # index into typemap

    def isPointerType(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onPointerType(self, *args, **kw)

class ReferenceType(PointerType):
    type = None # index into typemap

    def _visit(self, visitor, *args, **kw):
        return visitor.onReferenceType(self, *args, **kw)

class ArrayType(AlignedType):
    type = None # index into typemap

    _min = 0
    def getMin(self):
        return self._min
    def setMin(self, min):
        self._min = int(min or 0)
    min = property(getMin, setMin)

    _max = None
    def getMax(self):
        return self._max
    def setMax(self, max):
        if max:
            self._max = int(max)
        else:
            self._max = None
    max = property(getMax, setMax)

    def _visit(self, visitor, *args, **kw):
        return visitor.onArrayType(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Contexts, Structures, Unions, and Fields
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Namespace(Element):
    id = None # key in identmap
    name = ''
    members = ''

    def isContext(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onNamespace(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CompositeType(SizedType):
    name = ''
    mangled = ''
    bases = ''
    context = None # index into composite type

    memebers = ''

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
    def _visit(self, visitor, *args, **kw):
        return visitor.onStruct(self, *args, **kw)

class Class(Struct):
    def _visit(self, visitor, *args, **kw):
        return visitor.onClass(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Variable
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Variable(Element):
    id = None # key in identmap
    name = ""
    type = None # index into typemap
    context = None # index into composite type

    init = None # initial value -- useful it type is constant

    def isVariable(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onVariable(self, *args, **kw)

class Field(Element):
    id = None # key in identmap
    name = ""
    mangled = '' # mangled name
    type = None # index into typemap
    bits = None

    context = None # index into composite type
    access = ''

    _offset = None
    def getOffset(self):
        return self._offset
    def setOffset(self, offset):
        if offset:
            self._offset = int(offset)
        else: self._offset = None
    offset = property(getOffset, setOffset)

    def isField(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onField(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Callable Types & Argument
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Argument(Element):
    name = ''
    type = None # index into typemap

    def isArgument(self): 
        return True
    def isEllipsisArgument(self):
        return False

    def _visit(self, visitor, *args, **kw):
        return visitor.onArgument(self, *args, **kw)

class Ellipsis(Element):
    def isArgument(self): 
        return True
    def isEllipsisArgument(self): 
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onEllipsis(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Callable(CType):
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

    def addElement(self, elem):
        if elem.isArgument():
            self.arguments.append(elem)
        else:
            raise Exception("Unexpected child element: %s for: %s" % (elem, self))

    def iterVisitChildren(self, visitor):
        return iter(self.arguments)

class Function(Callable):
    name = ''
    mangled = ''

    context = None # index into composite type
    extern = None # extern method?

    returns = None # index into typemap
    
    _inline = False
    def getInline(self):
        return self._inline
    def setInline(self, inline):
        self._inline = bool(int(inline or 0))
    inline = property(getInline, setInline)

    def _visit(self, visitor, *args, **kw):
        return visitor.onFunction(self, *args, **kw)

class FunctionType(Callable):
    returns = None # index into typemap

    def _visit(self, visitor, *args, **kw):
        return visitor.onFunctionType(self, *args, **kw)

class Method(Function):
    throw = ''

    def _visit(self, visitor, *args, **kw):
        return visitor.onMethod(self, *args, **kw)

class Constructor(Method):
    _explicit = False
    def getExplicit(self):
        return self._explicit
    def setExplicit(self, explicit):
        self._explicit = bool(int(explicit or 0))
    explicit = property(getExplicit, setExplicit)

    def _visit(self, visitor, *args, **kw):
        return visitor.onConstructor(self, *args, **kw)

class Destructor(Method):
    def _visit(self, visitor, *args, **kw):
        return visitor.onDestructor(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ GCC XML Elements
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GCC_XML(Element):
    # use this name because it matches the xml scheme
    _elements = None
    def getElements(self):
        if self._elements is None:
            self.setElements([])
        return self._elements
    def setElements(self, elements):
        self._elements = elements
    elements = property(getElements, setElements)

    def addElement(self, elem):
        self.elements.append(elem)

    def _visit(self, visitor, *args, **kw):
        return visitor.onRoot(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Child definitions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GCC_XML.setChildTypes([
        Namespace, File,
        FundamentalType, CvQualifiedType, Enumeration, 
        PointerType, ReferenceType, ArrayType, 
        Typedef, Union, Struct, Class,
        FunctionType, Function, Method, Constructor, Destructor, 
        Variable, Field,
        ])

Enumeration.setChildTypes([EnumValue])
Callable.setChildTypes([Argument, Ellipsis])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ xml.sax.handler.ContentHandler
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GCCXMLHandler(xml.sax.handler.ContentHandler):
    RootFactory = GCC_XML
    root = None

    def parse(self, xmlFile):
        xml.sax.parse(xmlFile, self)
        return self.root

    def startDocument(self):
        self.root = None
        self.stack = [None]

    def endDocument(self):
        del self.stack
        self.endRoot()

    def startElement(self, name, attrs):
        parent = self.stack[-1]
        elem = self.startElementWithParent(parent, name, attrs)
        self.stack.append(elem)

    def endElement(self, name):
        elem = self.stack.pop()
        self.endElementWithParent(self.stack[-1], elem)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def startElementWithParent(self, parent, name, attrs):
        if parent is None:
            if self.root is None:
                self.createRoot(name, attrs)
                elem = self.root
            else:
                # root is already set, but a parent is unknown... so just ignore it
                elem = None
        else:
            elem = parent.startElement(name, attrs)
            if elem is None:
                self._log("Unknown child of: %r name: %r attrs: %r" % (parent, name, attrs))
        return elem

    def endElementWithParent(self, parent, elem):
        if parent is not None:
            elem = parent.endElement(elem)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createRoot(self, name, attrs):
        self.root = self.RootFactory(attrs)

        # pretend the root is already pushed -- this will
        # be done "for real" by the startElement method
        self.stack.append(self.root)
        try:
            self.startRoot()
        finally:
            if self.stack.pop() is not self.root:
                raise Exception("Stack mismatch: root is not where it is supposed to be")
    
    def startRoot(self):
        pass
    def endRoot(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _log(self, msg):
        print msg

