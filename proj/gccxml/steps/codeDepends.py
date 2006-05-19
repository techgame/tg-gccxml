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

import tempfile
from external import GCCXMLProcessStep

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CodeDependencyStep(GCCXMLProcessStep):
    command = r"gccxml -E -MT TARGET -M %(srcfile)s %(includes)s > %(outfile)s"

    # standard out file descriptor
    stdout_fd = GCCXMLProcessStep.PIPE

    def hostVisitStep(self, host):
        host.visitDependencyStep(self)

    def findDependencies(self):
        return self.fileListToDependencies(self._getSourceFiles())

    def fileListToDependencies(self, fileList, **kw):
        # list to maintain order, set for fast searching
        result = []
        resultSet = set() 
        for filename in fileList:
            fileDeps = self.fileToDepencies(filename, **kw)
            fileDeps = [dep for dep in fileDeps if dep not in resultSet]
            result.extend(fileDeps)
            resultSet.update(fileDeps)
        return result

    def fileToDepencies(self, srcfile, filterBaseline=True):
        crucher = self._processSrcFile(srcfile, 'depends-'+srcfile+'.mak')
        aMakeFile = crucher.outfile.read()
        srcDeps = self.makefileRuleAsDeps(aMakeFile)
        if filterBaseline:
            srcDeps = (d for d in srcDeps if d not in self.getBaseline())
        return srcDeps

    @classmethod
    def makefileRuleAsDeps(klass, line):
        deps = klass.makefileRuleAsList(line)
        deps.next() # skip TARGET
        deps.next() # skip src.c
        return deps
    @classmethod
    def makefileRuleAsList(klass, makefile):
        # Note: this doesn't allow for filenames with spaces in them, but they
        # are not output by the gcc tool either.

        makefile = makefile.replace('\\ ', '\\$') # save the escaped spaces
        makefile = makefile.replace('\\\n', '') # join the split lines
        lines = makefile.splitlines()
        words = (word.replace('\\$', ' ') # replace escaped spaces
                    for line in lines 
                        for word in line.split())
        return words

    _baseline = None
    def getBaseline(self):
        if self._baseline is None:
            self.createBaseline()
        return self._baseline
    def setBaseline(self, baseline):
        self._baseline = baseline

    def createBaseline(self):
        baselineFiles = self._getBaselineSourceFiles()

        if not baselineFiles:
            aBaseline = tempfile.NamedTemporaryFile('w', suffix='.c')
            aBaseline.write('''void main() {}''')
            aBaseline.flush()
            baselineFiles = [aBaseline.name]

        baselineDeps = self.fileListToDependencies(baselineFiles, filterBaseline=False)
        self.setBaseline(baselineDeps)

    def _getBaselineSourceFiles(self):
        return self.config.files.get('baseline', [])

