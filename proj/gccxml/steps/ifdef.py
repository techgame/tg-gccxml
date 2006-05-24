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
from base import ElementFileStepMixin, ProcessStep
from handlers.cpreprocessor import ConditionsScanner

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IfdefProcessorStep(ElementFileStepMixin, ProcessStep):
    def _getHandlerForStep(self, elements):
        return elements.getHandleFor('preprocess', 'conditional')
    def _getFilesForStep(self, elements):
        return elements.getDependencies()

    def fileToElements(self, elements, handler, srcfile):
        srcfile = open(srcfile, 'rb')
        try:
            self.scanner(handler, srcfile)
        finally:
            srcfile.close()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _scanner = None
    def getScanner(self):
        if self._scanner is None:
            self.createScanner()
        return self._scanner
    def setScanner(self, scanner):
        self._scanner = scanner
    scanner = property(getScanner, setScanner)

    def createScanner(self):
        scanner = ConditionsScanner()
        self.setScanner(scanner)

