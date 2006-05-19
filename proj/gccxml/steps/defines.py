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

import re
from external import GCCXMLProcessStep

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DefinesHandler(object):
    active = False
    lineno = 0
    filename = None

    def __init__(self, host, elements):
        self.host = host
        self.elements = elements

    def onPreParseLine(self, line):
        pass
    def onPostParseLine(self, line):
        self.lineno += 1

    def onPosition(self, filename, lineno):
        self.filename = filename
        self.lineno = int(lineno)
        self.active = filename in self.host.dependencies
        #print 'file:', filename, lineno

    def onDefine(self, name, definition):
        if self.active:
            print '%s:%d: DEFINE %r %r' % (self.filename, self.lineno, name, definition)

    def onMacro(self, name, params, definition):
        if self.active:
            print '%s:%d: MACRO %r %r' % (self.filename, self.lineno, name, definition)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DefinesProcessorStep(GCCXMLProcessStep):
    command = r"gccxml -E -dD %(srcfile)s %(includes)s > '%(outfile)s'"
    HandlerFactory = DefinesHandler

    def hostVisitStep(self, host):
        host.visitElementStep(self)

    def findElements(self, elements):
        self.handler = self.HandlerFactory(self.host, elements)
        result = self.fileListToElements(elements, self._getSourceFiles())
        del self.handler
        return result

    def fileListToElements(self, elements, fileList, **kw):
        elements = {}
        for filename in fileList:
            self.fileToElements(elements, filename, **kw)
        return elements

    def fileToElements(self, elements, srcfile):
        crucher = self._processSrcFile(srcfile, 'defines-' + srcfile)
        self.scanFile(self.handler, crucher.outfile)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Define processing section 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    re_filePosition = re.compile(r'''#\s*(\d+)\s*(["'])(.*?)\2''')
    re_s_ident = '[A-Za-z_][A-Za-z0-9_]*'
    re_define = re.compile(
            (r'\s*#\s*define\s+(%(ident)s)\s*' % dict(ident=re_s_ident)) + 
            (r'\s*(.*)'))
    re_macro = re.compile(
            (r'\s*#\s*define\s+(%(ident)s)\s*\(\s*' % dict(ident=re_s_ident)) + 
            (r'((?:%(ident)s\s*)(?:,\s*%(ident)s\s*)*)' % dict(ident=re_s_ident)) + 
            (r'\s*\)\s*(.*)'))
    exprMatchList = []

    def matchFilePosition(self, handler, line, match):
        lineno, _, filename = match.groups()
        handler.onPosition(filename, lineno)
    exprMatchList.append((re_filePosition, matchFilePosition))

    def matchMacro(self, handler, line, match):
        name, params, definition = match.groups()
        handler.onMacro(name, params, definition)
    exprMatchList.append((re_macro, matchMacro))

    def matchDefine(self, handler, line, match):
        name, definition = match.groups()
        handler.onDefine(name, definition)
    exprMatchList.append((re_define, matchDefine))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def scanFile(self, handler, fileToScan):
        exprMatchList = self.exprMatchList
        scanLine = self.scanLine

        for line in fileToScan:
            handler.onPreParseLine(line)
            scanLine(handler, line, exprMatchList)
            handler.onPostParseLine(line)

    def scanLine(self, handler, line, exprMatchList):
        for re_expr, onMatch in exprMatchList:
            match = re_expr.match(line)
            if match is not None:
                onMatch(self, handler, line, match)
                break

