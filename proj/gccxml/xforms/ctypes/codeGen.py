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

from TG.gccxml.model import visitor

from ciBase import *
from ciContainers import *
from ciTypes import *
from ciComposites import *
from ciCallables import *
from ciPreprocessor import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Code Gen Node Visitor
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BaseCodeGenVisitor(visitor.DependencyAtomVisitor):
    context = None
    def __init__(self, context):
        self.context = context
        self.cache = dict()

    @classmethod
    def validateFactories(klass):
        invalidFactories = []
        for n, v in vars(klass).iteritems():
            if n.startswith('CI') and n.endswith('Factory'):
                if v is None:
                    invalidFactories.append(n)

        if invalidFactories:
            e = Exception("Invalid code item factories: [%s]" % (', '.join(invalidFactories),))
            e.invalidFactories = invalidFactories
            raise e
        else:
            return True

    def _visitAtom(self, atom):
        ci = self.cache.get(atom, None)
        if ci is None:
            ci = atom.visit(self)
            atom.visitDependencies(self)
            self.cache[atom] = ci
        return ci

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # root reference
    CIRootFactory = CIRoot
    def onRoot(self, atom):
        result = self.CIRootFactory(self.context, atom)
        for f in atom.files.itervalues():
            self._visit(f)
        return result

    # file references
    CIFileFactory = CIFile
    def onFile(self, atom):
        return self.CIFileFactory(self.context, atom)

BaseCodeGenVisitor.validateFactories()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ C Code Generation
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CCodeGenVisitor(BaseCodeGenVisitor):
    # simple types
    CIFundamentalTypeFactory = CIFundamentalType
    def onFundamentalType(self, atom):
        return self.CIFundamentalTypeFactory(self.context, atom)

    CICvQualifiedTypeFactory = CICvQualifiedType
    def onCvQualifiedType(self, atom):
        return self.CICvQualifiedTypeFactory(self.context, atom)

    CIEnumerationFactory = CIEnumeration
    def onEnumeration(self, atom):
        return self.CIEnumerationFactory(self.context, atom)

    CIEnumValueFactory = CIEnumValue
    def onEnumValue(self, atom):
        return self.CIEnumValueFactory(self.context, atom)


    # complex types and pointers
    CITypedefFactory = CITypedef
    def onTypedef(self, atom):
        return self.CITypedefFactory(self.context, atom)

    CIPointerTypeFactory = CIPointerType
    def onPointerType(self, atom):
        return self.CIPointerTypeFactory(self.context, atom)

    CIReferenceTypeFactory = CIReferenceType
    def onReferenceType(self, atom):
        # technically this is C++, but it tends to sneak in to C code
        return self.CIReferenceTypeFactory(self.context, atom)

    CIArrayTypeFactory = CIArrayType
    def onArrayType(self, atom):
        return self.CIArrayTypeFactory(self.context, atom)


    # composite elements
    CIUnionFactory = CIUnion
    def onUnion(self, atom):
        return self.CIUnionFactory(self.context, atom)

    CIStructFactory = CIStruct
    def onStruct(self, atom):
        return self.CIStructFactory(self.context, atom)


    # context members
    CIVariableFactory = CIVariable
    def onVariable(self, atom):
        return self.CIVariableFactory(self.context, atom)

    CIFieldFactory = CIField
    def onField(self, atom):
        return self.CIFieldFactory(self.context, atom)


    # sub elements of Callables
    CIArgumentFactory = CIArgument
    def onArgument(self, atom):
        return self.CIArgumentFactory(self.context, atom)

    CIEllipsisFactory = CIEllipsis
    def onEllipsis(self, atom):
        return self.CIEllipsisFactory(self.context, atom)


    # callables
    CIFunctionFactory = CIFunction
    def onFunction(self, atom):
        return self.CIFunctionFactory(self.context, atom)

    CIFunctionTypeFactory = CIFunctionType
    def onFunctionType(self, atom):
        return self.CIFunctionTypeFactory(self.context, atom)


    # preprocessor
    CIPPIncludeFactory = CIPPInclude
    def onPPInclude(self, atom):
        return self.CIPPIncludeFactory(self.context, atom)

    CIPPConditionalFactory = CIPPConditional
    def onPPConditional(self, atom):
        return self.CIPPConditionalFactory(self.context, atom)

    CIPPDefineFactory = CIPPDefine
    def onPPDefine(self, atom):
        return self.CIPPDefineFactory(self.context, atom)

    CIPPMacroFactory = CIPPMacro
    def onPPMacro(self, atom):
        return self.CIPPMacroFactory(self.context, atom)

CCodeGenVisitor.validateFactories()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ C++ Code Generation
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CPPCodeGenVisitor(CCodeGenVisitor):
    # namespace 
    CINamespaceFactory = CINamespace
    def onNamespace(self, atom):
        return self.CINamespaceFactory(self.context, atom)

    # composite elements
    CIClassFactory = CIClass
    def onClass(self, atom):
        return self.CIClassFactory(self.context, atom)

    CIBaseFactory = CIBase
    def onBase(self, atom):
        return self.CIBaseFactory(self.context, atom)


    # callables
    CIMethodFactory = CIMethod
    def onMethod(self, atom):
        return self.CIMethodFactory(self.context, atom)

    CIConstructorFactory = CIConstructor
    def onConstructor(self, atom):
        return self.CIConstructorFactory(self.context, atom)

    CIDestructorFactory = CIDestructor
    def onDestructor(self, atom):
        return self.CIDestructorFactory(self.context, atom)

CPPCodeGenVisitor.validateFactories()

