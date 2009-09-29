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

from base import PreprocessorStep
from external import GCCXMLProcessStep
from handlers.cpreprocessor import DefinesScanner
from handlers.funcTypedefScanner import FuncTypedefScanner

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DefinesProcessorStep(PreprocessorStep, GCCXMLProcessStep):
    ScannerFactory = DefinesScanner
    command = r'gccxml -E -dD %(srcfile)s %(includes)s > "%(outfile)s"'

    def _getEmitterForStep(self, elements):
        return elements.getEmitterFor('preprocess', 'defines')
    def _getFilesForStep(self, elements):
        return self._getSourceFiles()

    def fileToElements(self, elements, emitter, srcfile):
        scanner = self.getScanner(elements, emitter)

        filename = 'pp-' + os.path.basename(srcfile)
        subproc, outfile = self._processSrcFile(srcfile, filename)
        try:
            scanner(emitter, outfile)
        finally:
            outfile.close()

        # HACK: run through the preprocessed elements and grab the func typedef
        # argument names
        self.scanFuncTypedefArgNames(elements, filename)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _getFuncTypedefEmitter(self, elements):
        return elements.getEmitterFor('patch', 'function-type-name')
    def _getFuncTypedefScanner(self, elements, emitter):
        return FuncTypedefScanner()
    def scanFuncTypedefArgNames(self, elements, filename):
        emitter = self._getFuncTypedefEmitter(elements)
        scanner = self._getFuncTypedefScanner(elements, emitter)

        outfile = open(self._getOutFile(filename), 'rb')
        try:
            scanner(emitter, outfile)
        finally:
            outfile.close()

