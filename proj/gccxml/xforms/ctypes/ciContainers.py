
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

from bisect import insort, bisect_left, bisect_right

from ciBase import CodeItem

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIRoot(CodeItem): 
    def _initialize(self):
        self.files = []

    def add(self, ciFile):
        ciFile = CodeItem.asCodeItem(ciFile)
        self.files.append(ciFile)

    def getHostCI(self):
        return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CIFile(CodeItem): 
    def _initialize(self):
        self.lines = []
        self.ciAll = set()

    @property
    def name(self): return self.item.name

    def getHostCI(self):
        return self.item.root.codeItem

    def add(self, ci):
        ci = CodeItem.asCodeItem(ci)
        if ci not in self.ciAll:
            assert ci.file is self.item
            insort(self.lines, (ci.line, ci))
            self.ciAll.add(ci)

    def getItemsBetween(self, fromCI, toCI=None):
        return (l[-1] for l in self.getLinesBetween(fromCI, toCI))
    def getLinesBetween(self, fromCI, toCI=None):
        if fromCI is not None:
            idx0 = bisect_right(self.lines, (fromCI.line, fromCI))
        else: idx0 = None

        if toCI is not None:
            idx1 = bisect_left(self.lines, (toCI.line, toCI))
        else: idx1 = None

        return self.lines[idx0:idx1]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def writeTo(self, stream):
        self.writeHeaderTo(stream)
        self.writeContentTo(stream)

    def writeHeaderTo(self, stream):
        print >> stream, '# Generated from "%s"' % (self.item.name,)
        print >> stream

    def writeContentTo(self, stream):
        lastIdx = 0
        for idx, l in self.lines:
            if not lastIdx:
                pass
            elif idx-lastIdx > 3:
                print >> stream
                print >> stream, '#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                print >> stream
            elif idx-lastIdx > 1:
                print >> stream
            lastIdx = idx

            l.writeTo(stream)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CINamespace(CodeItem): 
    pass

