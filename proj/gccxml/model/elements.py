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

import bisect

import emitters

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Elements
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RootElement(object):
    def __init__(self):
        self.files = {}

    def addDependency(self, filename):
        aFile = self.addFile(filename)
        return aFile

    def getDependencies(self):
        return self.files.iterkeys()

    def addFile(self, filename):
        aFile = self.files.get(filename, None)
        if aFile is None:
            aFile = self.createFileFor(filename)
            self.files[filename] = aFile
        return aFile

    def createFileFor(self, filename):
        return FileElement(filename)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    emitterFactoryMap = emitters.emitterFactoryMap
    def getEmitterFor(self, section, kind):
        factory = emitters.getEmitterFactoryFromMap(section, kind, 
                        self.emitterFactoryMap)
        return factory(self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FileElement(object):
    def __init__(self, filename):
        self.filename = filename
        self.lines = []

    def __len__(self):
        return len(self.lines)
    def __iter__(self):
        return iter(self.lines)

    def insertAtLine(self, line, content):
        bisect.insort(self.lines, line, content)

    def addElement(self, line, elemKind, elemArgs):
        self.insertAtLine(line, (elemKind, elemArgs))

