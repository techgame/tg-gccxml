#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from ciBase import CodeItem
from ciTypes import CIPointerType
from ciCallables import CallableCodeItem
from ciComposites import CIStruct

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ C++ Containers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CINamespace(CodeItem): 
    """TODO: Implement CINamespace"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ C++ Type Extensions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIReferenceType(CIPointerType):
    """TODO: Implement CIMethod"""
    typeRefTemplate = 'REFERENCE(%s)'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ C++ Classes and Bases
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIClass(CIStruct):
    """TODO: Implement CIClass"""
    bindClass = 'Structure'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIBase(CodeItem):
    """TODO: Implement CIBase"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ C++ Methods, Constructors, and Destructors
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MethodCodeItem(CallableCodeItem):
    """TODO: Implement MethodCodeItem"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIMethod(MethodCodeItem):
    """TODO: Implement CIMethod"""

class CIConstructor(MethodCodeItem):
    """TODO: Implement CIConstructor"""

class CIDestructor(MethodCodeItem):
    """TODO: Implement CIDestructor"""

