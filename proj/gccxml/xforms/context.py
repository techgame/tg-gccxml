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

import sys
from bisect import insort, bisect_left, bisect_right

from blockWriter import BlockWriter

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CodeContext(object):
    def __init__(self):
        self._seen = set()
        self._out = dict()

    def printAll(self):
        self.writeTo(sys.stdout)

    def writeToFiles(self):
        for f, o in self._out.iteritems():
            fn = f.name+'.py'
            stream = open(fn, 'wb')
            o.writeTo(stream)

    def writeTo(self, stream):
        for f, o in self._out.iteritems():
            o.writeTo(stream)

    def fileFor(self, ci):
        result = self._out.get(ci.file, None)
        if result is None:
            result = CodeOutput(ci.file)
            self._out[ci.file] = result
        return result

    def addCodeItem(self, ci):
        if ci not in self._seen:
            self._seen.add(ci)
            self.fileFor(ci).addCodeItem(ci)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CodeOutput(object):
    def __init__(self, fileAtom):
        self.fileAtom = fileAtom
        self.lines = []

    def writeTo(self, stream):
        stream = BlockWriter.wrap(stream)

        self.writeHeaderTo(stream)
        self.writeContentTo(stream)

    def writeHeaderTo(self, stream):
        print >> stream, '# Generated from "%s"' % (self.fileAtom.name,)
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

    def addCodeItem(self, ci):
        insort(self.lines, (ci.line, ci))

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

