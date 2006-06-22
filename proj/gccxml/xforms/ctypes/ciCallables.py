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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CIEllipsis = None

class CIArgument(CodeItem):
    def isTopLevel(self):
        return False

    def codeRef(self):
        return self.item.name

    def codeDef(self):
        raise NotImplementedError()

class CIEllipsis(CodeItem):
    def isTopLevel(self):
        return False

    def codeRef(self):
        raise NotImplementedError()

    def codeDef(self):
        raise NotImplementedError()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CICallable(CodeItem):
    bindCall = 'bind'
    unnamedArgTemplate = 'arg_%s'

    def argumentReferences(self, arguments=None):
        arguments = arguments or self.item.arguments
        return [self.refFor(a) for a in arguments]

    def argumentNames(self, arguments=None):
        def argName(idx, a):
            return a.name or (self.unnamedArgTemplate % idx)

        arguments = arguments or self.item.arguments
        return [argName(idx,a) for idx, a in enumerate(arguments)]

    def returnReference(self):
        returns = self.item.returns
        if returns:
            return self.refFor(returns)
        else: return 'None'

    def refBindCall(self):
        return self.bindCall

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIFunctionType(CICallable):
    bindCall = 'CFUNCTYPE'
    template = (
        '%(bindCall)s(%(returnType)s, [%(paramTypes)s])'
        )

    def codeRef(self):
        return self.codeDef()

    def codeDef(self):
        return self.template % dict(
                    bindCall=self.refBindCall(),
                    returnType=self.returnReference(),
                    paramTypes=', '.join(self.argumentReferences()),
                    )

class CIFunction(CICallable):
    template = (
        'def %(funcName)s(%(paramNames)s): pass\n'
        )
    templateTypeDecorator = (
        '@%(bindCall)s(%(returnType)s, [%(paramTypes)s])'
        )

    def codeRef(self):
        return self.item.name

    def codeDef(self):
        return '\n'.join([
                self.codeTypeDecorator(),
                self.codeFuncDecl(),
                ])

    def codeTypeDecorator(self):
        return self.templateTypeDecorator % dict(
            bindCall=self.refBindCall(),
            returnType=self.returnReference(),
            paramTypes=', '.join(self.argumentReferences()),
            )

    def codeFuncDecl(self):
        return self.template % dict(
            funcName=self.ref(),
            paramNames=', '.join(self.argumentNames()))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIMethod(CodeItem):
    pass

class CIConstructor(CodeItem):
    pass

class CIDestructor(CodeItem):
    pass

