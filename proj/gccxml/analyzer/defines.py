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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DefinesProcessorStep(PreprocessorStep, GCCXMLProcessStep):
    ScannerFactory = DefinesScanner
    command = r"gccxml -E -dD %(srcfile)s %(includes)s > '%(outfile)s'"

    def _getEmitterForStep(self, elements):
        return elements.getEmitterFor('preprocess', 'defines')
    def _getFilesForStep(self, elements):
        return self._getSourceFiles()

    def fileToElements(self, elements, emitter, srcfile):
        scanner = self.getScanner(elements, emitter)

        subproc, outfile = self._processSrcFile(srcfile, 'defines-' + os.path.basename(srcfile))
        scanner(emitter, outfile)

