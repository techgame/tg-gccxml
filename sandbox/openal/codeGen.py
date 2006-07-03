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
        if not item.extern: return
        if item.name.startswith('al'):
            self.select(item)
        else: print item

    def onPPInclude(self, item):
        print '"%s" includes "%s"' % (item.file.name, item.filename)

    def onPPDefine(self, item):
        if item.ident in self.filterConditionals:
            return

        if item.ident.startswith('AL'):
            # Grab all AL defines
            self.select(item)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    filterConditionals = set([
        'AL_NO_PROTOTYPES',
        'ALC_NO_PROTOTYPES',
        ])
    def onPPConditional(self, item):
        if not item.isOpening():
            return 
        if item.body in self.filterConditionals:
            return

        if item.body.startswith('AL'):
            print repr(item), item.inOrder()
            self.select(item.inOrder())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    srcCodeModelFile = 'build/gccxml/srcCode.model'
    if not os.path.exists(srcCodeModelFile):
        import gen
        root = gen.main().root
        context = CCodeGenContext(root)
    else:
        context = CCodeGenContext.fromFileNamed(srcCodeModelFile)

    context.atomFilter = FilterVisitor()

    ciFilesByName = dict((os.path.basename(f.name), f) for f in context if f)

    for ciFile in ciFilesByName.itervalues():
        ciFile.importAll('_ctypes_openal')

    altypes = ciFilesByName['altypes.h']
    altypes.importAll()

    al = ciFilesByName['al.h']
    al.importAll(altypes)

    alctypes = ciFilesByName['alctypes.h']
    alctypes.importAll()

    alc = ciFilesByName['alc.h']
    alc.importAll(altypes, alctypes)

    alut = ciFilesByName['alut.h']
    alut.importAll(altypes, alctypes)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    context.outputPath = 'out'
    print
    print "Writing out ctypes code:"
    print "========================"
    for ciFile in ciFilesByName.values():
        print 'Writing:', ciFile.filename
        ciFile.writeToFile()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    main()

