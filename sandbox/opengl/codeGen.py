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
        if item.extern and item.name.startswith('gl'):
            self.select(item)

    def onPPInclude(self, item):
        print '"%s" includes "%s"' % (item.file.name, item.filename)

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
        ciFile.importAll('_ctypes_opengl')

    gl = context['OpenGL/gl.h']

    glext = context['OpenGL/glext.h']
    glext.importAll(gl)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    context.outputPath = 'out'
    print
    print "Writing out ctypes code:"
    print "========================"
    for ciFile in [gl, glext]:
        print 'Writing:', ciFile.filename
        ciFile.writeToFile()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    main()

