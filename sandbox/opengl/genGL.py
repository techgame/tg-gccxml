#!/usr/bin/env python
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

import cPickle
from TG.gccxml.model import atoms

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AtomFilter(atoms.ModelAtomVisitor):
    def __init__(self):
        self.functions = list()
        self.defines = list()
        self.types = set()
        self.conditions = set()

    def onFunction(self, item):
        if not item.extern: 
            return

        self.functions.append(item)
        self._addCallableTypeRefs(item)

    def _addCallableTypeRefs(self, item):
        for a in item.arguments:
            self._addType(a.type) 
        self._addType(item.returns) 

    def _addType(self, aType):
        if aType is None:
            return

        assert aType.isType(), aType
        self.types.add(aType)
        if aType.isCallable():
            self._addCallableTypeRefs(aType)

        elif aType.isCompositeType():
            for m in aType.members:
                self._addType(m.type)

        elif not aType.isBasicType():
            self._addType(aType.type)

    def onPPDefine(self, item):
        if not item.ident.startswith('GL'):
            return
        self.defines.append(item)

    def onPPConditional(self, item):
        if not item.body.startswith('GL'):
            return
        if item.body in ('GL_GLEXT_PROTOTYPES', 'GLAPI', 'GL_TYPEDEFS_2_0', 'GL_GLEXT_LEGACY', 'GL_GLEXT_FUNCTION_POINTERS'):
            return
        self.conditions.add(item)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Code generation
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def codeItemFor(item):
    if item is not None:
        codeItem = getattr(item, 'codeItem', None)
        if codeItem is None:
            factory = CodeItem.typeMap[type(item)]
            codeItem = factory(item)
        return codeItem
    else: return None

def referenceFor(item):
    codeItem = codeItemFor(item)
    if codeItem is not None:
        return codeItem.reference()
    else: return ''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CodeItem(object):
    def __init__(self, item):
        self.item = item
        item.codeItem = self

    def reference(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def definition(self):
        return ''

    referenceFor = staticmethod(referenceFor)

    typeMap = {}
    @classmethod
    def register(klass, typeList):
        for type in typeList:
            CodeItem.typeMap[type] = klass

class FundamentalTypeCodeItem(CodeItem):
    def reference(self):
        return self.item.name
    def definition(self):
        return self.item.name
FundamentalTypeCodeItem.register([atoms.FundamentalType])

class DecoratedCodeItem(CodeItem):
    def reference(self):
        return self.referenceFor(self.item.type)
    def definition(self):
        return ''
DecoratedCodeItem.register([atoms.CvQualifiedType])

class ArgumentCodeItem(CodeItem):
    def reference(self):
        return self.referenceFor(self.item.type)
    def definition(self):
        return ''
ArgumentCodeItem.register([atoms.Argument])

class PointerCodeItem(CodeItem):
    def reference(self):
        itemType = self.item.type
        ref = self.referenceFor(itemType)
        if hasattr(itemType, 'name'):
            return ref + '.ptr'
        else:
            return 'POINTER(%s)' % (ref,)
    def definition(self):
        ref = self.referenceFor(self.item.type)
        return '%s.ptr = POINTER(%s)\n' % (ref, ref)
PointerCodeItem.register([atoms.PointerType])

class TypedefCodeItem(CodeItem):
    def reference(self):
        return self.item.name
    def definition(self):
        item = self.item
        if item.type.isFundamentalType():
            return 'class %(name)s(%(typeName)): pass' % dict(name=item.name, typeName=item.type.name)
TypedefCodeItem.register([atoms.Typedef])

class StructCodeItem(CodeItem):
    def reference(self):
        return self.item.name
    def definition(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
StructCodeItem.register([atoms.Struct, atoms.Class])

class CallableCodeItem(CodeItem):
    def argumentReferences(self, arguments=None):
        arguments = arguments or self.item.arguments
        result = [self.referenceFor(a) for a in arguments]
        return result
    def argumentNames(self, arguments=None, argTempalte='arg_%d'):
        arguments = arguments or self.item.arguments
        result = [(a.name or argTempalte % i) for i, a in enumerate(arguments)]
        return result

class FunctionTypeCodeItem(CallableCodeItem):
    def reference(self):
        return self.definition()
    def definition(self):
        item = self.item
        return 'CFUNCTYPE(%s, [%s])' % (
                    self.referenceFor(item.returns), 
                    ', '.join(self.argumentReferences(item.arguments)),
                    )
FunctionTypeCodeItem.register([atoms.FunctionType])

class FunctionCodeItem(CallableCodeItem):
    template = (
        '@glCall(%(returnType)s, [%(paramTypes)s])\n'
        'def %(funcName)s(%(paramNames)s): pass\n'
        )

    def reference(self):
        return self.item.name

    def definition(self):
        item = self.item
        kw = dict(
            funcName=item.name,
            returnType=self.referenceFor(item.returns),
            paramTypes=', '.join(self.argumentReferences(item.arguments)),
            paramNames=', '.join(self.argumentNames(item.arguments)),
            )

        return self.template % kw
FunctionCodeItem.register([atoms.Function])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    root = cPickle.load(file('gen.pickle', 'rb'))

    atomFilter = AtomFilter()
    atomFilter.visit(root)

    for atom in atomFilter.functions:
        ci = codeItemFor(atom)

        if 'Callback' in atom.name:
            print ci.definition()

