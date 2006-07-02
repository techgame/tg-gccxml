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

import os
from bisect import insort, bisect_left, bisect_right
from ciBase import CodeItem, asCodeItem

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

fileHeader = '''\
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

%(importStmts)s

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Code generated from:
#~   "%(generatedFrom)s"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

fileFooter = '''\

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ End of code generated from:
#~   "%(generatedFrom)s"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

class CIFile(CodeItem): 
    header = fileHeader
    footer = fileFooter
    blockSeparator = '\n#~ line: %(line)s, skipped: %(lineDelta)s ~~~~~~\n'
    lineSeparator = ''

    importStmts = []

    def _initialize(self):
        # make a modifable copy of importStmts
        self.importStmts = self.importStmts[:]
        self.lines = []
        self.ciAll = set()

    def isRequired(self):
        for e in self.lines:
            if e[-1]:
                return True
        else:
            return False
    def __len__(self):
        return len(self.lines)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def clearImportStmts(self):
        self.setImportStmts([])
    def setImportStmts(self, importStmts):
        self.importStmts = list(importStmts)
    def addImportStmt(self, *importStmts):
        self.importStmts.extend(importStmts)
    def extendImportStmts(self, importStmts):
        self.importStmts.extend(importStmts)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def stmtImport(self, moduleName):
        if not isinstance(moduleName, (str, unicode)):
            moduleName = moduleName.getModuleName()
        return 'import %s' % (moduleName,)
    def stmtImportNames(self, moduleName, *names):
        if not isinstance(moduleName, (str, unicode)):
            moduleName = moduleName.getModuleName()
        return 'from %s import %s' % (moduleName, ', '.join(names))
    def stmtImportAll(self, moduleName):
        return self.stmtImportNames(moduleName, '*')

    def clearImports(self):
        self.clearImportStmts()
    def importModules(self, *moduleNames, **kw):
        if kw.pop('clear', False): self.clearImports()
        self.extendImportStmts(self.stmtImport(mod) for mod in moduleNames)
    def importAll(self, *moduleNames, **kw):
        if kw.pop('clear', False): self.clearImports()
        self.extendImportStmts(self.stmtImportAll(mod) for mod in moduleNames)
    def importNames(self, moduleName, *names, **kw):
        if kw.pop('clear', False): self.clearImports()
        self.addImportStmt(self.stmtImportNames(moduleName, *names))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @property
    def name(self): 
        return self.item.name

    _moduleName = None
    def getModuleName(self):
        if self._moduleName is None:
            result = self.getBaseFilename()
            result = os.path.basename(result)
            result = os.path.splitext(result)[0]
            return result
        else:
            return self._moduleName
    def setModuleName(self, moduleName):
        self._moduleName = moduleName
        if self._filename is None:
            self.setBaseFilename(moduleName+'.py')
    moduleName = property(getModuleName, setModuleName)

    _filename = None
    def getBaseFilename(self):
        if self._filename is None:
            result = self.name
            result = os.path.basename(result)
            result = os.path.splitext(result)[0]
            self.setBaseFilename(result + '.py')

        return self._filename
    def setBaseFilename(self, filename):
        self._filename = filename
    baseFilename = property(getBaseFilename, setBaseFilename)

    def getFilename(self):
        return self.context.getOutputFilename(self.getBaseFilename())
    filename = property(getFilename)

    def getHostCI(self):
        return asCodeItem(self.item.root)

    def add(self, ci):
        ci = asCodeItem(ci)
        if ci not in self.ciAll:
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

    def writeToFile(self):
        stream = self.context.createStream(self.getBaseFilename())
        try:
            self.writeTo(stream)
        finally:
            stream.close()

    def writeTo(self, stream):
        self.writeHeaderTo(stream)
        self.writeContentTo(stream)
        self.writeFooterTo(stream)

    def writeHeaderTo(self, stream):
        if self.header:
            print >> stream, self.header % dict(
                                    importStmts='\n'.join(self.importStmts),
                                    generatedFrom=self.item.name,
                                    )

    def writeFooterTo(self, stream):
        if self.footer:
            print >> stream, self.footer % dict(
                                    generatedFrom=self.item.name,
                                    )

    prependFiles = ()
    appendFiles = ()
    def writeContentTo(self, stream):
        for ciFile in self.prependFiles:
            ciFile.writeContentTo(stream)

        self.writeLinesTo(self.lines, stream)

        for ciFile in self.appendFiles:
            ciFile.writeContentTo(stream)

    def writeLinesTo(self, lines, stream):
        lastIdx = 0
        for idx, lineItem in lines:
            if not lineItem:
                continue
            else:
                lastIdx = self.writeSeparatorTo(stream, lastIdx, idx)
                if isinstance(lineItem, (str, unicode)):
                    # allow for literals
                    print >> stream, lineItem
                else:
                    lineItem.writeTo(stream)
        print >> stream

    def writeSeparatorTo(self, stream, lastIdx, idx):
        if not lastIdx:
            return idx

        delta = idx-lastIdx
        if self.blockSeparator and delta > 3:
            print >> stream, self.blockSeparator % dict(line=idx, lastprev=lastIdx, lineDelta=delta)
        elif delta > 1:
            print >> stream, self.lineSeparator % dict(line=idx, lastPrev=lastIdx, lineDelta=delta)

        return idx

