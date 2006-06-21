##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2006  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BlockWriter(object):
    softspace = False
    spaces = 4
    level = 0
    _indent = ""

    def __init__(self, file):
        self.file = file

    def indent(self, count=1):
        self.level += count
        self._makeIndent()

    def dedent(self, count=1):
        self.level -= count
        self._makeIndent()

    def _makeIndent(self):
        self._indent = ' '*self.level*self.spaces

    def write(self, text):
        return self.writelines(l+'\n' for l in text.split('\n'))

    def writelines(self, lines):
        indent = self._indent
        return self.file.writelines([indent + l for l in lines])

