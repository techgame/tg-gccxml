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
#~ Attr Value Map Functions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Linkable(object):
    @staticmethod
    def isLinkable(item):
        return isinstance(item, Linkable)

    def link(self, idMap):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

class LinkReference(Linkable):
    def __init__(self, v):
        self.ref = v

    def link(self, idMap):
        if self.ref:
            item = idMap[self.ref]
        else: item = None
        return item

class LinkReferenceList(Linkable):
    def __init__(self, refList):
        self.refList = list(refList)

    def link(self, idMap):
        return [m for m in (ref.link(idMap) for ref in self.refList) if m]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def passThrough(v):
    return v

def intOr0(v):
    return int(v or 0)
def intOrNone(v):
    if v: return int(v)
    else: return None
def boolOr0(v):
    return bool(int(v or 0))

def ignore(v):
    return None
def acccessStr(v):
    return v
def funcAttrList(v): 
    return v.split(' ')

def definition(v):
    return v
def reference(v):
    return LinkReference(v)

def referenceList(v):
    return LinkReferenceList(reference(i) for i in v.split(' '))

def throwList(v): 
    return referenceList(v)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ XML Element base class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLElement(object):
    topLevel = True
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

    def iterChildren(self):
        return iter(())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ GCC Model creation
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createModel(self, emitter, idMap):
        itemKind = self.itemKind
        if not itemKind:
            return None

        model = emitter.emit('create', itemKind, self.topLevel, dict(self._staticAttrs()))
        self.model = model
        self.createModelChildren(emitter, idMap, model)
        return model

    def createModelChildren(self, emitter, idMap, model):
        for e in self.iterChildren():
            sub = e.createModel(emitter, idMap)
            if sub is not None:
                emitter.emit('add-child', model, sub)

    def _staticAttrs(self):
        for n,v in self.attrs.iteritems():
            if not Linkable.isLinkable(v):
                yield n, v

    def linkModel(self, emitter, idMap):
        emitter.emit('linked', self.itemKind, self.topLevel, self.model, dict(self._linkAttrs(idMap)))
        self.linkModelChildren(emitter, idMap, self.model)

    def linkModelChildren(self, emitter, idMap, model):
        for e in self.iterChildren():
            sub = e.linkModel(emitter, idMap)
            if sub is not None:
                emitter.emit('link-child', model, sub)

    def _linkAttrs(self, idMap):
        attrs = self.attrs
        for n,v in attrs.iteritems():
            if Linkable.isLinkable(v):
                v = v.link(idMap)
                attrs[n] = v
                yield n, v

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
    itemKind = None

    attrValueMap = XMLElement.attrValueMap.copy()
    attrValueMap.update(
        id=definition,
        )

    def createModel(self, emitter, idMap):
        id = self.attrs.pop('id', None)
        model = XMLElement.createModel(self, emitter, idMap)
        if id is not None:
            idMap[id] = model
        return model

class LocatedElement(IdentifiedElement):
    attrValueMap = IdentifiedElement.attrValueMap.copy()
    attrValueMap.update(
        file=reference,
        line=intOr0,
        #location=locationOrNone,  # ignore this in favor of file and line references
        )
    attrNameMap = IdentifiedElement.attrNameMap.copy()
    attrNameMap.update(
        location=None, # ignore location -- prefer file and line references
        )

class SizedType(LocatedElement):
    attrValueMap = LocatedElement.attrValueMap.copy()
    attrValueMap.update(
        align=intOr0,
        size=intOr0,
        )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FundamentalType(SizedType):
    itemKind = 'FundamentalType'

    attrValueMap = SizedType.attrValueMap.copy()
    attrValueMap.update(
        name=passThrough,
        )

class CvQualifiedType(LocatedElement):
    itemKind = 'CvQualifiedType'

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
    itemKind = 'Enumeration'

    attrValueMap = SizedType.attrValueMap.copy()
    attrValueMap.update(
        name=passThrough,
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
    
    def iterChildren(self):
        return iter(self.enumValues)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EnumValue(XMLElement):
    topLevel = False
    itemKind = 'EnumValue'

    attrValueMap = XMLElement.attrValueMap.copy()
    attrValueMap.update(
        name=passThrough,
        init=intOr0,
        )
    attrNameMap = XMLElement.attrNameMap.copy()
    attrNameMap.update(init='value')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Typedefs, pointers, and arrays
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Typedef(LocatedElement):
    itemKind = 'Typedef'

    attrValueMap = LocatedElement.attrValueMap.copy()
    attrValueMap.update(
        name=passThrough,
        type=reference,
        context=reference,
        )

class PointerType(SizedType):
    itemKind = 'PointerType'

    attrValueMap = SizedType.attrValueMap.copy()
    attrValueMap.update(
        type=reference,
        )

class ReferenceType(SizedType):
    itemKind = 'ReferenceType'

    attrValueMap = SizedType.attrValueMap.copy()
    attrValueMap.update(
        type=reference,
        )

class ArrayType(SizedType):
    itemKind = 'ArrayType'

    attrValueMap = SizedType.attrValueMap.copy()
    attrValueMap.update(
        type=reference,
        min=intOr0,
        max=intOrNone,
        )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Contexts, Structures, Unions, and Fields
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Namespace(IdentifiedElement):
    itemKind = 'Namespace'

    attrValueMap = IdentifiedElement.attrValueMap.copy()
    attrValueMap.update(
        name=passThrough,
        mangled=passThrough,
        context=reference,
        members=referenceList,
        )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CompositeType(SizedType):
    itemKind = None

    attrValueMap = SizedType.attrValueMap.copy()
    attrValueMap.update(
        name=passThrough,
        mangled=passThrough,
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

    def iterChildren(self):
        return iter(self.fields)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Union(CompositeType):
    itemKind = 'Union'

class Struct(CompositeType):
    itemKind = 'Struct'

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

    def iterChildren(self):
        return iter(self.baseReferences)
    
class Class(Struct):
    itemKind = 'Class'

    attrValueMap = Struct.attrValueMap.copy()
    attrValueMap.update()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Base(XMLElement):
    topLevel = False
    itemKind = 'Base'

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
    itemKind = 'Variable'

    attrValueMap = LocatedElement.attrValueMap.copy()
    attrValueMap.update(
        name=passThrough,
        type=reference,
        context=reference,
        artificial=boolOr0,
        extern=boolOr0,
        init=passThrough,
        )
    attrNameMap = LocatedElement.attrNameMap.copy()
    attrNameMap.update(init='value')

class Field(LocatedElement):
    topLevel = False
    itemKind = 'Field'

    attrValueMap = LocatedElement.attrValueMap.copy()
    attrValueMap.update(
        name=passThrough,
        mangled=passThrough,
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
    topLevel = False
    itemKind = 'Argument'

    attrValueMap = LocatedElement.attrValueMap.copy()
    attrValueMap.update(
        name=passThrough,
        type=reference,
        )

class Ellipsis(XMLElement):
    topLevel = False
    itemKind = 'Ellipsis'

    attrValueMap = XMLElement.attrValueMap.copy()
    attrValueMap.update()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Callable(LocatedElement):
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

    def iterChildren(self):
        return iter(self.arguments)

class FunctionType(Callable):
    itemKind = 'FunctionType'

    attrValueMap = Callable.attrValueMap.copy()
    attrValueMap.update(
        returns=reference,
        )

class Function(Callable):
    itemKind = 'Function'

    attrValueMap = Callable.attrValueMap.copy()
    attrValueMap.update(
        name=passThrough,
        mangled=passThrough,
        endline=intOrNone,

        returns=reference,
        context=reference,

        extern=boolOr0,
        inline=boolOr0,

        attributes=funcAttrList,
        throw=throwList,
        )

class Method(Function):
    itemKind = 'Method'

    attrValueMap = Function.attrValueMap.copy()
    attrValueMap.update(
        access=acccessStr,
        virtual=boolOr0,
        )

class Constructor(Method):
    itemKind = 'Constructor'

    attrValueMap = Function.attrValueMap.copy()
    attrValueMap.update(
        artificial=boolOr0,
        explicit=boolOr0,
        )

class Destructor(Method):
    itemKind = 'Destructor'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ File references
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class File(IdentifiedElement):
    itemKind = 'File'

    attrValueMap = IdentifiedElement.attrValueMap.copy()
    attrValueMap.update(
        name=passThrough,
        )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ GCC XML Elements
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GCC_XML(XMLElement):
    # use this name because it matches the xml scheme

    elements = None # list of elements
    idMap = None # map of ids to elements

    def addElement(self, elem):
        self.elements.append(elem)

    def walk(self, emitters):
        idMap = {}
        for elem in self.elements:
            elem.createModel(emitters, idMap)

        for elem in self.elements:
            elem.linkModel(emitters, idMap)

        #from pprint import pprint as pp
        #pp(idMap)

    def start(self):
        self.elements = []

    def end(self):
        pass

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
        self.root.start()
    def endRoot(self):
        self.root.end()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _log(self, msg):
        print msg

