##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2005  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import re

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DefineParserBase(object):
    re_filePosition = re.compile(r'''#\s*(\d+)\s*(["'])(.*?)\2''')
    re_s_ident = '[A-Za-z_][A-Za-z0-9_]*'
    re_define = re.compile(
            (r'#\s*define\s+(%(ident)s)\s*' % dict(ident=re_s_ident)) + 
            (r'\s*(.*)'))
    re_macro = re.compile(
            (r'#\s*define\s+(%(ident)s)\s*\(\s*' % dict(ident=re_s_ident)) + 
            (r'((?:%(ident)s\s*)(?:,\s*%(ident)s\s*)*)' % dict(ident=re_s_ident)) + 
            (r'\s*\)\s*(.*)'))
    exprMatchList = []

    def parse(self, dumpFile):
        if isinstance(dumpFile, (str, unicode)):
            dumpFile = open(dumpFile, 'rU')

        self.onStart()
        for line in dumpFile:
            self.onPreParseLine(line)
            self.parseLine(line)
            self.onPostParseLine(line)
        self.onEnd()

    def parseLine(self, line):
        for re_expr, onMatch in self.exprMatchList:
            match = re_expr.match(line)
            if match is not None:
                onMatch(self, line, match)
                break

    def matchFilePosition(self, line, match):
        lineno, _, filename = match.groups()
        self.onPosition(filename, lineno)
    exprMatchList.append((re_filePosition, matchFilePosition))

    def matchMacro(self, line, match):
        name, params, definition = match.groups()
        self.onMacro(name, params, definition)
    exprMatchList.append((re_macro, matchMacro))

    def matchDefine(self, line, match):
        name, definition = match.groups()
        self.onDefine(name, definition)
    exprMatchList.append((re_define, matchDefine))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def onStart(self):
        pass

    def onEnd(self):
        pass

    def onPreParseLine(self, line):
        pass
    def onPostParseLine(self, line):
        pass

    def onPosition(self, filename, lineno):
        print 'file:', filename, lineno

    def onDefine(self, name, definition):
        print 'define:', name, definition

    def onMacro(self, name, params, definition):
        print 'macro:', name, params, definition

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DefineParser(DefineParserBase):
    def onStart(self):
        self.fileno = None
        self.lineno = 0
        self.filemap = {}

    def onEnd(self):
        pass

    def onPostParseLine(self, line):
        self.lineno += 1 

    def onPosition(self, filename, lineno):
        fileno = self.filemap.get(filename, None)
        if fileno is None:
            fileno = 'fd%d' % len(self.filemap)
            self.filemap[filename] = fileno
            self.onFile(fileno, filename)
        self.fileno = fileno
        self.lineno = int(lineno) - 1

    def onFile(self, id, name):
        attrs = dict(id=id, name=name)
        self.xmlHandler.startElement('File', attrs)
        self.xmlHandler.endElement('File')

    def onDefine(self, name, definition):
        attrs = dict(name=name, body=definition, file=self.fileno, line=self.lineno)
        self.xmlHandler.startElement('Define', attrs)
        self.xmlHandler.endElement('Define')

    def onMacro(self, name, params, definition):
        attrs = dict(name=name, params=params, body=definition, file=self.fileno, line=self.lineno)
        self.xmlHandler.startElement('Macro', attrs)
        self.xmlHandler.endElement('Macro')

    _xmlHandler = None
    def getXmlHandler(self):
        return self._xmlHandler
    def setXmlHandler(self, xmlHandler):
        self._xmlHandler = xmlHandler
    def delXmlHandler(self):
        self._xmlHandler = None
    xmlHandler = property(getXmlHandler, setXmlHandler, delXmlHandler)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def parse(defineFile):
    return GCCDefineParser().parse(defineFile)

