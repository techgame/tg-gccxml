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

#from ciBase import *
from ciRoot import CIRoot
from ciFile import CIFile

from ciTypes import CIFundamentalType, CICvQualifiedType
from ciTypes import CIPointerType, CIReferenceType, CIArrayType
from ciTypes import CITypedef
from ciTypes import CIEnumeration, CIEnumValue

from ciCallables import CIArgument, CIEllipsis, CIFunction, CIFunctionType

from ciComposites import CIVariable, CIField, CIStruct, CIUnion

from ciPreprocessor import CIPPInclude, CIPPConditional, CIPPDefine, CIPPMacro

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
        invalidFactories = [n for n,v in vars(klass).items() if v is None and n.startswith('CI')]

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
    CIRoot = CIRoot
    def onRoot(self, atom):
        result = self.CIRoot(self.context, atom)
        for f in atom.files.itervalues():
            self._visit(f)
        return result

    # file references
    CIFile = CIFile
    def onFile(self, atom):
        return self.CIFile(self.context, atom)

BaseCodeGenVisitor.validateFactories()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ C Code Generation
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CCodeGenVisitor(BaseCodeGenVisitor):
    # simple types
    CIFundamentalType = CIFundamentalType
    def onFundamentalType(self, atom):
        return self.CIFundamentalType(self.context, atom)

    CICvQualifiedType = CICvQualifiedType
    def onCvQualifiedType(self, atom):
        return self.CICvQualifiedType(self.context, atom)

    CIEnumeration = CIEnumeration
    def onEnumeration(self, atom):
        return self.CIEnumeration(self.context, atom)

    CIEnumValue = CIEnumValue
    def onEnumValue(self, atom):
        return self.CIEnumValue(self.context, atom)


    # complex types and pointers
    CITypedef = CITypedef
    def onTypedef(self, atom):
        return self.CITypedef(self.context, atom)

    CIPointerType = CIPointerType
    def onPointerType(self, atom):
        return self.CIPointerType(self.context, atom)

    CIReferenceType = CIReferenceType
    def onReferenceType(self, atom):
        # technically this is C++, but it tends to sneak in to C code
        return self.CIReferenceType(self.context, atom)

    CIArrayType = CIArrayType
    def onArrayType(self, atom):
        return self.CIArrayType(self.context, atom)


    # composite elements
    CIUnion = CIUnion
    def onUnion(self, atom):
        return self.CIUnion(self.context, atom)

    CIStruct = CIStruct
    def onStruct(self, atom):
        return self.CIStruct(self.context, atom)


    # context members
    CIVariable = CIVariable
    def onVariable(self, atom):
        return self.CIVariable(self.context, atom)

    CIField = CIField
    def onField(self, atom):
        return self.CIField(self.context, atom)


    # sub elements of Callables
    CIArgument = CIArgument
    def onArgument(self, atom):
        return self.CIArgument(self.context, atom)

    CIEllipsis = CIEllipsis
    def onEllipsis(self, atom):
        return self.CIEllipsis(self.context, atom)


    # callables
    CIFunction = CIFunction
    def onFunction(self, atom):
        return self.CIFunction(self.context, atom)

    CIFunctionType = CIFunctionType
    def onFunctionType(self, atom):
        return self.CIFunctionType(self.context, atom)


    # preprocessor
    CIPPInclude = CIPPInclude
    def onPPInclude(self, atom):
        return self.CIPPInclude(self.context, atom)

    CIPPConditional = CIPPConditional
    def onPPConditional(self, atom):
        return self.CIPPConditional(self.context, atom)

    CIPPDefine = CIPPDefine
    def onPPDefine(self, atom):
        return self.CIPPDefine(self.context, atom)

    CIPPMacro = CIPPMacro
    def onPPMacro(self, atom):
        return self.CIPPMacro(self.context, atom)

CCodeGenVisitor.validateFactories()

