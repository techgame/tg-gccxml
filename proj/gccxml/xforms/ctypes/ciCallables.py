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

from ciBase import CodeItem
from ciTypes import TypeCodeItem

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CIEllipsis = None

class CIArgument(CodeItem):
    @property
    def name(self):
        return self.item.name

    def getHostCI(self):
        return None

    def typeRef(self, require=True):
        if require: self.require()
        return self.typeRefFor(self.item.type)

class CIEllipsis(CodeItem):
    def getHostCI(self):
        return None

    def typeRef(self, require=True):
        if require: self.require()
        raise NotImplementedError()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CallableCodeItem(CodeItem):
    templateArgIndex = 'arg_%s'

    def argTypeRefs(self, arguments=None):
        arguments = arguments or self.item.arguments
        return [self.typeRefFor(a) for a in arguments]
    def joinArgTypeRefs(self, sep=', '):
        return sep.join(self.argTypeRefs())

    def argNames(self, arguments=None):
        def argName(idx, a):
            return a.name or (self.templateArgIndex % idx)

        arguments = arguments or self.item.arguments
        return [argName(idx,a) for idx, a in enumerate(arguments)]
    def joinArgNames(self, sep=', '):
        return sep.join(self.argNames())

    def retTypeRef(self):
        return self.typeRefFor(self.item.returns)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIFunctionType(CallableCodeItem, TypeCodeItem):
    _required = False
    funcTypeTemplate = 'CFUNCTYPE(%(retTypeRef)s, %(argTypeRefs)s)'

    def writeTo(self, stream):
        print >> stream, self._typeDecl()
        
    def typeRef(self, require=True):
        if require: self.require()
        return self._typeDecl()

    def _typeDecl(self):
        return self.funcTypeTemplate % dict(
                    retTypeRef=self.retTypeRef(),
                    argTypeRefs=self.joinArgTypeRefs(),
                    )

class CIFunction(CallableCodeItem):
    bind = 'bind'
    decoTemplate = '@%(bind)s(%(retTypeRef)s, [%(argTypeRefs)s])'
    funcTemplate = 'def %(funcName)s(%(paramNames)s): pass\n'

    def writeTo(self, stream):
        print >> stream, self.decoDecl()
        print >> stream, self.funcDecl()

    def decoDecl(self):
        return self.decoTemplate % dict(
            bind=self.bind,
            retTypeRef=self.retTypeRef(),
            argTypeRefs=self.joinArgTypeRefs(),
            )

    def funcDecl(self):
        return self.funcTemplate % dict(
            funcName=self.name,
            paramNames=self.joinArgNames())

    @property
    def name(self):
        return self.item.name

