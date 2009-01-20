##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2006  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

__all__ = ['AtomFilterVisitor', 'CodeGenContext']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
from bisect import insort, bisect_left, bisect_right

from TG.gccxml import model
from TG.gccxml.model.visitor import AtomFilterVisitor

from codeItemVisitor import BaseCodeItemVisitor
from blockWriter import BlockWriter

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CodeGenContext(object):
    CodeItemVisitor = None # should be a concrete instance of BaseCodeItemVisitor

    root = None
    atomFilter = None

    def __init__(self, root, atomFilter=None):
        self.root = root
        self.atomFilter = atomFilter

    @classmethod
    def fromFileNamed(klass, rootModelFileName, atomFilter=None):
        root = model.loadFromFileNamed(rootModelFileName)
        return klass(root, atomFilter)

    @classmethod
    def fromFile(klass, rootModelFile, atomFilter=None):
        root = model.loadFromFile(rootModelFile)
        return klass(root, atomFilter)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __getitem__(self, key):
        return self.ciRoot[key]
    def __iter__(self):
        return iter(self.ciRoot)

    _ciRoot = None
    def getCIRoot(self):
        if self._ciRoot is None:
            self.run()
        return self._ciRoot
    def setCIRoot(self, ciRoot):
        self._ciRoot = ciRoot
    ciRoot = property(getCIRoot, setCIRoot)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getSelected(self):
        if self.atomFilter.selected is None:
            self._runAtomFilter()
        return self.atomFilter.selected
    selected = property(getSelected)

    _codeItemVisitor = None
    def getCodeItemVisitor(self):
        if self._codeItemVisitor is None:
            self.createCodeItemVisitor()
        return self._codeItemVisitor
    def setCodeItemVisitor(self, codeItemVisitor):
        self._codeItemVisitor = codeItemVisitor
    codeItemVisitor = property(getCodeItemVisitor, setCodeItemVisitor)

    def createCodeItemVisitor(self):
        codeItemVisitor = self.CodeItemVisitor(self)
        self.setCodeItemVisitor(codeItemVisitor)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def run(self):
        self._runAtomFilter()
        self._runCodeItemVisitor()

    def _runAtomFilter(self):
        self.atomFilter.clear()
        return self.atomFilter.visit(self.root)

    def _runCodeItemVisitor(self):
        self.codeItemVisitor.visit(self.root)
        self.ciRoot = self.root.codeItem

        #self.codeItemVisitor.visitAll(self.root.files.itervalues())

        self.codeItemVisitor.visitAll(self.selected)
        for ci in self.codeItemVisitor.iterCodeItems():
            if ci is not None:
                ci.emit()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ File generation utilities
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _outputPath = ''
    def getOutputPath(self):
        return self._outputPath
    def setOutputPath(self, outputPath):
        self._outputPath = outputPath
    outputPath = property(getOutputPath, setOutputPath)

    def makeOutputPath(self):
        outputPath = self.getOutputPath()
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
            return True
        else: return False

    def getOutputFilename(self, filename):
        return os.path.join(self.getOutputPath(), filename)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createStream(self, filename):
        filename = self.getOutputFilename(filename)

        for try_ in (1, 2):
            try:
                stream = open(filename, 'wb')
            except IOError, e:
                if (e.errno == 2):
                    if self.makeOutputPath():
                        continue
                raise

        return self.asBlockStream(stream)

    def asBlockStream(self, stream):
        return BlockWriter.wrap(stream)

