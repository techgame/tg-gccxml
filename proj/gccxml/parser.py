##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2005  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

"""
This module is inspired by Thomas Heller's gccxml work.  

His code works wonderfully.  It is inteded to transform from header to python
code so that you can start modifying the code from there.  This is great if the
generic wrapper choices he has made in the conversion code work for your
library (and style).  However, I desire the output code to look more like my
style, and allow for the wrapper developer to be able to put the "flavor" of
the wrapped library into the python module(s).  

So this work will take much of what Heller learned in ctypes.wrapper and apply
it to a Techgame-ish OO style.


Constraints:
    Python 2.4 or greater
    ctypes 0.9.9.3 or greater

gccxml options:
    -I gives include directories
    -M tells gcc to create a make-compatable include file.  implies -E
    -E tells gcc to stop after the preprocessing stage
    -dD dumps all macro definitions
    -fxml gives the filename to dump the output to

preprocesses the source for includes:
    gccxml -M -dD gen.cpp -I . 

preprocess the source -- great for includes and #defines:
    gccxml -E -dD gen.cpp -I . 

compiles source into xml:
    gccxml gen.cpp -I . -fxml='shane.xml'    
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from gccxmlParser import GCC_XML, GCCXMLHandler, ElementVisitor
from gccxmlDefines import GCCDefineHandler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GCCXMLDoc(GCCXMLHandler):
    def parse(self, xmlFile, defineFile):
        self.defineFile = defineFile
        try:
            result = GCCXMLHandler.parse(self, xmlFile)
        finally:
            del self.defineFile
        return result

    def startRoot(self):
        self.root.setBuilder(self.getBuilder())
        self.parseDefineFile()

    def endRoot(self):
        self.root.delBuilder()

    def parseDefineFile(self):
        defineHandler = GCCDefineHandler()
        defineHandler.xmlHandler = self
        try:
            defineHandler.parse(self.defineFile)
        finally:
            del defineHandler.xmlHandler

    _builder = None
    def getBuilder(self):
        return self._builder
    def setBuilder(self, builder):
        self._builder = builder
    def delBuilder(self):
        self._builder = None
    builder = property(getBuilder, setBuilder, delBuilder)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GCCXMLBuilder(ElementVisitor):
    GCCXMLDocFactory = GCCXMLDoc

    def parse(self, xmlFile, defineFile):
        doc = self.GCCXMLDocFactory()
        doc.setBuilder(self)
        try:
            self.onPreParse()
            doc.parse(xmlFile, defineFile)
            self.onPostParse()
        finally:
            doc.delBuilder()

    def addElement(self, elem):
        if self.onElementGeneric(elem):
            elem.visitAll(self)

    def onPreParse(self):
        pass

    def onPostParse(self):
        pass

    def onElementGeneric(self, item):
        return True

