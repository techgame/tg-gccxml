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

class CodeGenVisitor(visitor.AtomVisitor):
    # root reference
    CIRootFactory = CIRoot
    def onRoot(self, atom):
        if self.CIRootFactory:
            return self.CIRootFactory(atom)

    # file references
    CIFileFactory = CIFile
    def onFile(self, atom):
        if self.CIFileFactory:
            return self.CIFileFactory(atom)

    # namespace 
    CINamespaceFactory = CINamespace
    def onNamespace(self, atom):
        if self.CINamespaceFactory:
            return self.CINamespaceFactory(atom)

    # simple types
    CIFundamentalTypeFactory = CIFundamentalType
    def onFundamentalType(self, atom):
        if self.CIFundamentalTypeFactory:
            return self.CIFundamentalTypeFactory(atom)

    CICvQualifiedTypeFactory = CICvQualifiedType
    def onCvQualifiedType(self, atom):
        if self.CICvQualifiedTypeFactory:
            return self.CICvQualifiedTypeFactory(atom)

    CIEnumerationFactory = CIEnumeration
    def onEnumeration(self, atom):
        if self.CIEnumerationFactory:
            return self.CIEnumerationFactory(atom)

    CIEnumValueFactory = CIEnumValue
    def onEnumValue(self, atom):
        if self.CIEnumValueFactory:
            return self.CIEnumValueFactory(atom)


    # complex types and pointers
    CITypedefFactory = CITypedef
    def onTypedef(self, atom):
        if self.CITypedefFactory:
            return self.CITypedefFactory(atom)

    CIPointerTypeFactory = CIPointerType
    def onPointerType(self, atom):
        if self.CIPointerTypeFactory:
            return self.CIPointerTypeFactory(atom)

    CIReferenceTypeFactory = CIReferenceType
    def onReferenceType(self, atom):
        if self.CIReferenceTypeFactory:
            return self.CIReferenceTypeFactory(atom)

    CIArrayTypeFactory = CIArrayType
    def onArrayType(self, atom):
        if self.CIArrayTypeFactory:
            return self.CIArrayTypeFactory(atom)


    # composite elements
    CIUnionFactory = CIUnion
    def onUnion(self, atom):
        if self.CIUnionFactory:
            return self.CIUnionFactory(atom)

    CIStructFactory = CIStruct
    def onStruct(self, atom):
        if self.CIStructFactory:
            return self.CIStructFactory(atom)

    CIClassFactory = CIClass
    def onClass(self, atom):
        if self.CIClassFactory:
            return self.CIClassFactory(atom)

    CIBaseFactory = CIBase
    def onBase(self, atom):
        if self.CIBaseFactory:
            return self.CIBaseFactory(atom)


    # context members
    CIVariableFactory = CIVariable
    def onVariable(self, atom):
        if self.CIVariableFactory:
            return self.CIVariableFactory(atom)

    CIFieldFactory = CIField
    def onField(self, atom):
        if self.CIFieldFactory:
            return self.CIFieldFactory(atom)


    # sub elements of Callables
    CIArgumentFactory = CIArgument
    def onArgument(self, atom):
        if self.CIArgumentFactory:
            return self.CIArgumentFactory(atom)

    CIEllipsisFactory = CIEllipsis
    def onEllipsis(self, atom):
        if self.CIEllipsisFactory:
            return self.CIEllipsisFactory(atom)


    # callables
    CIFunctionFactory = CIFunction
    def onFunction(self, atom):
        if self.CIFunctionFactory:
            return self.CIFunctionFactory(atom)

    CIFunctionTypeFactory = CIFunctionType
    def onFunctionType(self, atom):
        if self.CIFunctionTypeFactory:
            return self.CIFunctionTypeFactory(atom)

    CIMethodFactory = CIMethod
    def onMethod(self, atom):
        if self.CIMethodFactory:
            return self.CIMethodFactory(atom)

    CIConstructorFactory = CIConstructor
    def onConstructor(self, atom):
        if self.CIConstructorFactory:
            return self.CIConstructorFactory(atom)

    CIDestructorFactory = CIDestructor
    def onDestructor(self, atom):
        if self.CIDestructorFactory:
            return self.CIDestructorFactory(atom)


    # preprocessor
    CIPPIncludeFactory = CIPPInclude
    def onPPInclude(self, atom):
        if self.CIPPIncludeFactory:
            return self.CIPPIncludeFactory(atom)

    CIPPConditionalFactory = CIPPConditional
    def onPPConditional(self, atom):
        if self.CIPPConditionalFactory:
            return self.CIPPConditionalFactory(atom)

    CIPPDefineFactory = CIPPDefine
    def onPPDefine(self, atom):
        if self.CIPPDefineFactory:
            return self.CIPPDefineFactory(atom)

    CIPPMacroFactory = CIPPMacro
    def onPPMacro(self, atom):
        if self.CIPPMacroFactory:
            return self.CIPPMacroFactory(atom)

