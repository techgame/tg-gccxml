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

class CodeItem(object):
    def __init__(self, context, item):
        self.item = proxy(item)
        item.codeItem = self

    @property
    def codeItem(self):
        return self

    def isTopLevel(self):
        return True

    def ref(self):
        return self.codeRef()
    def codeRef(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def codeDef(self):
        return ''

    def refFor(self, item):
        ci = getattr(item, 'codeItem', None)
        if ci:
            return ci.codeRef()
        else: return ''
    def codeFor(self, item):
        ci = getattr(item, 'codeItem', None)
        if ci:
            return ci.codeDef()
        else: return ''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class NamedCodeItem(CodeItem):
    def codeRef(self):
        return self.item.name

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class NullCodeItem(CodeItem):
    def isTopLevel(self):
        return False

    def codeRef(self):
        return ''

    def codeDef(self):
        return ''

