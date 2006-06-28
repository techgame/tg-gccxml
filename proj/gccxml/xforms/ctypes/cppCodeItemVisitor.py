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

from cCodeItemVisitor import CCodeItemVisitor
from ciCPlusPlus import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ C++ Code Generation
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CPPCodeItemVisitor(CCodeItemVisitor):
    # complex types and pointers
    CIReferenceTypeFactory = CIReferenceType
    def onReferenceType(self, atom):
        # technically this is C++, but it tends to sneak in to C code
        return self.CIReferenceTypeFactory(self.context, atom)

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

CPPCodeItemVisitor.validateFactories()

