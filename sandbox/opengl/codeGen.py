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
from TG.gccxml.xforms.context import CodeContext
from TG.gccxml.xforms.ctypes import codeGen

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GLFilterVisitor(visitor.AtomFilterVisitor):
    def onRoot(self, item):
        self.select(item)

    def onFile(self, item):
        self.select(item)

    def onFunction(self, item):
        if item.extern and item.name.startswith('gl'):
            self.select(item)

    def onPPDefine(self, item):
        if item.ident in self.filterConditionals:
            return

        if item.ident.startswith('GL'):
            # Grab all GL defines
            self.select(item)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    filterConditionals = set([
        'GL_GLEXT_PROTOTYPES',
        'GLAPI',
        'GL_TYPEDEFS_2_0',
        'GL_GLEXT_LEGACY',
        'GL_GLEXT_FUNCTION_POINTERS',
        ])
    def onPPConditional(self, item):
        if not item.isOpening():
            return 
        if item.body in self.filterConditionals:
            return
        if item.body.startswith('GL_VERSION'):
            return

        if item.body.startswith('GL'):
            # Grab all opening GL blocks to capture OpenGL Extension defines.
            # Closing and continuation blocks will be linked with the opening blocks.
            self.select(item.inOrder())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    from pprint import pprint
    root = loadFromFileNamed('srcCode.model')

    atomFilter = GLFilterVisitor()
    atomFilter.visit(root)

    context = CodeContext()
    codeVisitor = codeGen.CCodeGenVisitor(context)
    codeVisitor.visitAll(atomFilter.results)

    for a in atomFilter.results:
        ci = a.codeItem
        ci.emit()

    context.ciRoot = root.codeItem
    #context.printAll()
    context.writeToFiles()


