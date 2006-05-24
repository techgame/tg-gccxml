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
from base import ElementFileStepMixin
from external import GCCXMLProcessStep
from handlers.cpreprocessor import DefinesScanner

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DefinesProcessorStep(ElementFileStepMixin, GCCXMLProcessStep):
    command = r"gccxml -E -dD %(srcfile)s %(includes)s > '%(outfile)s'"

    def _getHandlerForStep(self, elements):
        return elements.getHandleFor('preprocess', 'defines')
    def _getFilesForStep(self, elements):
        return self._getSourceFiles()

    def fileToElements(self, elements, handler, srcfile):
        subproc = self._processSrcFile(srcfile, 'defines-' + os.path.basename(srcfile))
        self.scanner(handler, subproc.outfile)

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
        scanner = DefinesScanner()
        self.setScanner(scanner)

