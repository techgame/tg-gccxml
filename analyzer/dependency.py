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
import tempfile

from base import ScannerStep
from external import GCCXMLProcessStep, GCCXMLPreprocessorStep
from handlers.makefileRule import MakefileRuleScanner
from handlers.cpreprocessor import DependencyScannerBase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BaselineScannerStep(ScannerStep):
    def _getFilesForStep(self, elements):
        return self._getSourceFiles()

    def _getBaselineSourceFiles(self):
        return self.config.files.get('baseline', [])

    def initScanner(self, scanner, elements, emitter):
        filelist = self._getBaselineSourceFiles()
        if not filelist:
            aBaseline = tempfile.NamedTemporaryFile('w', suffix='.c')
            aBaseline.write('''void main() {}''')
            aBaseline.flush()
            filelist = [aBaseline.name]

        scanner.baselineMode = True
        try:
            for basesrcfile in filelist:
                self.fileToElements(elements, emitter, basesrcfile)
        finally:
            scanner.baselineMode = False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GCCDependencyProcessorStep(BaselineScannerStep, GCCXMLProcessStep):
    command = r'gcc -E -MT TARGET -M %(srcfile)s %(includes)s > "%(outfile)s"'
    #allowFrameworkInclude = True
    ScannerFactory = MakefileRuleScanner

    def _getEmitterForStep(self, elements):
        return elements.getEmitterFor('dependency', 'makefile')
    def fileToElements(self, elements, emitter, srcfile):
        scanner = self.getScanner(elements, emitter)

        cruncher, outfile = self._processSrcFile(srcfile, 'depends-'+os.path.basename(srcfile)+'.mak')
        scanner(emitter, outfile)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IncludeStackDependencyProcessorStep(BaselineScannerStep, GCCXMLPreprocessorStep):
    ScannerFactory = DependencyScannerBase
    command = r'gccxml -E -dD %(srcfile)s %(includes)s > "%(outfile)s"'

    def _getEmitterForStep(self, elements):
        return elements.getEmitterFor('dependency', 'preprocessor')
    def fileToElements(self, elements, emitter, srcfile):
        scanner = self.getScanner(elements, emitter)

        filename = 'pp-' + os.path.basename(srcfile)
        subproc, outfile = self._processSrcFile(srcfile, filename)
        try:
            scanner(emitter, outfile)
        finally:
            outfile.close()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#DependencyProcessorStep = GCCDependencyProcessorStep
DependencyProcessorStep = IncludeStackDependencyProcessorStep

