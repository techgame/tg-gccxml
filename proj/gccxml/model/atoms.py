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

from collections import deque
from bisect import insort, bisect_left, bisect_right
from itertools import chain

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getTypeString(aTypeAtom, descriptive=False):
    if not aTypeAtom:
        return 'None'
    assert aTypeAtom.isType(), repr(aTypeAtom)
    return aTypeAtom.getTypeString(descriptive)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ModelAtom(object):
    def isAtom(self): return True
    def isLocated(self): return False
    def isRoot(self): return False
    def isArgument(self): return False
    def isType(self): return False
    def isBasicType(self): return False
    def isFundamentalType(self): return False
    def isPointerType(self): return False
    def isReferenceType(self): return False
    def isArrayType(self): return False
    def isEnumeration(self): return False
    def isEnumValue(self): return False
    def isTypedef(self): return False
    def isVariable(self): return False
    def isContext(self): return False
    def isContainer(self): return False
    def isCvQualifiedType(self): return False
    def isCompositeType(self): return False
    def isUnion(self): return False
    def isStruct(self): return False
    def isClass(self): return False
    def isBaseRef(self): return False
    def isField(self): return False
    def isCallable(self): return False
    def isFunctionType(self): return False
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

        if short: className = self.__class__.__name__
        else: className = '.'.join([self.__class__.__module__, self.__class__.__name__])

        return "<%s: %s>" % (className, repr_atom)

    def __repr_atom__(self):
        return ""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def iterAll(self):
        work = deque([self])
        seen = set(work)
        seen.add(None)

        while work:
            atom = work.popleft()
            yield atom

            children = [child for child in atom.iterVisitChildren() if child not in seen]
            seen.update(children)
            work.extend(children)

    def iterTree(self):
        return self, (child.iterTree() for child in self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def visit(self, visitor, *args, **kw):
        return visitor.onVisitAtom(self, self._visit, *args, **kw)
    def _visit(self, visitor, *args, **kw):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def visitChildren(self, visitor, *args, **kw):
        return visitor.onVisitChildrenOf(self, self.iterVisitChildren(), *args, **kw)
    def iterVisitChildren(self):
        return iter([])

    def visitDependencies(self, visitor, *args, **kw):
        return visitor.onVisitDependenciesOf(self, self.iterVisitDependencies(), *args, **kw)
    def iterVisitDependencies(self):
        return self.iterVisitChildren()

    def treeDependencies(self):
        return ((d, d.treeDependencies()) for d in self.iterVisitDependencies())

    def allDependencies(self):
        seen = set([None])
        deps = list(self.iterVisitDependencies())
        while deps:
            d = deps.pop()
            if d not in seen:
                seen.add(d)
                deps.extend(d.iterVisitDependencies())
                yield d

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _updateAttrs(self, attrs):
        for n,v in attrs.iteritems():
            if v != getattr(self, n):
                setattr(self, n, v)

    def addAtom(self, atom): 
        raise Exception("Unexpected atom %r added to %r" % (atom, self))

    def linkChild(self, atom): 
        pass
    def linkTo(self, toAtom): 
        pass
    def linkFrom(self, fromAtom): 
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Root and File
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Root(ModelAtom):
    def __init__(self):
        self.files = {}
        self.ppDefines = {}

    def __repr_atom__(self):
        return "%s files" % len(self.files)

    def __iter__(self):
        return self.iterAll()

    def isRoot(self): 
        return True
    def isContainer(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onRoot(self, *args, **kw)
    def iterVisitChildren(self):
        return self.files.itervalues()
    def iterVisitDependencies(self):
        return iter([])

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
        result = File(filename)
        result.root = self
        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addPPAtom(self, ppAtom):
        if ppAtom.isPPDefine() or ppAtom.isPPMacro():
            self.ppDefines[ppAtom.ident] = ppAtom

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class File(ModelAtom):
    name = ''
    root = None

    def __init__(self, name=''):
        ModelAtom.__init__(self)
        self.name = name
        self.lines = []

    def __repr_atom__(self):
        if self.lines:
            return '"%s" atoms:%s lines:%s' % (self.name, len(self.lines), self.lines[-1][0])
        else:
            return '"%s" atoms:%s lines:%s' % (self.name, 0, 0)

    def __iter__(self):
        return self.iterLineItems()

    def iterLineItems(self):
        return (l[-1] for l in self.lines)

    def isFile(self):
        return True
    def isContainer(self): 
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onFile(self, *args, **kw)
    def iterVisitChildren(self):
        return (x[-1] for x in self.lines)
    def iterVisitDependencies(self):
        return iter([])

    def addAtom(self, atom):
        atom.file = self
        insort(self.lines, (atom.line, atom))

    def getAtomsBetween(self, fromAtom, toAtom=None):
        return (l[-1] for l in self.getLinesBetween(fromAtom, toAtom))
    def getLinesBetween(self, fromAtom, toAtom=None):
        if fromAtom is not None:
            idx0 = bisect_right(self.lines, (fromAtom.line, fromAtom))
        else: idx0 = None

        if toAtom is not None:
            idx1 = bisect_left(self.lines, (toAtom.line, toAtom))
        else: idx1 = None

        return self.lines[idx0:idx1]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    patches = None
    def addPatch(self, patchAtom):
        self.addAtom(patchAtom)
        if self.patches is None:
            self.patches = {}
        subPatches = self.patches.setdefault(patchAtom.kind, {})
        subPatches.setdefault(patchAtom.key, []).append(patchAtom)
    
    def getPatchFor(self, kind, itemKey=NotImplemented, default=()):
        if self.patches:
            subPatches = self.patches[kind]

            if itemKey is NotImplemented:
                return subPatches
            else:
                return subPatches.get(itemKey, default)
        else:
            if itemKey is NotImplemented:
                return {}
            else:
                return default

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Namespace(ModelAtom):
    name = ''
    mangled = ''
    demangled = ''
    members = () # list of composite members
    context = None # a Context Atom

    def __repr_atom__(self):
        return '%s members:%s' % (self.name, len(self.members))

    def isContext(self):
        return True
    def isContainer(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onNamespace(self, *args, **kw)
    def iterVisitChildren(self):
        return iter(self.members)
    def iterVisitDependencies(self):
        return iter([])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Types
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LocatedElement(ModelAtom):
    file = None # reference to a File instance
    line = 0

    def isLocated(self):
        return self.file is not None

    def getLoc(self):
        if self.file is not None:
            return '"%s":%s' % (self.file.name, self.line)
        elif self.line:
            return '"":%s' % (self.line,)
        else:
            return ''
    loc = property(getLoc)

class CType(LocatedElement):
    def isType(self):
        return True
    def getTypeString(self, descriptive=False):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def getTypeChain(self):
        return [self.type] + self.type.getTypeChain()

    def getBasicType(self):
        return self._resolveBasicType()
    basicType = property(getBasicType)
    def _resolveBasicType(self):
        return self

    referers = ()
    def linkFrom(self, fromAtom): 
        if self.referers is ():
            self.referers = []
        self.referers.append(fromAtom)

    _refLinks = None
    def getRefLinks(self):
        if self._refLinks is not None:
            return self._refLinks

        files = {}
        self._refLinks = files

        for r in self.referers:
            if r.isLocated():
                fileLinks = files.setdefault(r.file, {})
                fileLinks[r.line] = r

        return files
    def getFirstRefLinkByFile(self, file):
        return min(self.getRefLinks()[file].iteritems())
    def getFirstRefLinks(self):
        return dict(
                (f, min(v.iteritems())) 
                for f,v in self.getRefLinks().iteritems())

class CDelgateType(CType):
    _basicType = None
    def getBasicType(self):
        if self._basicType is None:
            self._basicType = self._resolveBasicType()
        return self._basicType
    basicType = property(getBasicType)

class FundamentalType(CType):
    name = ''
    align = 0
    size = 0

    def __repr_atom__(self):
        return "%s size:%s align:%s" % (self.name, self.size, self.align)

    def isFundamentalType(self):
        return True
    def isBasicType(self):
        return True
    def isType(self):
        return True

    def isVoidType(self):
        return self.name == 'void'

    def getTypeString(self, descriptive=False):
        return self.name

    def getTypeChain(self):
        return []

    def _visit(self, visitor, *args, **kw):
        return visitor.onFundamentalType(self, *args, **kw)

class CvQualifiedType(CDelgateType):
    type = None # a Type Atom
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
    def iterVisitChildren(self):
        return iter([self.type])

    def _resolveBasicType(self):
        return self.type.getBasicType()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Enumeration Type
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Enumeration(CType):
    name = ''
    align = 0
    size = 0
    artificial = False
    context = None # a Context Atom

    def isEnumeration(self):
        return True

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
    def iterVisitChildren(self):
        return iter(self.enumValues)

    def addAtom(self, atom): 
        if atom.isEnumValue():
            atom.host = self
            self.enumValues.append(atom)
        else:
            CType.addAtom(atom)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EnumValue(ModelAtom):
    host = None # Enumeration instance
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

class Typedef(CDelgateType):
    name = ''
    _type = None # a Type Atom
    context = None # a Context Atom

    def __init__(self):
        CDelgateType.__init__(self)

    def __repr_atom__(self):
        return '%s %s' % (self.name, getTypeString(self.type, True))

    def getTypeString(self, descriptive=False):
        return self.name

    def isTypedef(self):
        return True

    def getType(self):
        return self._type
    def setType(self, aType):
        if self._type is not None:
            raise Exception("Typedef type already set")

        self._type = aType
        self._updateBacklinks(aType)
    type = property(getType, setType)

    def isPointerTypedef(self):
        return aType.isPointerType()
    def isFunctionPointerTypedef(self):
        return aType.isPointerType() and aType.type.isFunctionType()

    def _updateBacklinks(self, aType):
        if aType is not None:
            backrefs = getattr(aType, 'typedefs', set())
            backrefs.add(self)
            aType.typedefs = backrefs

    def _visit(self, visitor, *args, **kw):
        return visitor.onTypedef(self, *args, **kw)
    def iterVisitChildren(self):
        return iter([self.type])

    def _resolveBasicType(self):
        return self.type.getBasicType()


class PointerType(CType):
    align = 0
    size = 0
    type = None # a Type Atom

    def __repr_atom__(self):
        return getTypeString(self.type, True)

    def getTypeString(self, descriptive=False):
        return getTypeString(self.type, True) + '*'

    def isPointerType(self): 
        return True
    def isBasicPointerType(self): 
        return self.type.basicType.isBasicType()

    def _visit(self, visitor, *args, **kw):
        return visitor.onPointerType(self, *args, **kw)
    def iterVisitChildren(self):
        return iter([self.type])

class ReferenceType(CType):
    align = 0
    size = 0
    type = None # a Type Atom

    def __repr_atom__(self):
        return getTypeString(self.type, True)

    def getTypeString(self, descriptive=False):
        return getTypeString(self.type, True) + '&'

    def isReferenceType(self): return True
    def isFundamentalReferenceType(self): 
        return self.type.isFundamentalType()

    def _visit(self, visitor, *args, **kw):
        return visitor.onReferenceType(self, *args, **kw)
    def iterVisitChildren(self):
        return iter([self.type])

class ArrayType(CType):
    type = None # a Type Atom
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
    def iterVisitChildren(self):
        return iter([self.type])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Contexts, Structures, Unions, and Fields
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CompositeType(CType):
    name = ''
    mangled = ''
    demangled = ''
    size = 0
    align = 0
    artificial = False
    incomplete = False
    access = ''

    context = None # a Context Atom
    bases = () # list of base clases
    members = () # list of composite members

    def __repr_atom__(self):
        return '%s members:%s size:%s align:%s' % (self.name, len(self.members), self.size, self.align)

    def getTypeString(self, descriptive=False):
        return self.name

    def getTypeChain(self):
        return []

    def isCompositeType(self):
        return True
    def isContext(self):
        return True
    def isContainer(self):
        return True

    def isAnonymous(self):
        return not bool(self.name)

    def iterVisitChildren(self):
        return chain(self.bases, self.members)

    def hasFields(self):
        for e in self.iterFields():
            return True
        else: return False

    def iterFields(self):
        return (e for e in self.members if e.isField())

class Union(CompositeType):
    def isUnion(self): 
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onUnion(self, *args, **kw)

class Struct(CompositeType):
    baseRefs = () # list of base references

    def __init__(self):
        self.baseRefs = []

    def isStruct(self): 
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onStruct(self, *args, **kw)

    def addAtom(self, atom):
        if atom.isBaseRef():
            atom.host = self
            self.baseRefs.append(atom)
        else:
            CompositeType.addAtom(self, atom)

    def iterVisitChildren(self):
        return chain(self.baseRefs, self.members)

class Class(Struct):
    def isClass(self): 
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onClass(self, *args, **kw)

class Base(ModelAtom):
    host = None # a Struct/Class atom
    type = None # a Struct/Class atom
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
    
    def iterVisitChildren(self):
        return iter([self.type])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Variable
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Variable(LocatedElement):
    name = ""
    type = None # a Type Atom
    context = None # a Context Atom

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
    def iterVisitChildren(self):
        return iter([self.type])

class Field(LocatedElement):
    name = ""
    mangled = '' # mangled name
    demangled = ''
    access = ''
    attributes = () # list of string attributes

    bits = None
    offset = None

    type = None # a Type Atom
    context = None # a Context Atom

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
    def iterVisitChildren(self):
        return iter([self.type])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Callable Types & Argument
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Argument(LocatedElement):
    host = None # a Callable instance
    name = ''
    default = ''
    type = None # a Type Atom

    def __repr_atom__(self):
        r = [self.name, 'type:'+getTypeString(self.type, True)]
        return ' '.join(i for i in r if i)

    def isArgument(self): 
        return True
    def isEllipsisArgument(self):
        return False

    def _visit(self, visitor, *args, **kw):
        return visitor.onArgument(self, *args, **kw)
    def iterVisitChildren(self):
        return iter([self.type])

class Ellipsis(ModelAtom):
    host = None # a Callable instance

    def __repr_atom__(self):
        return '...'

    def isArgument(self): 
        return True
    def isEllipsisArgument(self): 
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onEllipsis(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Callable(LocatedElement):
    returns = None # a Type Atom

    def isCallable(self): 
        return True
    def isContainer(self):
        return True

    def getType(self):
        return self.returns
    type = property(getType)

    _arguments = None
    def getArguments(self):
        if self._arguments is None:
            self.setArguments([])
        return self._arguments
    def setArguments(self, arguments):
        self._arguments = arguments
    arguments = property(getArguments, setArguments)

    def iterVisitChildren(self):
        return chain([self.returns], self.arguments)

    def addAtom(self, atom):
        if atom.isArgument():
            atom.host = self
            self.arguments.append(atom)
        else:
            LocatedElement.addAtom(self, atom)

class FunctionType(Callable):
    def __repr_atom__(self):
        return 'returns: %s' % (repr(self.returns),)

    def isType(self):
        return True
    def isBasicType(self):
        return True

    def getBasicType(self):
        return self._resolveBasicType()
    basicType = property(getBasicType)
    def _resolveBasicType(self):
        return self

    def getTypeChain(self):
        return []

    def isFunctionType(self):
        return True
    def isFunction(self):
        return False

    def getTypeString(self, descriptive=False):
        if descriptive:
            return '<function type>'
        else:
            raise NotImplementedError("Simple type string not available for function types")

    def _visit(self, visitor, *args, **kw):
        return visitor.onFunctionType(self, *args, **kw)

class Function(Callable):
    name = ''
    mangled = ''
    demangled = ''
    endline = None

    returns = None # a Type Atom 
    context = None # a Context Atom
    
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

class Method(Function):
    access = ''
    virtual = False
    const = False
    static = False
    explicit = False
    artificial = False

    def isMethod(self): 
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onMethod(self, *args, **kw)

class OperatorMethod(Method):
    def _visit(self, visitor, *args, **kw):
        return visitor.onOperatorMethod(self, *args, **kw)

class Constructor(Method):

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

    def isOpening(self):
        return self.directive.startswith('if')
    def isAlternate(self):
        return self.directive.startswith('el')
    def isClosing(self):
        return self.directive.startswith('end')

    def iterVisitDependencies(self):
        if not self.isOpening():
            return iter([self.getFirst()])
        else: return iter([])
    def _visit(self, visitor, *args, **kw):
        return visitor.onPPConditional(self, *args, **kw)

    def getEnclosed(self):
        if self.next is None:
            return []
        elif self.file is not None:
            return self.file.getAtomsBetween(self, self.next)

    def getOpening(self):
        result = self
        while result.prev is not None:
            result = result.prev
        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def inOrder(self):
        p = reversed(list(self.iterPrev()))
        n = self.iterNext(True)
        return chain(p, n)
    def getFirst(self):
        r = self
        while r.prev is not None:
            r = r.prev
        return r
    def iterPrev(self, incSelf=False):
        if incSelf: yield self
        c = self.prev
        while c is not None:
            yield c
            c = c.prev
    def iterNext(self, incSelf=False):
        if incSelf: yield self
        c = self.next
        while c is not None:
            yield c
            c = c.next

class PPDefine(PreprocessorAtom):
    ident = ''
    body = ''

    def __repr_atom__(self):
        return '#define %s %s' % (self.ident, self.body)

    def getName(self):
        return self.ident
    name = property(getName)

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

    def getName(self):
        return self.ident
    name = property(getName)

    def isPPMacro(self):
        return True

    def _visit(self, visitor, *args, **kw):
        return visitor.onPPMacro(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Patch Items
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PatchAtom(LocatedElement):
    kind = None # Major index - usually string
    key = None  # Minor index - usually a reference to the item the patch is associated with

    def isPatch(self):
        return True
    def _visit(self, visitor, *args, **kw):
        return visitor.onPatch(self, *args, **kw)

class FunctionTypeNamesPatch(PatchAtom):
    kind = "FunctionType"
    typeName = "" # the name of the typedef to the pointer to the function type
    argNames = () # a list of names that are being patched into the function type

    @property
    def key(self):
        return self.typeName

    def getName(self):
        return self.typeName
    name = property(getName)

    def getArgNames(self):
        return self.argNames

