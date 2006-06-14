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

import bisect
import itertools

import xml.sax
import xml.sax.handler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getTypeString(aTypeAtom, descriptive=False):
    if not aTypeAtom:
        return None
    assert aTypeAtom.isType(), repr(aTypeAtom)
    return aTypeAtom.getTypeString(descriptive)

class ModelAtomVisitor(object):
    # Common visitor types
    useCommonCalls = False
    def onAtomCommon(self, item, *args, **kw): pass
    def onTypeCommon(self, item, *args, **kw): pass
    def onContextCommon(self, item, *args, **kw): pass
    def onCallableCommon(self, item, *args, **kw): pass

    # root reference
    def onRoot(self, item, *args, **kw): pass

    # file references
    def onFile(self, item, *args, **kw): pass

    # simple types
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
    def onNamespace(self, item, *args, **kw): pass
    def onUnion(self, item, *args, **kw): pass
    def onStruct(self, item, *args, **kw): pass
    def onClass(self, item, *args, **kw): pass
    def onBase(self, item, *args, **kw): pass

    # context members
    def onVariable(self, item, *args, **kw): pass
    def onField(self, item, *args, **kw): pass

    # sub elements of Callables
    def onArgument(self, item, *args, **kw): pass
    def onEllipsis(self, item, *args, **kw): pass

    # callables
    def onFunction(self, item, *args, **kw): pass
    def onFunctionType(self, item, *args, **kw): pass
    def onMethod(self, item, *args, **kw): pass
    def onConstructor(self, item, *args, **kw): pass
    def onDestructor(self, item, *args, **kw): pass

    # preprocessor
    def onPPInclude(self, item, *args, **kw): pass
    def onPPConditional(self, item, *args, **kw): pass
    def onPPDefine(self, item, *args, **kw): pass
    def onPPMacro(self, item, *args, **kw): pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ModelAtom(object):
    def isRoot(self): return False
    def isArgument(self): return False
    def isType(self): return False
    def isBasicType(self): return False
    def isPointerType(self): return False
    def isReferenceType(self): return False
    def isArrayType(self): return False
    def isTypedef(self): return False
    def isVariable(self): return False
    def isContext(self): return False
    def isCvQualifiedType(self): return False
    def isCompositeType(self): return False
    def isUnion(self): return False
    def isStruct(self): return False
    def isClass(self): return False
    def isBaseRef(self): return False
    def isField(self): return False
    def isCallable(self): return False
    def isFunction(self): return False
    def isMethod(self): return False
    def isConstructor(self): return False
    def isDestructor(self): return False
    def isPreprocessor(self): return False
    def isPPInclude(self): return False
    def isPPConditional(self): return False
    def isPPDefine(self): return False
    def isPPMacro(self): return False
    def isFile(self): return False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self, short=False):
        repr_atom = self.__repr_atom__()
        if not repr_atom:
            repr_atom = 'id:0x%x' % id(self)
        if short:
            return "<%s: %s>" % (self.__class__.__name__, repr_atom)
        else:
            return "<%s.%s: %s>" % (self.__class__.__module__, self.__class__.__name__, repr_atom)
    def __repr_atom__(self):
        return ""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __iter__(self):
        for child in self.iterVisitChildren(None):
            yield child
    def iterAll(self):
        yield self
        for child in self:
            for each in child.iterAll():
                yield each
    def iterTree(self):
        return self, (child.iterTree() for child in self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def visit(self, visitor, *args, **kw):
        if visitor.useCommonCalls:
            self._visitCommon(visitor, *args, **kw)
        return self._visit(visitor, *args, **kw)
    def _visit(self, visitor, *args, **kw):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def visitChildren(self, visitor, *args, **kw):
        for child in self.iterVisitChildren(visitor):
            if child is not None:
                child.visit(visitor, *args, **kw)
    def visitAll(self, visitor, *args, **kw):
        self.visit(visitor, *args, **kw)
        for child in self.iterVisitChildren(visitor):
            if child is not None:
                child.visitAll(visitor, *args, **kw)
    def iterVisitChildren(self, visitor):
        return iter([])

    def _visitCommon(self, visitor, *args, **kw):
        visitor.onAtomCommon(self, *args, **kw)
        if self.isType():
            visitor.onTypeCommon(self, *args, **kw)
        if self.isContext():
            visitor.onContextCommon(self, *args, **kw)
        elif self.isCallable():
            visitor.onCallableCommon(self, *args, **kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _updateAttrs(self, attrs):
        for n,v in attrs.iteritems():
            if v != getattr(self, n):
                setattr(self, n, v)

    def addAtom(self, atom): 
        raise Exception("Unexpected atom %r added to %r" % (atom, self))
    def linkAtom(self, atom): 
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Root and File
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Root(ModelAtom):
    def __init__(self):
        self.files = {}

    def __repr_atom__(self):
        return "%s files" % len(self.files)

    def isRoot(self): 
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onRoot(self, *args, **kw)

    def iterVisitChildren(self, visitor):
        return self.files.itervalues()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getFile(self, filename):
        return self.files.get(filename, None)
    def addFile(self, filename):
        aFile = self.getFile(filename)
        if aFile is None:
            aFile = self.createFileFor(filename)
            self.files[filename] = aFile
        return aFile

    def createFileFor(self, filename):
        return File(filename)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class File(ModelAtom):
    name = ''

    def __init__(self, name=''):
        ModelAtom.__init__(self)
        self.name = name
        self.lines = []

    def __repr_atom__(self):
        if self.lines:
            return '"%s" atoms:%s lines:%s' % (self.name, len(self.lines), self.lines[-1][0])
        else:
            return '"%s" atoms:%s lines:%s' % (self.name, 0, 0)

    def isFile(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onFile(self, *args, **kw)
    
    def iterVisitChildren(self, visitor):
        return (x[-1] for x in self.lines)

    def addAtom(self, atom):
        bisect.insort(self.lines, (atom.line, atom))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Types
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LocatedElement(ModelAtom):
    file = None # reference to a File instance
    line = 0

class CType(LocatedElement):
    def isType(self):
        return True
    def getTypeString(self, descriptive=False):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def getTypeChain(self):
        return [self.type] + self.type.getTypeChain()


class FundamentalType(CType):
    name = ''
    align = 0
    size = 0

    def __repr_atom__(self):
        return "%s size:%s align:%s" % (self.name, self.size, self.align)

    def isType(self):
        return True
    def isBasicType(self):
        return True

    def getTypeString(self, descriptive=False):
        return self.name

    def getTypeChain(self):
        return []

    def _visit(self, visitor, *args, **kw):
        return visitor.onFundamentalType(self, *args, **kw)

class CvQualifiedType(CType):
    type = None
    const = False
    volatile = False
    
    def __repr_atom__(self):
        return self.getTypeString(True)

    def getTypeString(self, descriptive=False):
        r = []
        if self.const: r.append('const')
        if self.volatile: r.append('volatile')
        r.append(getTypeString(self.type, True))
        return ' '.join(r)

    def isCvQualifiedType(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onCvQualifiedType(self, *args, **kw)
    def iterVisitChildren(self, visitor):
        return iter([self.type])

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

    def __repr_atom__(self):
        return self.getTypeString(True)

    def getTypeString(self, descriptive=False):
        return self.name

    def _visit(self, visitor, *args, **kw):
        return visitor.onEnumeration(self, *args, **kw)

    def iterVisitChildren(self, visitor):
        return iter(self.enumValues)

    def addAtom(self, atom): 
        if atom.isEnumValue():
            self.enumValues.append(atom)
        else:
            CType.addAtom(atom)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EnumValue(ModelAtom):
    name = ''
    value = ''
    
    def isEnumValue(self):
        return True

    def __repr_atom__(self):
        return '%s=%s' % (self.name, self.value)

    def _visit(self, visitor, *args, **kw):
        return visitor.onEnumValue(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Typedefs, pointers, and arrays
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Typedef(CType):
    name = ''
    type = None # index into typemap
    context = None # index into composite type

    def __repr_atom__(self):
        return '%s %s' % (self.name, getTypeString(self.type, True))

    def __repr_atom__(self):
        return self.getTypeString(True)

    def getTypeString(self, descriptive=False):
        return self.name

    def isTypedef(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onTypedef(self, *args, **kw)
    def iterVisitChildren(self, visitor):
        return iter([self.type])

class PointerType(CType):
    align = 0
    size = 0
    type = None # index into typemap

    def __repr_atom__(self):
        return getTypeString(self.type, True)

    def getTypeString(self, descriptive=False):
        return getTypeString(self.type, True) + '*'

    def isPointerType(self): return True
    def _visit(self, visitor, *args, **kw):
        return visitor.onPointerType(self, *args, **kw)
    def iterVisitChildren(self, visitor):
        return iter([self.type])

class ReferenceType(CType):
    align = 0
    size = 0
    type = None # index into typemap

    def __repr_atom__(self):
        return getTypeString(self.type, True)

    def getTypeString(self, descriptive=False):
        return getTypeString(self.type, True) + '&'

    def isReferenceType(self): return True
    def _visit(self, visitor, *args, **kw):
        return visitor.onReferenceType(self, *args, **kw)
    def iterVisitChildren(self, visitor):
        return iter([self.type])

class ArrayType(CType):
    type = None # index into typemap
    align = 0
    size = 0
    min = 0
    max = None

    def __repr_atom__(self):
        return self.getTypeString(True)

    def getTypeString(self, descriptive=False):
        return getTypeString(self.type, True)+'[%s]' % (self.max,)

    def isArrayType(self): return True
    def _visit(self, visitor, *args, **kw):
        return visitor.onArrayType(self, *args, **kw)
    def iterVisitChildren(self, visitor):
        return iter([self.type])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Contexts, Structures, Unions, and Fields
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Namespace(LocatedElement):
    name = ''
    mangled = ''
    demangled = ''
    members = () # list of composite members
    context = None

    def __repr_atom__(self):
        return '%s members:%s' % (self.name, len(self.members))

    def isContext(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onNamespace(self, *args, **kw)
    def iterVisitChildren(self, visitor):
        return iter(self.members)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CompositeType(CType):
    name = ''
    mangled = ''
    demangled = ''
    size = 0
    align = 0

    context = None # index into composite type
    bases = () # list of base clases
    members = () # list of composite members

    def __repr_atom__(self):
        return '%s members:%s size:%s align:%s' % (self.name, len(self.members), self.size, self.align)

    def getTypeString(self, descriptive=False):
        return self.name

    def isCompositeType(self):
        return True
    def isContext(self):
        return True

    def iterVisitChildren(self, visitor):
        return itertools.chain(self.bases, self.members)

class Union(CompositeType):
    def isUnion(self): 
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onUnion(self, *args, **kw)

class Struct(CompositeType):
    incomplete = False
    artificial = False
    baseRefs = () # list of base references

    def __init__(self):
        self.baseRefs = []

    def isStruct(self): 
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onStruct(self, *args, **kw)

    def addAtom(self, atom):
        if atom.isBaseRef():
            self.baseRefs.append(atom)
        else:
            CompositeType.addAtom(self, atom)

    def iterVisitChildren(self, visitor):
        return itertools.chain(self.baseRefs, self.members)

class Class(Struct):
    def isClass(self): 
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onClass(self, *args, **kw)


class Base(ModelAtom):
    type = None
    access = ''
    virtual = False
    offset = 0

    def __repr_atom__(self):
        r = [getTypeString(self.type, True)]
        if self.virtual: r.append('virtual')
        if self.access: r.append('access:%s' % (self.access,))
        if self.offset: r.append('offset:%s' % (self.offset,))
        return ' '.join(i for i in r if i)

    def isBaseRef(self): 
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onBase(self, *args, **kw)

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

    def __repr_atom__(self):
        r = [self.name, 'type:'+getTypeString(self.type, True)]
        if self.extern: r.append('extern')
        return ' '.join(r)

    def isVariable(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onVariable(self, *args, **kw)
    def iterVisitChildren(self, visitor):
        return iter([self.type])

class Field(LocatedElement):
    name = ""
    mangled = '' # mangled name
    demangled = ''
    access = ''

    bits = None
    offset = None

    type = None # index into typemap
    context = None # index into composite type

    def __repr_atom__(self):
        r = [self.name, 'type:'+getTypeString(self.type, True)]
        if self.access: r.append('access:%s' % (self.access,))
        if self.bits: r.append('bits:%s' % (self.bits,))
        if self.offset: r.append('offset:%s' % (self.offset,))
        return ' '.join(r)

    def isField(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onField(self, *args, **kw)
    def iterVisitChildren(self, visitor):
        return iter([self.type])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Callable Types & Argument
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Argument(LocatedElement):
    name = ''
    type = None # index into typemap

    def __repr_atom__(self):
        r = [self.name, 'type:'+getTypeString(self.type, True)]
        return ' '.join(i for i in r if i)
    def isArgument(self): 
        return True
    def isEllipsisArgument(self):
        return False

    def _visit(self, visitor, *args, **kw):
        return visitor.onArgument(self, *args, **kw)
    def iterVisitChildren(self, visitor):
        return iter([self.type])

class Ellipsis(ModelAtom):
    def isArgument(self): 
        return True
    def isEllipsisArgument(self): 
        return True

    def __repr_atom__(self):
        return '...'

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

    def addAtom(self, atom):
        if atom.isArgument():
            self.arguments.append(atom)
        else:
            LocatedElement.addAtom(self, atom)

class FunctionType(Callable):
    returns = None # index into typemap

    def __repr_atom__(self):
        return 'returns:' + repr(self.returns)

    def isType(self):
        return True
    def isBasicType(self):
        return True

    def getTypeChain(self):
        return []

    def isFunction(self):
        return False

    def getTypeString(self, descriptive=False):
        if descriptive:
            return '<function type>'
        else:
            raise NotImplementedError("Simple type string not available for function types")

    def _visit(self, visitor, *args, **kw):
        return visitor.onFunctionType(self, *args, **kw)
    def iterVisitChildren(self, visitor):
        return iter([self.returns])

class Function(Callable):
    name = ''
    mangled = ''
    demangled = ''
    endline = None

    returns = None # index into typemap
    context = None # index into typemap
    
    inline = False
    extern = False

    attributes = () # list of string attributes
    throw = () # list of references

    def __repr_atom__(self):
        r = [self.name]
        if self.inline: r.append('inline')
        if self.extern: r.append('extern')
        if self.attributes: r.append('attrs:(' + ' '.join(self.attributes)+')')
        return ' '.join(r)

    def isFunction(self): 
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onFunction(self, *args, **kw)
    def iterVisitChildren(self, visitor):
        return itertools.chain([self.returns], self.arguments)

class Method(Function):
    access = ''
    virtual = False

    def isMethod(self): 
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onMethod(self, *args, **kw)

class Constructor(Method):
    explicit = False
    artificial = False

    def isConstructor(self): 
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onConstructor(self, *args, **kw)

class Destructor(Method):
    def isDestructor(self): 
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onDestructor(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Preprocessor Atoms
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PreprocessorAtom(LocatedElement):
    def isPreprocessorAtom(self):
        return True

class PPInclude(PreprocessorAtom):
    filename = ''
    includedFile = None
    isSystemInclude = False

    def __repr_atom__(self):
        if self.isSystemInclude:
            return '#include <%s>' % (self.filename,)
        else:
            return '#include "%s"' % (self.filename,)

    def isPPInclude(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onPPInclude(self, *args, **kw)

class PPConditional(PreprocessorAtom):
    directive = ''
    body = ''
    next = None
    prev = None

    def __repr_atom__(self):
        return '#%s %s' % (self.directive, self.body)
    def isPPConditional(self):
        return True

    def isConditionalOpening(self):
        return self.directive.startswith('if')
    def isConditionalContinuation(self):
        return self.directive.startswith('el')
    def isConditionalEnding(self):
        return self.directive.startswith('end')

    def _visit(self, visitor, *args, **kw):
        return visitor.onPPConditional(self, *args, **kw)

class PPDefine(PreprocessorAtom):
    ident = ''
    body = ''

    def __repr_atom__(self):
        return '#define %s %s' % (self.ident, self.body)

    def isPPDefine(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onPPDefine(self, *args, **kw)

class PPMacro(PreprocessorAtom):
    ident = ''
    args = () # list of idents
    body = ''

    def __repr_atom__(self):
        return '#define %s(%s) %s' % (self.ident, ', '.join(self.args), self.body)

    def isPPMacro(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onPPMacro(self, *args, **kw)

