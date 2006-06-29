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

    @classmethod
    def wrap(klass, file):
        if isinstance(file, klass):
            return file
        else: 
            return klass(file)

    def indent(self, count=1):
        self.level += count
        self._makeIndent()

    def dedent(self, count=1):
        self.level -= count
        self._makeIndent()
        #self.indentNext = False

    def _makeIndent(self):
        assert self.level >= 0, self.level
        self._indent = ' '*self.level*self.spaces

    indentNext = False
    def write(self, text):
        if self.indentNext:
            self.file.write(self._indent)

        self.indentNext = text.endswith('\n')
        text = text[:-1].replace('\n', '\n'+self._indent) + text[-1]
        return self.file.write(text)

    def close(self):
        self.file.close()
