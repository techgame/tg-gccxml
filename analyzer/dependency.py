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

from base import ElementFileStepMixin
from external import GCCXMLProcessStep
from handlers.makefileRule import MakefileRuleScanner

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DependencyProcessorStep(ElementFileStepMixin, GCCXMLProcessStep):
    command = r"gcc -E -MT TARGET -M %(srcfile)s %(includes)s > %(outfile)s"
    #allowFrameworkInclude = True

    def _getEmitterForStep(self, elements):
        return elements.getEmitterFor('dependency', 'makefile')
    def _getFilesForStep(self, elements):
        return self._getSourceFiles()

    def fileToElements(self, elements, emitter, srcfile):
        scanner = self.getScanner(elements, emitter)

        cruncher, outfile = self._processSrcFile(srcfile, 'depends-'+os.path.basename(srcfile)+'.mak')
        scanner(emitter, outfile)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _scanner = None
    def getScanner(self, elements, emitter):
        if self._scanner is None:
            self.createScanner(elements, emitter)
        return self._scanner
    def setScanner(self, scanner):
        self._scanner = scanner

    def createScanner(self, elements, emitter):
        scanner = MakefileRuleScanner()
        self.setScanner(scanner)

        scanner.baselineMode = True
        try:
            self.initBaseline(elements, emitter)
        finally:
            scanner.baselineMode = False

    def _getBaselineSourceFiles(self):
        return self.config.files.get('baseline', [])

    def initBaseline(self, elements, emitter):
        filelist = self._getBaselineSourceFiles()
        if not filelist:
            aBaseline = tempfile.NamedTemporaryFile('w', suffix='.c')
            aBaseline.write('''void main() {}''')
            aBaseline.flush()
            filelist = [aBaseline.name]

        for basesrcfile in filelist:
            self.fileToElements(elements, emitter, basesrcfile)

