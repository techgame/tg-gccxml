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

import cPickle

from TG.gccxml.model import visitor
from TG.gccxml.xforms.ctypes import codeGen

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AtomFilter(visitor.AtomVisitor):
    def __init__(self):
        self.functions = list()
        self.defines = list()
        self.conditions = list()

    def onFunction(self, item):
        # TODO: Remove
        if self.functions: return

        if item.extern and item.name.startswith('gl'):
            # TODO: Remove
            if item.name.startswith('glBlend'):
                self.functions.append(item)

    def onPPDefine(self, item):
        if item.ident.startswith('GL'):
            # Grab all GL defines
            self.defines.append(item)

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
            self.conditions.append(item)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    from pprint import pprint
    root = cPickle.load(file('gen.pickle', 'rb'))

    atomFilter = AtomFilter()
    atomFilter.visit(root)

    codeVisitor = codeGen.CodeGenVisitor()
    for atom in atomFilter.functions:
        print
        print atom
        for e in atom.allDependencies():
            print '   ', e
            print '   ', e.loc
            print
        #pprint(list(atom.allDependencies()))
        #print atom
        #for e in atom.treeDependencies():
        #    print '  ->', e
        #ci = codeVisitor.visit(atom)
        #print ci

