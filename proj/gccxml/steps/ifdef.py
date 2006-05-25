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
    def _getEmitterForStep(self, elements):
        return elements.getEmitterFor('preprocess', 'conditional')
    def _getFilesForStep(self, elements):
        return elements.getDependencies()

    def fileToElements(self, elements, emitter, srcfile):
        scanner = self.getScanner(elements, emitter)

        srcfile = open(srcfile, 'rb')
        try:
            scanner(emitter, srcfile)
        finally:
            srcfile.close()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _scanner = None
    def getScanner(self, elements, emitter):
        if self._scanner is None:
            self.createScanner(elements, emitter)
        return self._scanner
    def setScanner(self, scanner):
        self._scanner = scanner

    def createScanner(self, elements, emitter):
        scanner = ConditionsScanner()
        self.setScanner(scanner)

