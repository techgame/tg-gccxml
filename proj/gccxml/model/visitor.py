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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ModelAtomVisitorInterface(object):
    def onVisitAtom(self, atom, atomVisitCB, *args, **kw):
        return atomVisitCB(self, *args, **kw)
    def onVisitChildrenOf(self, atom, iterChildren, *args, **kw): pass
    def onVisitDependenciesOf(self, atom, iterDependencies, *args, **kw): pass

class AtomVisitorInterface(ModelAtomVisitorInterface):
    # root reference
    def onRoot(self, atom, *args, **kw): pass

    # file references
    def onFile(self, atom, *args, **kw): pass

    # namespace 
    def onNamespace(self, atom, *args, **kw): pass

    # simple types
    def onFundamentalType(self, atom, *args, **kw): pass
    def onCvQualifiedType(self, atom, *args, **kw): pass
    def onEnumeration(self, atom, *args, **kw): pass
    def onEnumValue(self, atom, *args, **kw): pass

    # complex types and pointers
    def onTypedef(self, atom, *args, **kw): pass
    def onPointerType(self, atom, *args, **kw): pass
    def onReferenceType(self, atom, *args, **kw): pass
    def onArrayType(self, atom, *args, **kw): pass

    # context elements
    def onUnion(self, atom, *args, **kw): pass
    def onStruct(self, atom, *args, **kw): pass
    def onClass(self, atom, *args, **kw): pass
    def onBase(self, atom, *args, **kw): pass

    # context members
    def onVariable(self, atom, *args, **kw): pass
    def onField(self, atom, *args, **kw): pass

    # sub elements of Callables
    def onArgument(self, atom, *args, **kw): pass
    def onEllipsis(self, atom, *args, **kw): pass

    # callables
    def onFunction(self, atom, *args, **kw): pass
    def onFunctionType(self, atom, *args, **kw): pass
    def onMethod(self, atom, *args, **kw): pass
    def onOperatorMethod(self, atom, *args, **kw): pass
    def onConstructor(self, atom, *args, **kw): pass
    def onDestructor(self, atom, *args, **kw): pass

    # preprocessor
    def onPPInclude(self, atom, *args, **kw): pass
    def onPPConditional(self, atom, *args, **kw): pass
    def onPPDefine(self, atom, *args, **kw): pass
    def onPPMacro(self, atom, *args, **kw): pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BasicAtomVisitorMixin(object):
    # Common visitor types

    def visitAll(self, atomCollection, *args, **kw):
        self._visitAtoms = set()
        for atom in atomCollection:
            self._visit(atom, *args, **kw)
        del self._visitAtoms

    def visit(self, atom, *args, **kw):
        self._visitAtoms = set()
        result = self._visit(atom, *args, **kw)
        del self._visitAtoms
        return result

    def _visit(self, atom, *args, **kw):
        # this method prevents the DFS from tracing loops in the graph
        if atom in self._visitAtoms:
            return

        self._visitAtoms.add(atom)
        try:
            result = self._visitAtom(atom, *args, **kw)
        finally:
            self._visitAtoms.remove(atom)
        return result

    def _visitAtom(self, atom, *args, **kw):
        return atom.visit(self, *args, **kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def onVisitChildrenOf(self, atom, iterChildren, *args, **kw):
        for c in iterChildren:
            if c is not None:
                self._visit(c, *args, **kw)

    def onVisitDependenciesOf(self, atom, iterDependencies, *args, **kw):
        for e in iterDependencies:
            if e is not None:
                self._visit(e, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BasicAtomVisitor(BasicAtomVisitorMixin, AtomVisitorInterface):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DependencyAtomVisitorMixin(BasicAtomVisitorMixin):
    def _visitAtom(self, atom, *args, **kw):
        result = atom.visit(self, *args, **kw)
        atom.visitDependencies(self, *args, **kw)
        return result

class DependencyAtomVisitor(DependencyAtomVisitorMixin, AtomVisitorInterface):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AtomVisitorMixin(BasicAtomVisitorMixin):
    def _visitAtom(self, atom, *args, **kw):
        result = atom.visit(self, *args, **kw)
        atom.visitChildren(self, *args, **kw)
        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def onVisitAtom(self, atom, atomVisitCB, *args, **kw):
        self._visitAtomCommon(atom, *args, **kw)
        return atomVisitCB(self, *args, **kw)

    def _visitAtomCommon(self, atom, *args, **kw):
        self.onAtomCommon(atom, *args, **kw)
        if atom.isType():
            self.onTypeCommon(atom, *args, **kw)
        if atom.isContext():
            self.onContextCommon(atom, *args, **kw)
        elif atom.isCallable():
            self.onCallableCommon(atom, *args, **kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def onAtomCommon(self, atom, *args, **kw): pass
    def onTypeCommon(self, atom, *args, **kw): pass
    def onContextCommon(self, atom, *args, **kw): pass
    def onCallableCommon(self, atom, *args, **kw): pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AtomVisitor(AtomVisitorMixin, AtomVisitorInterface):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Atom Filters
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AtomFilterVisitor(AtomVisitor):
    selected = None

    def __init__(self):
        self.selected = set()

    def visitAll(self, atomCollection, *args, **kw):
        super(AtomFilterVisitor, self).visitAll(atomCollection, *args, **kw)
        return self.selected

    def visit(self, atom, *args, **kw):
        super(AtomFilterVisitor, self).visit(atom, *args, **kw)
        return self.selected

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def clear(self):
        self.selected = set()
    def iter(self):
        return iter(self.selected)
    def select(self, item):
        if item is not None:
            try:
                if item.isAtom():
                    item = [item]
            except AttributeError:
                pass

            self.selected.update(item)

