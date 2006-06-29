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

import os
from TG.gccxml.xforms.ctypes import AtomFilterVisitor, CCodeGenContext

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FilterVisitor(AtomFilterVisitor):
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
    context = CCodeGenContext.fromFileNamed('srcCode.model')
    context.atomFilter = FilterVisitor()

    ciFilesByName = dict((os.path.basename(f.name), f) for f in context if f)
    for ciFile in ciFilesByName.itervalues():
        ciFile.importAll('_ctypes_freetype')

    ftconfig = ciFilesByName['ftconfig.h']
    ftimage = ciFilesByName['ftimage.h']

    fttypes = ciFilesByName['fttypes.h']
    fttypes.importAll(ftconfig, ftimage)

    ftsystem = ciFilesByName['ftsystem.h']
    ftsystem.importAll(fttypes)

    freetype = ciFilesByName['freetype.h']
    freetype.importAll(fttypes, ftsystem)

    context.outputPath = 'out'
    for ciFile in ciFilesByName.values():
        print 'Writing:', ciFile.filename
        ciFile.blockSeparator = ''
        ciFile.writeToFile()

