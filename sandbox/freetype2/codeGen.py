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

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    includePrefixes = set([
        'FREETYPE', 'FT', 'TT',
        ])
    exludeDefines = set([
        'FT_CHAR_BIT',
        'FT_ALIGNMENT',
        'FT_MACINTOSH',
        'FT_INT64',
        'FT_BEGIN_STMNT',
        'FT_END_STMNT',
        'FT_DUMMY_STMNT',
        'FT_CALLBACK_TABLE',
        'FT_CALLBACK_TABLE_DEF',

        'FT_ERR_PREFIX',
        'FT_ERR_BASE',
        'FT_ERROR_START_LIST',
        'FT_ERROR_END_LIST',

        'FT_MODERR_START_LIST',
        'FT_MODERR_END_LIST',

        'FT_UINT_MAX',
        'FT_ULONG_MAX',

        'FT_Outline_MoveTo_Func',
        'FT_Outline_LineTo_Func',
        'FT_Outline_ConicTo_Func',
        'FT_Outline_CubicTo_Func',
        'FT_Raster_Span_Func',
        'FT_Raster_New_Func',
        'FT_Raster_Done_Func',
        'FT_Raster_Reset_Func',
        'FT_Raster_Set_Mode_Func',
        'FT_Raster_Render_Func',
        ])

    def onPPDefine(self, item):
        body = item.body
        ident = item.ident
        if not item.body:
            return

        prefix = ident[:ident.find('_')]
        if prefix not in self.includePrefixes:
            return
        if 'SIZEOF' in ident:
            return
        if 'LOAD_TARGET' in ident:
            return
        if ident in self.exludeDefines:
            return

        if body.lower().startswith('0x'):
            if body[-1:] == 'U':
                item.body = body[:-1]

        self.select(item)

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

    ciFilesByName.pop('ftheader.h', None)
    ciFilesByName.pop('fterror.h', None)
    ciFilesByName.pop('ftstdlib.h', None)
    ciFilesByName.pop('internal.h', None)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ftconfig = ciFilesByName.pop('ftconfig.h')
    ftconfig.lines.insert(0, (0, '#~ Code block from "%s" ~~~\n' % (ftconfig.name,)))

    ftoption = ciFilesByName.pop('ftoption.h')
    ftoption.lines.insert(0, (0, '#~ Code block from "%s" ~~~\n' % (ftoption.name,)))

    for ciFile in ciFilesByName.itervalues():
        ciFile.importAll('_ctypes_freetype')

    fttypes = ciFilesByName['fttypes.h']
    fttypes.prependFiles = [ftconfig, ftoption]
    fttypes.lines.insert(0, (0, '#~ Code block from "%s" ~~~\n' % (fttypes.name,)))

    ftimage = ciFilesByName['ftimage.h']
    ftimage.importAll(fttypes)

    ftsystem = ciFilesByName['ftsystem.h']
    ftsystem.importAll(fttypes)

    freetype = ciFilesByName['freetype.h']
    freetype.importAll(fttypes, ftimage, ftsystem)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    context.outputPath = 'out'
    for ciFile in ciFilesByName.values():
        print 'Writing:', ciFile.filename
        ciFile.blockSeparator = ''
        ciFile.writeToFile()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    main()

