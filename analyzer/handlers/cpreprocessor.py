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

    def scanCompleteLine(self, emitter, line, matcher=re_preprocessor.match):
        match = matcher(line)
        if match is None: 
            return 

        directive, body = match.groups()
        self.dispatchDirective(emitter, directive, body)

    def dispatchDirective(self, emitter, directive, body):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ConditionsScanner(CPreprocessorScanner):
    conditionDirectives = set(('ifndef', 'ifdef', 'if', 'elif', 'else', 'endif'))

    def dispatchDirective(self, emitter, directive, body):
        if directive in self.conditionDirectives:
            self.onCondition(emitter, directive, body)

    def onCondition(self, emitter, directive, body):
        emitter.emit('conditional', directive, body)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IncludesScanner(CPreprocessorScanner):
    includeDirectives = set(('include', ))

    def dispatchDirective(self, emitter, directive, body):
        if directive in self.includeDirectives:
            self.onInclude(emitter, body)

    def onInclude(self, emitter, filename):
        isSystemInclude = (filename[0:1] == '<')
        filename=filename[1:-1]
        emitter.emit('include', filename, isSystemInclude)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DefinesScannerBase(CPreprocessorScanner):
    commonDefs = dict(
            REST=r'(?:\s*(.*)\s*)', 
            IDENT=r'(?:[A-Za-z_][A-Za-z0-9_]*)',
            ARGS=r'(?:\(\s*(%(IDENT)s(?:\s*,\s*%(IDENT)s)*)(?:\s*,)?\s*\)\s*)',
            )
    commonDefs['ARGS'] %= commonDefs

    def dispatchDirective(self, emitter, directive, body):
        if directive.isdigit():
            self.onFilePosition(emitter, directive, body)

    filePositionMatcher = re.compile(r'''["'](.*?)["']\s*(\d*)''' % commonDefs).match
    def onFilePosition(self, emitter, lineno, body):
        filename, flags = self.filePositionMatcher(body).groups()
        lineno = int(lineno)
        flags = int(flags or 0)
        if flags == 1:
            emitter.emit('position-push', filename, lineno, flags)
        elif flags == 2:
            emitter.emit('position-pop', filename, lineno, flags)
        else:
            emitter.emit('position-load', filename, lineno, flags)
        emitter.emit('position', filename, lineno, flags)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DefinesScanner(DefinesScannerBase):
    def dispatchDirective(self, emitter, directive, body):
        if directive.isdigit():
            self.onFilePosition(emitter, directive, body)
        elif directive == "define":
            self.onDefine(emitter, directive, body)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    commonDefs = DefinesScannerBase.commonDefs

    identMatcher = re.compile(r'(%(IDENT)s)%(REST)s' % commonDefs).match
    macroMatcher = re.compile(r'%(ARGS)s%(REST)s' % commonDefs).match
    def onDefine(self, emitter, directive, body):
        ident, body = self.identMatcher(body).groups()

        marcoPart = self.macroMatcher(body)
        if marcoPart is None:
            emitter.emit('define', ident, body)
        else:
            args, body = marcoPart.groups()
            args = tuple(a.strip() for a in args.split(','))
            emitter.emit('macro', ident, args, body)

