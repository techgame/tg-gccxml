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

from lineScanners import LineScannerWithContinuations

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MakefileRuleScanner(LineScannerWithContinuations):
    _baseline = frozenset()
    def getBaseline(self):
        return self._baseline
    def setBaseline(self, baseline):
        self._baseline = frozenset(baseline)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def scanCompleteLine(self, handler, line):
        target, line = line.split(':', 1)
        files = [x.replace('\\$', ' ') for x in line.replace('\\ ', '\\$').split()]
        srcfile, files = files[0], files[1:]

        if handler is None:
            # no handler -- create the baseline
            self.setBaseline(files)
            return

        files = [f for f in files if f not in self.getBaseline()]
        handler.emit('preprocessor', 'includes', srcfile, files)

