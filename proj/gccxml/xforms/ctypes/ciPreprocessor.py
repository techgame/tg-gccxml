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

class CIPPInclude(CodeItem): 
    pass

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

class CIPPDefine(CodeItem): 
    def writeTo(self, stream):
        if self.item.body[:1].isalpha():
            # TODO: handle out of order constants more elegantly
            print >> stream, '# TODO: Rearrange for dependency'
            print >> stream, '# %s = %s' % (self.item.ident, self.item.body)
        else:
            print >> stream, '%s = %s' % (self.item.ident, self.item.body)

class CIPPMacro(CodeItem): 
    def writeTo(self, stream):
        name, args, body = (self.item.ident, ', '.join(self.item.args), self.item.body)
        print >> stream, 'def %s(%s):' % (name, args)
        print >> stream, '    """#define %s(%s) %s"""' % (name, args, body)

