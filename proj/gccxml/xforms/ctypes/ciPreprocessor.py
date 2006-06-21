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

from ciBase import CodeItem, NullCodeItem

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIPPInclude(NullCodeItem): 
    pass

class CIPPConditional(CodeItem): 
    def isTopLevel(self):
        return True
    def codeDef(self):
        return '\nif 1:\n    # %s %s\n    # "%s":%s-%s\n    %s' % (
                self.item.directive, self.item.body,
                self.item.file.name, self.item.line, self.item.next.line,
                '\n    '.join(self.codeFor(a) for a in self.item.getEnclosed())
                )

class CIPPDefine(CodeItem): 
    def codeDef(self):
        return '%s = %s' % (self.item.ident, self.item.body)

class CIPPMacro(NullCodeItem): 
    pass

