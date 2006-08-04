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

from TG.gccxml.model.visitor import AtomFilterVisitor, DependencyAtomVisitor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DotItem(object):
    def __init__(self, atom):
        self.atom = atom
    def addDependencies(self, dependencyList):
        self.dependencies = dependencyList

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DigraphItemVisitor(DependencyAtomVisitor):
    def __init__(self, context):
        self.context = context

    def _visitAtom(self, atom, *args, **kw):
        ci = atom.visit(self, *args, **kw)
        if ci is None:
            ci = DotItem(atom)
            self.context.append(ci)
        atom.visitChildren(self, ci=ci)
        atom.visitDependencies(self, ci=ci)
        return ci

    def onVisitDependenciesOf(self, atom, iterDependencies, ci):
        dependencies = list(iterDependencies)
        ci.addDependencies(dependencies)
        return DependencyAtomVisitor.onVisitDependenciesOf(self, atom, iter(dependencies))

