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
        handler =  self._getHandlerForStep(elements)
        fileList = self._getFilesForStep(elements)
        return self.fileListToElements(elements, handler, fileList)

    def fileListToElements(self, elements, handler, fileList, **kw):
        for filename in fileList:
            handler.setFilename(filename)
            self.fileToElements(elements, handler, filename, **kw)
        return elements

    def _getHandlerForStep(self, elements):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def _getFilesForStep(self, elements):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def fileToElements(self, elements, handler, srcfile):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

