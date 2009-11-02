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

import os, sys

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Step Visitor
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StepVisitor(object):
    def visitStep(self, step):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def getConfig(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Steps and Step Mixins
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ProcessStep(object):
    host = None
    def visit(self, host):
        self.host = host
        self.hostVisitStep(host)
        del self.host

    def hostVisitStep(self, host):
        host.visitStep(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getConfig(self):
        return self.host.getConfig()
    config = property(getConfig)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ElementFileStepMixin(ProcessStep):
    def findElements(self, elements):
        emitter =  self._getEmitterForStep(elements)
        fileList = self._getFilesForStep(elements)
        return self.fileListToElements(elements, emitter, fileList)

    def fileListToElements(self, elements, emitter, fileList, **kw):
        for filename in fileList:
            emitter.setFilename(filename)
            self.fileToElements(elements, emitter, filename, **kw)
        return elements

    def _getEmitterForStep(self, elements):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def _getFilesForStep(self, elements):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def fileToElements(self, elements, emitter, srcfile):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ScannerStep(ElementFileStepMixin):
    ScannerFactory = None

    def fileToElements(self, elements, emitter, srcfile):
        scanner = self.getScanner(elements, emitter)

        if not os.path.exists(srcfile):
            print >> sys.stderr, 'Warning: path does not exist: %s' % (srcfile,)
            return 

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
        scanner = self.ScannerFactory()
        self.setScanner(scanner)
        self.initScanner(scanner, elements, emitter)

    def initScanner(self, scanner, elements, emitter):
        pass

PreprocessorStep = ScannerStep

