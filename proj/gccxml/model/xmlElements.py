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

import gccElements

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def ignore(v):
    return None

class definition(str): pass
class reference(str): pass

class fileReference(str): pass

def acccessStr(v):
    return v

def intOr0(v):
    return int(v or 0)
def intOrNone(v):
    if v: return int(v)
    else: return None
def boolOr0(v):
    return bool(int(v or 0))

def referenceList(v):
    return [reference(i) for i in v.split(' ')]

def throwList(v): 
    return referenceList(v)

def funcAttrList(v): 
    return v.split(' ')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLElement(object):
    ElementFactory = None
    attrValueMap = dict()
    attrNameMap = dict(cvs_revision=None,)

    def __init__(self, attrs):
        self._setXMLAttrs(attrs)

    @classmethod
    def getXMLElementName(klass):
        return klass.__name__

    def _setXMLAttrs(self, attrs):
        self.attrs = self._transformAttrs(attrs)

    def _transformAttrs(self, attrs):
        attrNameMap = self.attrNameMap
        attrValueMap = self.attrValueMap

        print 'in:', self.getXMLElementName()
        newAttrs = {}
        for xn,xv in attrs.items():
            # see if we are converting this name
            n = attrNameMap.get(xn, xn)
            if not n: continue

            # get the value conversion function from the xml attribute name
            vFn = attrValueMap[xn]

            # convert the value 
            v = vFn(xv)

            # set it into the new attr map under the new name
            newAttrs[n] = v
            print '   ', n, '=', v

        return newAttrs

    def startElement(self, name, attrs):
        xmlElemFactory = self.getChildTypes().get(name, None)
        if xmlElemFactory is not None:
            elem = xmlElemFactory(attrs)
        else:
            elem = None
        return elem
    def endElement(self, elem):
        if elem is not None:
            self.addElement(elem)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addElement(self, elem):
        raise Exception("Unexpected child element: %s for: %s" % (elem, self))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Child Elements Types
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _elemTypeMap = {}
    @classmethod
    def getChildTypes(klass):
        return klass._elemTypeMap
    @classmethod
    def setChildTypes(klass, elementTypes):
        klass._elemTypeMap = dict((et.getXMLElementName(), et) for et in elementTypes)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Types
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IdentifiedElement(XMLElement):
    ElementFactory = None

    attrValueMap = XMLElement.attrValueMap.copy()
    attrValueMap.update(
        id=definition,
        )

class LocatedElement(IdentifiedElement):
    ElementFactory = None

    attrValueMap = IdentifiedElement.attrValueMap.copy()
    attrValueMap.update(
        file=ignore,
        line=ignore,
        #location=locationOrNone,  # ignore this in favor of file and line references
        )
    attrNameMap = IdentifiedElement.attrNameMap.copy()
    attrNameMap.update(
        location=None, # ignore location -- prefer file and line references
        )

class SizedType(LocatedElement):
    ElementFactory = None

    attrValueMap = LocatedElement.attrValueMap.copy()
    attrValueMap.update(
        align=intOr0,
        size=intOr0,
        )

class FundamentalType(SizedType):
    ElementFactory = gccElements.FundamentalType
    ElementFactory = None

    attrValueMap = SizedType.attrValueMap.copy()
    attrValueMap.update(
        name=str,
        )

class CvQualifiedType(LocatedElement):
    ElementFactory = gccElements.CvQualifiedType

    attrValueMap = LocatedElement.attrValueMap.copy()
    attrValueMap.update(
        type=reference,
        const=boolOr0,
        volatile=boolOr0,
        )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Enumeration Type
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Enumeration(SizedType):
    ElementFactory = gccElements.Enumeration

    attrValueMap = SizedType.attrValueMap.copy()
    attrValueMap.update(
        name=str,
        artificial=boolOr0,
        context=reference,
        )

    _enumValues = None
    def getEnumValues(self):
        if self._enumValues is None:
            self.setEnumValues([])
        return self._enumValues
    def setEnumValues(self, enumValues):
        self._enumValues = enumValues
    enumValues = property(getEnumValues, setEnumValues)

    def addElement(self, elem):
        if isinstance(elem, EnumValue):
            self.enumValues.append(elem)
        else:
            SizedType.addElement(self, enum)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EnumValue(XMLElement):
    ElementFactory = gccElements.EnumValue

    attrValueMap = XMLElement.attrValueMap.copy()
    attrValueMap.update(
        name=str,
        init=intOr0,
        )
    attrNameMap = XMLElement.attrNameMap.copy()
    attrNameMap.update(init='value')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Typedefs, pointers, and arrays
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Typedef(LocatedElement):
    ElementFactory = gccElements.Typedef

    attrValueMap = LocatedElement.attrValueMap.copy()
    attrValueMap.update(
        name=str,
        type=reference,
        context=reference,
        )

class PointerType(SizedType):
    ElementFactory = gccElements.PointerType

    attrValueMap = SizedType.attrValueMap.copy()
    attrValueMap.update(
        type=reference,
        )

class ReferenceType(SizedType):
    ElementFactory = gccElements.ReferenceType

    attrValueMap = SizedType.attrValueMap.copy()
    attrValueMap.update(
        type=reference,
        )

class ArrayType(SizedType):
    ElementFactory = gccElements.ArrayType

    attrValueMap = SizedType.attrValueMap.copy()
    attrValueMap.update(
        type=reference,
        min=intOr0,
        max=intOrNone,
        )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Contexts, Structures, Unions, and Fields
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Namespace(XMLElement):
    ElementFactory = gccElements.Namespace

    attrValueMap = XMLElement.attrValueMap.copy()
    attrValueMap.update(
        id=definition,
        name=str,
        mangled=str,
        context=reference,
        members=referenceList,
        )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CompositeType(SizedType):
    ElementFactory = None

    attrValueMap = SizedType.attrValueMap.copy()
    attrValueMap.update(
        name=str,
        mangled=str,
        size=intOr0,
        align=intOr0,

        context=reference,

        bases=referenceList,
        members=referenceList,
        )

    _fields = None
    def getFields(self):
        if self._fields is None:
            self.setFields([])
        return self._fields
    def setFields(self, fields):
        self._fields = fields
    fields = property(getFields, setFields)

    def addElement(self, elem):
        if isinstance(elem, Field):
            self.fields.append(elem)
        else:
            SizedType.addElement(self, enum)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Union(CompositeType):
    ElementFactory = gccElements.Union

class Struct(CompositeType):
    ElementFactory = gccElements.Struct

    attrValueMap = CompositeType.attrValueMap.copy()
    attrValueMap.update(
        incomplete=boolOr0,
        artificial=boolOr0,
        )

    _baseReferences = None
    def getBaseReferences(self):
        if self._baseReferences is None:
            self.setBaseReferences([])
        return self._baseReferences
    def setBaseReferences(self, baseReferences):
        self._baseReferences = baseReferences
    baseReferences = property(getBaseReferences, setBaseReferences)

    def addElement(self, elem):
        if isinstance(elem, Base):
            self.baseReferences.append(elem)
        else:
            CompositeType.addElement(self, enum)

class Class(Struct):
    ElementFactory = gccElements.Class

    attrValueMap = Struct.attrValueMap.copy()
    attrValueMap.update()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Base(XMLElement):
    ElementFactory = gccElements.Base

    attrValueMap = XMLElement.attrValueMap.copy()
    attrValueMap.update(
        type=reference,
        access=acccessStr,
        virtual=boolOr0,
        )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Variable
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Variable(LocatedElement):
    ElementFactory = gccElements.Variable

    attrValueMap = LocatedElement.attrValueMap.copy()
    attrValueMap.update(
        name=str,
        type=reference,
        context=reference,
        artificial=boolOr0,
        extern=boolOr0,
        init=str,
        )
    attrNameMap = LocatedElement.attrNameMap.copy()
    attrNameMap.update(init='value')

class Field(LocatedElement):
    ElementFactory = gccElements.Field

    attrValueMap = LocatedElement.attrValueMap.copy()
    attrValueMap.update(
        name=str,
        mangled=str,
        access=acccessStr,

        offset=intOrNone,
        bits=intOrNone,

        type=reference,
        context=reference,
        )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Callable Types & Argument
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Argument(LocatedElement):
    ElementFactory = gccElements.Argument

    attrValueMap = LocatedElement.attrValueMap.copy()
    attrValueMap.update(
        name=str,
        type=reference,
        )

class Ellipsis(XMLElement):
    ElementFactory = gccElements.Ellipsis

    attrValueMap = XMLElement.attrValueMap.copy()
    attrValueMap.update()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Callable(LocatedElement):
    ElementFactory = None

    attrValueMap = LocatedElement.attrValueMap.copy()
    attrValueMap.update()

    _arguments = None
    def getArguments(self):
        if self._arguments is None:
            self.setArguments([])
        return self._arguments
    def setArguments(self, arguments):
        self._arguments = arguments
    arguments = property(getArguments, setArguments)

    def addElement(self, elem):
        if isinstance(elem, (Argument, Ellipsis)):
            self.arguments.append(elem)
        else:
            LocatedElement.addElement(self, enum)

class FunctionType(Callable):
    ElementFactory = gccElements.FunctionType

    attrValueMap = Callable.attrValueMap.copy()
    attrValueMap.update(
        returns=reference,
        )

class Function(Callable):
    ElementFactory = gccElements.Function

    attrValueMap = Callable.attrValueMap.copy()
    attrValueMap.update(
        name=str,
        mangled=str,
        endline=intOrNone,

        returns=reference,
        context=reference,

        extern=boolOr0,
        inline=boolOr0,

        attributes=funcAttrList,
        throw=throwList,
        )

class Method(Function):
    ElementFactory = gccElements.Method

    attrValueMap = Function.attrValueMap.copy()
    attrValueMap.update(
        access=acccessStr,
        virtual=boolOr0,
        )

class Constructor(Method):
    ElementFactory = gccElements.Constructor

    attrValueMap = Function.attrValueMap.copy()
    attrValueMap.update(
        artificial=boolOr0,
        explicit=boolOr0,
        )

class Destructor(Method):
    ElementFactory = gccElements.Destructor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ File references
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class File(IdentifiedElement):
    ElementFactory = gccElements.File

    attrValueMap = IdentifiedElement.attrValueMap.copy()
    attrValueMap.update(
        name=str,
        )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ GCC XML Elements
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GCC_XML(XMLElement):
    ElementFactory = None

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

Struct.setChildTypes([Base]) # Class is a subtype of Struct

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

