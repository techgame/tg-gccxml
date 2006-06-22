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

from weakref import proxy

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Code generation
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def asCodeItem(self):
    if self.isAtom():
        return self.codeItem
    else: return self

class CodeItem(object):
    asCodeItem = asCodeItem

    def __new__(klass, context, item):
        ci = getattr(item, 'codeItem', None)
        if ci is not None:
            return ci
        return object.__new__(klass, context, item)

    def __init__(self, context, item):
        self.item = item
        item.codeItem = self

        self._initialize()

    def _initialize(self):
        pass

    def isAtom(self):
        return False
    def isCodeItem(self):
        return True

    def getHostCI(self):
        return asCodeItem(self.item.file)

    def emit(self):
        ciHost = self.getHostCI()
        if ciHost:
            ciHost.add(self)

    def writeTo(self, stream):
        print >> stream, '#', self.item.__repr__(True), self.loc

    @property
    def line(self): return self.item.line
    @property
    def file(self): return self.item.file
    @property
    def loc(self):
        return '"%s":%s' % (self.item.file.name, self.item.line)

