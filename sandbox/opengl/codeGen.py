#!/usr/bin/env python
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

from itertools import chain

from TG.gccxml.model import loadFromFileNamed
from TG.gccxml.model import visitor
from TG.gccxml.xforms.ctypes import codeGen

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AtomFilter(visitor.AtomVisitor):
    def __init__(self):
        self.functions = set()
        self.defines = set()
        self.conditions = set()
        self.items = set()

    def iterResults(self):
        return chain(self.conditions, self.defines, self.functions, self.items)

    def iterAll(self):
        return chain(self.getDepends(), self.iterResults())

    _depends = None
    def getDepends(self):
        if self._depends is None:
            self._depends = set()
            for e in self.iterResults():
                self._depends.update(e.allDependencies())
        return self._depends

    def onFunction(self, item):
        if item.extern and item.name.startswith('gl'):
            # TODO: Restore
            return
            if 'Texture' in item.name:
                self.functions.add(item)

    def onPPDefine(self, item):
        if item.ident in self.filterConditionals:
            return

        if item.ident.startswith('GL'):
            # Grab all GL defines
            self.defines.add(item)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    filterConditionals = set([
        'GL_GLEXT_PROTOTYPES',
        'GLAPI',
        'GL_TYPEDEFS_2_0',
        'GL_GLEXT_LEGACY',
        'GL_GLEXT_FUNCTION_POINTERS',
        ])
    def onPPConditional(self, item):
        if item.body in self.filterConditionals:
            return

        if item.isOpening() and item.body.startswith('GL'):
            # Grab all opening GL blocks to capture OpenGL Extension defines.
            # Closing and continuation blocks will be linked with the opening blocks.
            self.conditions.add(item)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    from pprint import pprint
    root = loadFromFileNamed('srcCode.model')

    atomFilter = AtomFilter()
    atomFilter.visit(root)
    allAtoms = set(atomFilter.iterAll())

    codeVisitor = codeGen.CCodeGenVisitor(None)
    codeVisitor.visitAll(allAtoms)
    for atom in allAtoms:
        ci = atom.codeItem
        if ci and ci.isTopLevel():
            d = ci.codeDef()
            if d is not None:
                print d

