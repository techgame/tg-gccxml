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
    def printAll(self):
        self.writeTo(sys.stdout)

    def writeToFiles(self):
        for ciFile in self.ciRoot.files:
            fn = ciFile.name.replace('.', '_') +'.py'
            stream = open(fn, 'wb')
            try:
                ciFile.writeTo(BlockWriter(stream))
            finally:
                stream.close()

    def writeTo(self, stream):
        stream = BlockWriter.wrap(stream)

        for ciFile in self.ciRoot.files:
            ciFile.writeTo(stream)

