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

class FilterVisitor(visitor.AtomFilterVisitor):
    def onRoot(self, item):
        self.select(item)

    def onFile(self, item):
        self.select(item)

    def onFunction(self, item):
        if item.extern and item.name.startswith('FT_'):
            self.select(item)

    def onPPDefine(self, item):
        pass

    def onPPConditional(self, item):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    from pprint import pprint
    root = loadFromFileNamed('srcCode.model')

    atomFilter = FilterVisitor()
    atomFilter.visit(root)

    context = CodeContext()
    codeVisitor = codeGen.CCodeGenVisitor(context)
    codeVisitor.visitAll(atomFilter.results)

    for ci in codeVisitor.cache.itervalues():
        if ci is not None:
            ci.emit()

    context.ciRoot = root.codeItem
    #context.printAll()
    context.writeToFiles()


