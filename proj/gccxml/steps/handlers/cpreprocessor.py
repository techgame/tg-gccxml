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

from lineScanners import LineScannerWithContinuations

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CPreprocessorScanner(LineScannerWithContinuations):
    re_preprocessor = re.compile(r'^\s*#\s*(\w+)\s*(.*)\s*')

    def scanCompleteLine(self, handler, line, matcher=re_preprocessor.match):
        match = matcher(line)
        if match is None: 
            return 

        directive, body = match.groups()
        self.dispatchDirective(handler, directive, body)

    def dispatchDirective(self, handler, directive, body):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ConditionsScanner(CPreprocessorScanner):
    conditionDirectives = set(('ifndef', 'ifdef', 'if', 'elif', 'else', 'endif'))

    def dispatchDirective(self, handler, directive, body):
        if directive in self.conditionDirectives:
            self.onCondition(handler, directive, body)

    def onCondition(self, handler, directive, body):
        handler.emit('preprocessor', directive, body)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DefinesScanner(CPreprocessorScanner):
    def dispatchDirective(self, handler, directive, body):
        if directive.isdigit():
            self.onFilePosition(handler, directive, body)
        elif directive == "define":
            self.onDefine(handler, directive, body)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    commonDefs = dict(
            REST=r'(?:\s*(.*)\s*)', 
            IDENT=r'(?:[A-Za-z_][A-Za-z0-9_]*)',
            ARGS=r'(?:\(\s*(%(IDENT)s(?:\s*,\s*%(IDENT)s)*)(?:\s*,)?\s*\)\s*)',
            )
    commonDefs['ARGS'] %= commonDefs

    filePositionMatcher = re.compile(r'''(["'])(.*?)\1\s*(\d*)''' % commonDefs).match
    def onFilePosition(self, handler, lineno, body):
        _, filename, flags = self.filePositionMatcher(body).groups()
        lineno = int(lineno)
        flags = int(flags or 0)
        handler.emit('preprocessor', 'position', filename, lineno, flags)

    identMatcher = re.compile(r'(%(IDENT)s)%(REST)s' % commonDefs).match
    macroMatcher = re.compile(r'%(ARGS)s%(REST)s' % commonDefs).match
    def onDefine(self, handler, directive, body):
        ident, body = self.identMatcher(body).groups()

        marcoPart = self.macroMatcher(body)
        if marcoPart is None:
            handler.emit('preprocessor', 'define', ident, body)
        else:
            args, body = marcoPart.groups()
            args = tuple(a.strip() for a in args.split(','))
            handler.emit('preprocessor', 'macro', ident, args, body)

