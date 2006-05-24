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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Elements
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RootElement(object):
    def __init__(self):
        self.files = {}

    def addFile(self, filename):
        if filename not in self.files:
            self.files[filename] = self.createFileFor(filename)

    def createFileFor(self, filename):
        return FileElement(filename)

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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Handlers 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BaseHandler(object):
    rootElement = None
    def __init__(self, rootElement):
        self.rootElement = rootElement

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FileLineBaseHandler(BaseHandler):
    fileElement = None
    filename, lineno = "", 0

    def setFileAndLine(self, filename, lineno=1):
        self.filename = filename
        self.lineno = int(lineno)
        self.fileElement = self.rootElement.files.get(filename, None)

    def incLineno(self, delta=1):
        self.lineno += 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addElement(self, kind, data):
        self.fileElement.addElement(self.lineno, kind, data)

