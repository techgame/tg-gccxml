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

import re

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LineScannerBase(object):
    def __call__(self, handler, fileToScan):
        return self.scanFile(handler, fileToScan)
    def scanFile(self, handler, fileToScan):
        scanLine = self.scanLine
        matchCommands = self.getMatchCommands()
        assert matchCommands, "Scanning without any rules to scan for"

        incLineno = handler.incLineno
        for line in fileToScan:
            r = scanLine(handler, line, matchCommands)
            incLineno()

    def scanLine(self, handler, line, matchCommands):
        for matchCmd in matchCommands:
            line = matchCmd(self, handler, line)
            if not line:
                return True
        else:
            return False

    matchCommands = []
    def getMatchCommands(self):
        return self.matchCommands

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def addMatchCmd(lst):
    def _addToList(fn):
        lst.append(fn)
        return fn
    return _addToList

class CPreprocessorLineScannerBase(LineScannerBase):
    matchCommands = LineScannerBase.matchCommands[:]

    re_prefix = re.compile(r'^\s*#\s*')

    @addMatchCmd(matchCommands)
    def matchPrefix(self, handler, line, matcher=re_prefix.match):
        match = matcher(line)
        if match is not None:
            # Continue matching after current match for this line
            return line[match.end():]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PreprocessorDefinesScanner(CPreprocessorLineScannerBase):
    matchCommands = CPreprocessorLineScannerBase.matchCommands[:]

    commonDefs = dict(
            REST=r'(?:\s*(.*)\s*)', 
            IDENT=r'(?:[A-Za-z_][A-Za-z0-9_]*)',
            ARGS=r'(?:\s*\(\s*(%(IDENT)s(?:\s*,\s*%(IDENT)s)(?:\s*,)?)\s*\)\s*)',
            )
    commonDefs['ARGS'] %= commonDefs

    re_filePosition = re.compile(r'''(\d+)\s*(["'])(.*?)\2(\d*)''' % commonDefs)
    re_define = re.compile(r'define\s+(%(IDENT)s)%(REST)s' % commonDefs)
    re_macro_part = re.compile(r'%(ARGS)s%(REST)s' % commonDefs)

    @addMatchCmd(matchCommands)
    def matchFilePosition(self, handler, line, matcher=re_filePosition.match, ):
        match = matcher(line)
        if match is None: 
            # Continue matching from this line on other rules
            return line 

        lineno, _, filename, flags = match.groups()
        handler.emit('position', (filename, int(lineno), int(flags or 0)))

    @addMatchCmd(matchCommands)
    def matchDefine(self, handler, line, matcher=re_define.match, macroMatcher=re_macro_part.match):
        match = matcher(line)
        if match is None:
            # Continue matching from this line on other rules
            return line 

        name, body = match.groups()
        marcoPart = macroMatcher(body)
        if marcoPart is None:
            handler.emit('define', (name, body))
        else:
            args, body = marcoPart.groups()
            args = tuple(a.strip() for a in args.split(','))
            handler.emit('macro', (name, args, body))

