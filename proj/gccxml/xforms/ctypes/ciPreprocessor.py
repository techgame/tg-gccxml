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

class CIPPDefine(CodeItem): 
    template = '%(ident)s = %(body)s'

    def writeTo(self, stream):
        print >> stream, self.template % dict(
                                ident=self.item.ident, 
                                body=self.getDefineBody())

    def getDefineBody(self):
        body = self.item.body

        if not body[:1].isalpha():
            return body

        derefList = []
        ppDefines = self.item.file.root.ppDefines
        while body[:1].isalpha():
            nextDefine = ppDefines.get(body, None)
            if nextDefine is None: 
                return body
            elif body == nextDefine.body: 
                return body
            else:
                derefList.append(body)
                body = nextDefine.body
        return body + ' # = ' + ' = '.join(derefList)

class CIPPMacro(CodeItem): 
    template = (
        'def %(ident)s(%(args)s):\n'
        '    """#define %(ident)s(%(args)s) %(body)s"""')
            
    def writeTo(self, stream):
        print >> stream, self.template % dict(
                                ident=self.item.ident, 
                                args=self.joinArgNames(), 
                                body=self.item.body,
                                )

    def argNames(self):
        return self.item.args
    def joinArgNames(self, sep=', '):
        return sep.join(self.argNames())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIPPInclude(CodeItem): 
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIPPConditional(CodeItem): 
    def writeTo(self, stream):
        if self.item.isOpening():
            print >> stream, 'if 1: # %s %s (%s)' % (self.item.directive, self.item.body, self.loc)
            stream.indent()
            print >> stream, '"""%s"""' % (self.item.body,)

        elif self.item.isAlternate():
            stream.dedent()
            if self.item.directive != 'else':
                print >> stream, 'elif 1: # %s %s (%s)' % (self.item.directive, self.item.body, self.loc)
                stream.indent()
                print >> stream, '"""%s"""' % (self.item.body,)

            else:
                print >> stream, 'else: # %s %s (%s)' % (self.item.directive, self.item.prev.body, self.loc)
                stream.indent()
                print >> stream, '"""%s"""' % (self.item.prev.body,)

        elif self.item.isClosing():
            stream.dedent()

