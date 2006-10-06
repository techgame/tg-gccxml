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

    _argTypeRefs = None
    def argTypeRefs(self):
        if self._argTypeRefs is None:
            self._argTypeRefs = [self.typeRefFor(a) for a in self.item.arguments]
        return self._argTypeRefs
    def joinArgTypeRefs(self, sep=', '):
        return sep.join(self.argTypeRefs())

    _argNames = None
    def argNames(self):
        if self._argNames is None:
            def argName(idx, a):
                return a.name or (self.templateArgIndex % idx)
            self._argNames = [argName(idx,a) for idx, a in enumerate(self.item.arguments)]
        return self._argNames
    def joinArgNames(self, sep=', '):
        return sep.join(self.argNames())

    def retTypeRef(self):
        return self.typeRefFor(self.item.returns)

    def argsAndTypes(self):
        return zip(self.argNames(), self.item.arguments)
    def argsAndTypeRefs(self):
        return zip(self.argNames(), self.argTypeRefs())

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

    funcTemplate = (
            'def %(funcName)s(%(paramNames)s%(api)s): '
            )

    api = '_api_'
    apicallTemplate = 'return %(api)s(%(paramNames)s)\n'

    sepArgsToTypes = '\n    '
    docTemplate = (
            '"""%(funcName)s(%(paramNames)s)\n'
            + sepArgsToTypes + '%(argsToTypes)s\n'
            '"""')

    def writeTo(self, stream):
        deco = self.decoDecl()
        func = self.funcDecl()
        doc = self.docDecl()
        apiCall = self.apicallDecl()

        if deco:
            print >> stream, deco

        if not doc and not apiCall:
            print >> stream, func, 'pass'

        else:
            print >> stream, func
            stream.indent()

            if doc: 
                print >> stream, doc
            if apiCall: 
                print >> stream, apiCall

            stream.dedent()

    def decoDecl(self):
        return self.decoTemplate % dict(
            bind=self.bind,
            retTypeRef=self.retTypeRef(),
            argTypeRefs=self.joinArgTypeRefs())

    def funcDecl(self):
        paramNames=self.joinArgNames()
        api = '%s%s=None' % (paramNames and ', ' or '', self.api)
        return self.funcTemplate % dict(
            funcName=self.name,
            paramNames=paramNames,
            api=api)

    def apicallDecl(self):
        return self.apicallTemplate % dict(
            funcName=self.name,
            paramNames=self.joinArgNames(),
            api=self.api)

    def docDecl(self):
        return self.docTemplate % dict(
            funcName=self.name,
            paramNames=self.joinArgNames(), 
            argsToTypes=self.joinArgsAndTypeRefs())

    def joinArgsAndTypeRefs(self, fmtStr='%s : %s', sep=sepArgsToTypes):
        return sep.join(fmtStr % e for e in self.argsAndTypeRefs())


    @property
    def name(self):
        return self.item.name

