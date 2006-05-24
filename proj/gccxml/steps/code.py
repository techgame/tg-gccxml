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

from handlers.gccxml import GCCXMLScanner

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CodeProcessorStep(ElementFileStepMixin, GCCXMLProcessStep):
    command = r"gccxml %(srcfile)s %(includes)s -fxml='%(outfile)s'"

    def _getHandlerForStep(self, elements):
        return elements.getHandleFor('code', 'defines')
    def _getFilesForStep(self, elements):
        return self._getSourceFiles()

    def fileToElements(self, elements, handler, srcfile):
        cruncher = self._processSrcFile(srcfile, 'code-'+os.path.basename(srcfile)+'.xml')
        self.scanner(handler, cruncher.outfile)

    _scanner = None
    def getScanner(self):
        if self._scanner is None:
            self.createScanner()
        return self._scanner
    def setScanner(self, scanner):
        self._scanner = scanner
    scanner = property(getScanner, setScanner)

    def createScanner(self):
        scanner = GCCXMLScanner()
        self.setScanner(scanner)

