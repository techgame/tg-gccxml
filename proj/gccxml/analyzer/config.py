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
import posixpath

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StepConfig(object):
    outputDir = 'build/gccxml'

    def __init__(self):
        self.files = {}
        if not os.path.isdir(self.outputDir):
            os.makedirs(self.outputDir)

    def getOutFile(self, outfile):
        if outfile:
            outfile = posixpath.join(self.outputDir, outfile)
        return outfile

    def getSourceFiles(self):
        return self.files.setdefault('src', [])
    def addSourceFiles(self, files):
        existing = self.getSourceFiles()
        existing.extend(f for f in files if f not in existing)
    src = property(getSourceFiles, addSourceFiles)

    def getBaselineFiles(self):
        return self.files.setdefault('baseline', [])
    def addBaselineFiles(self, files):
        existing = self.getBaselineFiles()
        existing.extend(f for f in files if f not in existing)
    baseline = property(getBaselineFiles, addBaselineFiles)

    def getIncludeDirs(self):
        return self.files.setdefault('inc', [])
    def addIncludeDirs(self, files):
        existing = self.getIncludeDirs()
        existing.extend(f for f in files if f not in existing)
    inc = property(getIncludeDirs, addIncludeDirs)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StepConfigVisitorMixin(object):
    ConfigFactory = StepConfig

    _config = None
    def getConfig(self):
        if self._config is None:
            self.createConfig()
        return self._config
    def setConfig(self, config):
        self._config = config
    cfg = config = property(getConfig, setConfig)

    def createConfig(self):
        self.setConfig(self.ConfigFactory())

