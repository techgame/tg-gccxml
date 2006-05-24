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
from handlers.cpreprocessor import DefinesScanner

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DefinesProcessorStep(GCCXMLProcessStep):
    command = r"gccxml -E -dD %(srcfile)s %(includes)s > '%(outfile)s'"
    HandlerFactory = FileLineBaseHandler
    scanner = DefinesScanner()

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
        subproc = self._processSrcFile(srcfile, 'defines-' + srcfile)
        self.scanner(self.handler, subproc.outfile)

