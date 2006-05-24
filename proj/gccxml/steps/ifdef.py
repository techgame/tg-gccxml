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
from base import ProcessStep

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IfdefHandler(object):
    indent = 0
    def __init__(self, elements):
        self.elements = elements

    def onPreParseLine(self, line):
        pass
    def onPostParseLine(self, line):
        self.lineno += 1

    def onPosition(self, filename, lineno):
        self.filename = filename
        self.lineno = int(lineno)

    def onPreprocessorIf(self, kind, expr):
        print self.indent*'    ', self.indent,
        print '%s:%d: #OPEN %r %r' % (self.filename, self.lineno, kind, expr)
        self.indent += 1
    def onPreprocessorElseIf(self, kind, expr):
        self.indent -= 1
        print self.indent*'    ', self.indent,
        print '%s:%d: #ELSE %r %r' % (self.filename, self.lineno, kind, expr)
        self.indent += 1
    def onPreprocessorEndif(self, kind, expr):
        self.indent -= 1
        print self.indent*'    ', self.indent,
        print '%s:%d: #CLOSE %r %r' % (self.filename, self.lineno, kind, expr)
        print

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IfdefProcessorStep(ProcessStep):
    HandlerFactory = IfdefHandler

    def hostVisitStep(self, host):
        host.visitElementStep(self)

    def findElements(self, elements):
        self.handler = IfdefHandler(self.host, elements)
        result = self.fileListToElements(elements, self.host.dependencies)
        del self.handler
        return result

    def fileListToElements(self, elements, fileList, **kw):
        elements = {}
        for filename in fileList:
            self.fileToElements(elements, filename, **kw)
        return elements

    def fileToElements(self, elements, srcfile):
        self.handler.onPosition(srcfile, 1)
        srcfile = open(srcfile, 'rb')
        try:
            self.scanFile(self.handler, srcfile)
        finally:
            srcfile.close()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Define processing section 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    re_prefix = re.compile(r'^\s*#\s*')
    re_if = re.compile(r'(ifndef|ifdef|if)\b\s*(.*)\s*')
    re_else = re.compile(r'(elif|else)\b\s*(.*)\s*')
    re_endif = re.compile(r'(endif)\b\s*(.*)\s*')
    exprMatchList = []

    def matchPreprocessorIf(self, handler, line, match):
        kind, expr = match.groups()
        handler.onPreprocessorIf(kind, expr)
    exprMatchList.append((re_if, matchPreprocessorIf))

    def matchPreprocessorElse(self, handler, line, match):
        kind, expr = match.groups()
        handler.onPreprocessorElseIf(kind, expr)
    exprMatchList.append((re_else, matchPreprocessorElse))

    def matchPreprocessorEndif(self, handler, line, match):
        kind, expr = match.groups()
        handler.onPreprocessorEndif(kind, expr)
    exprMatchList.append((re_endif, matchPreprocessorEndif))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def scanFile(self, handler, fileToScan):
        exprMatchList = self.exprMatchList
        scanLine = self.scanLine

        for line in fileToScan:
            handler.onPreParseLine(line)
            scanLine(handler, line, exprMatchList)
            handler.onPostParseLine(line)

    def scanLine(self, handler, line, exprMatchList):
        match = self.re_prefix.match(line)
        if match is None: 
            return None

        line = line[match.end():]
        for re_expr, onMatch in exprMatchList:
            match = re_expr.match(line)
            if match is not None:
                onMatch(self, handler, line, match)
                return True
        else:
            return False

