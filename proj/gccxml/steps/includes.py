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

class IncludesProcessorStep(ElementFileStepMixin, GCCXMLProcessStep):
    command = r"gccxml -E -MT TARGET -M %(srcfile)s %(includes)s > %(outfile)s"
    scanner = MakefileRuleScanner()

    # standard out file descriptor
    stdout_fd = GCCXMLProcessStep.PIPE

    def _getHandlerForStep(self, elements):
        return elements.getHandleFor('preprocess', 'defines')
    def _getFilesForStep(self, elements):
        return self._getSourceFiles()

    def fileToElements(self, elements, handler, srcfile):
        cruncher = self._processSrcFile(srcfile, 'depends-'+os.path.basename(srcfile)+'.mak')
        self.scanner(handler, cruncher.outfile)

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
        scanner = MakefileRuleScanner()
        self.setScanner(scanner)
        self.initBaseline()

    def _getBaselineSourceFiles(self):
        return self.config.files.get('baseline', [])

    def initBaseline(self):
        filelist = self._getBaselineSourceFiles()
        if not filelist:
            aBaseline = tempfile.NamedTemporaryFile('w', suffix='.c')
            aBaseline.write('''void main() {}''')
            aBaseline.flush()
            filelist = [aBaseline.name]

        for basesrcfile in filelist:
            self.fileToElements(None, None, basesrcfile)

