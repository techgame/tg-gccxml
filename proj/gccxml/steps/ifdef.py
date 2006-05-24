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
from handlers import FileLineBaseHandler
from handlers.cpreprocessor import ConditionsScanner

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IfdefProcessorStep(ProcessStep):
    HandlerFactory = FileLineBaseHandler
    scanner = ConditionsScanner()

    def hostVisitStep(self, host):
        host.visitElementStep(self)

    def findElements(self, elements):
        self.handler = self.HandlerFactory(elements)
        result = self.fileListToElements(elements, elements.getDependencies())
        del self.handler
        return result

    def fileListToElements(self, elements, fileList, **kw):
        elements = {}
        for filename in fileList:
            self.fileToElements(elements, filename, **kw)
        return elements

    def fileToElements(self, elements, srcfile):
        srcfile = open(srcfile, 'rb')
        try:
            self.scanner(self.handler, srcfile)
        finally:
            srcfile.close()

