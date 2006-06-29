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
        self.context = context

        self._initialize()

    def _initialize(self):
        pass

    def __repr__(self, short=False):
        repr_codeItem = self.__repr_codeItem__(short)
        if not repr_codeItem:
            repr_codeItem = 'id:0x%x' % id(self)

        if short: className = self.__class__.__name__
        else: className = '.'.join([self.__class__.__module__, self.__class__.__name__])

        return '<%s: %s>' % (className, repr_codeItem)

    def __repr_codeItem__(self, short=False):
        return self.item.__repr_atom__()

    def __nonzero__(self):
        return self.isRequired() and self.isValidCodeItem()

    _required = True
    def isRequired(self):
        return self._required
    def require(self, required=True):
        self._required = required

    def isValidCodeItem(self):
        hostCI = self.getHostCI()
        if hostCI is not None:
            return hostCI.isValidCodeItem()
        else:
            return False

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
    def loc(self): return self.item.loc

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def typeRefFor(self, atom):
        ci = asCodeItem(atom)
        return ci.typeRef()
    
    def ptrTypeRefFor(self, atom, ciPtrType=None):
        ci = asCodeItem(atom)
        if ci is not None:
            return ci.ptrTypeRefFrom(ciPtrType)


