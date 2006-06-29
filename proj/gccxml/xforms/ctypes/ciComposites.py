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
    @property
    def name(self):
        return self.item.name

    # TODO: Implement CIVariable

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIField(CodeItem):
    tempalte = '("%(fieldName)s", %(fieldTypeRef)s),'
    @property
    def name(self):
        return self.item.name

    def writeTo(self, stream):
        print >> stream, self.tempalte % dict(
                fieldName=self.name, 
                fieldTypeRef=self.typeRefFor(self.item.type))

    def getHostCI(self):
        return self.item.context.codeItem

    def typeRef(self, require=True):
        if require: self.require()
        return self.typeRefFor(self.item.type)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Composites
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CompositeCodeItem(CodeItem):
    _required = True
    template = 'class %(name)s(%(bindClass)s):'
    pointerTemplate = 'POINTER(%(name)s)'
    forwardPtrTemplate = '%(ptrTypedefName)s.set_type(%(name)s)'

    fieldOpenTemplate = '_fields_ = ['
    fieldCloseTemplate = '    ]'
    fieldEmptyTemplate = '_fields_ = []'

    bindClass = None #'Structure' or 'Union'
    forwardPtrs = ()

    def typeRef(self, require=True):
        if require: self.require()
        return self.name

    def ptrTypeRefFrom(self, ciPtrType):
        if ciPtrType.isForwardType:
            name = '"' + self.name + '"'

            if not self.forwardPtrs:
                self.forwardPtrs = []
            self.forwardPtrs.append(ciPtrType)
        else: 
            name = self.name

        return self.pointerTemplate % dict(name=name,)

    @property
    def name(self): 
        return self.item.name

    def writeTo(self, stream):
        self.writeDeclTo(stream)
        stream.indent()
        self.writeFieldsTo(stream)
        stream.dedent()
        self.writePointerDefTo(stream)

    def writeDeclTo(self, stream):
        print >> stream, self.compositeDecl()

    def writeFieldsTo(self, stream):
        fieldList = list(self.item.iterFields())
        if not fieldList:
            print >> stream, self.fieldEmptyTemplate

        else:
            print >> stream, self.fieldOpenTemplate
            stream.indent()

            for field in fieldList:
                field.codeItem.writeTo(stream)

            stream.dedent()
            print >> stream, self.fieldCloseTemplate

    def writePointerDefTo(self, stream):
        for fwdPtr in self.forwardPtrs:
            if fwdPtr.ciTypedef is not None:
                ptrTypedefName = fwdPtr.ciTypedef.typeRef()
                print >> stream, self.forwardPtrTemplate % dict(
                                            ptrTypedefName=ptrTypedefName, 
                                            name=self.typeRef())
            else:
                assert False, fwdPtr

    def add(self, ciField):
        pass

    def compositeDecl(self):
        return self.template % dict(
                name=self.typeRef(),
                bindClass=self.bindClass)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIUnion(CompositeCodeItem):
    bindClass = 'Union'

class CIStruct(CompositeCodeItem):
    bindClass = 'Structure'

