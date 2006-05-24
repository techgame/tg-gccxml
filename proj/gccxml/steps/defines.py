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

from external import GCCXMLProcessStep
from handlers import FileLineBaseHandler
from handlers.cpreprocessor import PreprocessorDefinesScanner

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DefinesHandler(FileLineBaseHandler):
    def emit(self, kind, args):
        print 'emit:', kind, args
    def onPosition(self, filename, lineno):
        self.setFileAndLine(filename, lineno)
    def onDefine(self, name, definition):
        self.addElement('DEFINE', definition)
    def onMacro(self, name, params, definition):
        self.addElement('MACRO', (params, definition))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DefinesProcessorStep(GCCXMLProcessStep):
    command = r"gccxml -E -dD %(srcfile)s %(includes)s > '%(outfile)s'"
    HandlerFactory = DefinesHandler
    scanner = PreprocessorDefinesScanner()

    def hostVisitStep(self, host):
        host.visitElementStep(self)

    def findElements(self, elements):
        self.handler = self.HandlerFactory(elements)
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
        self.scanner(self.handler, crucher.outfile)

