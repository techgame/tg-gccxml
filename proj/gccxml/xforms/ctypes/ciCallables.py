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
CIMethod = None
CIConstructor = None
CIDestructor = None

class CIArgument(CodeItem):
    def codeRef(self):
        return self.referenceFor(self.item.type)
    def codeDef(self):
        return ''

class CICallable(CodeItem):
    def argumentReferences(self, arguments=None):
        arguments = arguments or self.item.arguments
        result = [self.referenceFor(a) for a in arguments]
        return result
    def argumentNames(self, arguments=None, argTempalte='arg_%d'):
        arguments = arguments or self.item.arguments
        result = [(a.name or argTempalte % i) for i, a in enumerate(arguments)]
        return result

class CIFunctionType(CICallable):
    def codeRef(self):
        return self.codeDef()
    def codeDef(self):
        item = self.item
        return 'CFUNCTYPE(%s, [%s])' % (
                    self.referenceFor(item.returns), 
                    ', '.join(self.argumentReferences(item.arguments)),
                    )

class CIFunction(CICallable):
    template = (
        '@glCall(%(returnType)s, [%(paramTypes)s])\n'
        'def %(funcName)s(%(paramNames)s): pass\n'
        )

    def codeRef(self):
        return self.item.name

    def codeDef(self):
        item = self.item
        kw = dict(
            funcName=item.name,
            returnType=self.referenceFor(item.returns),
            paramTypes=', '.join(self.argumentReferences(item.arguments)),
            paramNames=', '.join(self.argumentNames(item.arguments)),
            )

        return self.template % kw

