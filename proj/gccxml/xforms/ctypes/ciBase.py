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
    if self is None:
        return None
    elif self.isAtom():
        return getattr(self, 'codeItem', None)
    else: 
        return self

class CodeItem(object):
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

    def __nonzero__(self):
        return self.isRequired()

    _required = True
    def isRequired(self):
        return True
        return self._required
    def require(self, required=True):
        #if not self._required:
        #    print self.item
        self._required = required

    def isAtom(self):
        return False
    def isCodeItem(self):
        return True

    def getHostCI(self):
        return asCodeItem(self.item.file)

    def emit(self):
        ciHost = self.getHostCI()
        if ciHost is not None:
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

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def typeRefFor(self, atom):
        ci = asCodeItem(atom)
        return ci.typeRef()
    
    def ptrTypeRefFor(self, atom):
        ci = asCodeItem(atom)
        if ci is not None:
            return ci.ptrTypeRef()


