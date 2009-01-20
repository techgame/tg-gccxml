#!/usr/bin/env python
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
from cpreprocessor import DefinesScannerBase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FuncTypedefScanner(DefinesScannerBase):
    re_funcTypedef = re.compile(
            r'typedef\s*'
            r'\w[^\n\(]+'
            r'\(\s*\*\s*(\w+)\)\s*'
            r'\(([^\)]*)\)[^;]*;'
            , re.MULTILINE)

    re_argName = re.compile(
            r'^\s*\w+.*\b(\w+)\s*$'
            )

    def _getArgName(self, argumentAndType, matcher=re_argName.match):
        m = matcher(argumentAndType)
        return m and m.groups(1)[0] or ''

    def scanCompleteLine(self, emitter, line, matcher=re_funcTypedef.match):
        match = matcher(line)
        if match is None: 
            return DefinesScannerBase.scanCompleteLine(self, emitter, line)

        typeName, args = match.groups()
        args = args.split(',')
        argNames = [self._getArgName(a) for a in args]

        if max(argNames):
            emitter.emit('function-type-name', typeName, argNames)

