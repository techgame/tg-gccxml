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

    def _getEmitterForStep(self, elements):
        return elements.getEmitterFor('code', 'gccxml')
    def _getFilesForStep(self, elements):
        return self._getSourceFiles()

    def fileToElements(self, elements, emitter, srcfile):
        scanner = self.getScanner(elements, emitter)

        cruncher = self._processSrcFile(srcfile, 'code-'+os.path.basename(srcfile)+'.xml')
        scanner(emitter, cruncher.outfile)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _scanner = None
    def getScanner(self, elements, emitter):
        if self._scanner is None:
            self.createScanner(elements, emitter)
        return self._scanner
    def setScanner(self, scanner):
        self._scanner = scanner

    def createScanner(self, elements, emitter):
        scanner = GCCXMLScanner()
        self.setScanner(scanner)

