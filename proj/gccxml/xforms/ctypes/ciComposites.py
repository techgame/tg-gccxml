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

class CIVariable(CodeItem):
    # TODO: Implement CIVariable
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIField(CodeItem):
    # TODO: Implement CIField
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Composites
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CompositeCodeItem(CodeItem):
    # TODO: Implement CIField
    template = (
        'class %(name)s(%(bindClass)s):\n'
        '    _fields_ = [%(fields)s]'
        )
    fieldSep = '\n        '
    bindClass = 'Structure'

    def isTopLevel(self):
        return not self.item.isAnonymous()

    def codeDef(self):
        return self.template % dict(
                name=self.ref(),
                bindClass=self.refBindClass(),
                fields=self.fieldsCodeDef() or '')

    def fieldsCodeDef(self):
        fields = [self.codeFor(f) for f in self.item.members if f.isField()]
        if fields:
            fields.insert(0, '')
            return self.fieldSep.join(fields)

    def refBindClass(self):
        return self.bindClass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIUnion(CompositeCodeItem):
    # TODO: Implement CIUnion
    bindClass = 'Union'

class CIStruct(CompositeCodeItem):
    # TODO: Implement CIStruct
    bindClass = 'Structure'

class CIClass(CIStruct):
    # TODO: Implement CIClass
    bindClass = 'Structure'

    def codeDef(self):
        raise NotImplementedError("Class translations are not implemented yet")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIBase(CodeItem):
    # TODO: Implement CIBase
    pass

