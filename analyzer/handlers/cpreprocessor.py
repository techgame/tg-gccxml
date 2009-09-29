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
            self.pushPosition(emitter, filename, lineno, flags)
        elif flags == 2:
            self.popPosition(emitter, filename, lineno, flags)
        else:
            self.loadPosition(emitter, filename, lineno, flags)
        self.absPosition(emitter, filename, lineno, flags)

    def pushPosition(self, emitter, filename, lineno, flags):
        emitter.emit('position-push', filename, lineno, flags)
    def popPosition(self, emitter, filename, lineno, flags):
        emitter.emit('position-pop', filename, lineno, flags)
    def loadPosition(self, emitter, filename, lineno, flags):
        emitter.emit('position-load', filename, lineno, flags)
    def absPosition(self, emitter, filename, lineno, flags):
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DependencyScannerBase(DefinesScannerBase):
    baselineMode = False

    def __init__(self): 
        self.baseline = set()
        self.all = set()
        self.tree = {}
        self.stack = [self.tree]

    def addFilename(self, filename):
        res = False
        tos = self.stack[-1]
        if filename in self.baseline or tos is None:
            return False, None

        if filename not in self.all:
            self.all.add(filename)
            res = True

        e = tos.get(filename)
        if e is None:
            tos[filename] = e = {}

        return res, e

    def pushPosition(self, emitter, filename, lineno, flags):
        res, e = self.addFilename(filename)
        self.stack.append(e)
    def popPosition(self, emitter, filename, lineno, flags):
        self.stack.pop()
        res, e = self.addFilename(filename)
    def loadPosition(self, emitter, filename, lineno, flags):
        res, e = self.addFilename(filename)
    def absPosition(self, emitter, filename, lineno, flags):
        pass

    def scanFileEnd(self, emitter):
        if self.baselineMode:
            emitKey = 'includes-baseline'
        else: emitKey = 'includes'

        def flatten(tree):
            for fn, subtree in tree.iteritems():
                yield fn
                for e in flatten(subtree):
                    yield e

        for srcFile, deps in self.tree.iteritems():
            files = list(flatten(deps))
            emitter.emit(emitKey, srcFile, files)

        if self.baselineMode:
            self.baseline = self.all
            self.all = set()
            self.tree = {}
            self.stack = [self.tree]

