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

from TG.gccxml.model import visitor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Code Node Visitor
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BaseCodeItemVisitor(visitor.DependencyAtomVisitor):
    context = None
    def __init__(self, context):
        self.context = context
        self.map = dict()

    @classmethod
    def validateFactories(klass):
        invalidFactories = [n for n,v in vars(klass).items() if v is None and n.startswith('CI')]

        if invalidFactories:
            e = Exception("Invalid code item factories: [%s]" % (', '.join(invalidFactories),))
            e.invalidFactories = invalidFactories
            raise e
        else:
            return True

    def _visitAtom(self, atom):
        ci = self.map.get(atom, None)
        if ci is None:
            ci = atom.visit(self)
            atom.visitDependencies(self)
            self.map[atom] = ci
        return ci

    def iterCodeItems(self):
        return self.map.itervalues()

BaseCodeItemVisitor.validateFactories()

