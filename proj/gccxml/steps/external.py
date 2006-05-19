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

import subprocess

from base import ProcessStep

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExternalProcessStep(ProcessStep):
    PIPE = subprocess.PIPE
    STDOUT = subprocess.STDOUT

    # standard in/out/err file descriptors
    stdin_fd = None # PIPE
    stdout_fd = None # PIPE
    stderr_fd = None # PIPE

    def _subprocess(self, cmd, **kw):
        subProc = subprocess.Popen(cmd, shell=True, stdin=self.stdin_fd, stdout=self.stdout_fd, stderr=self.stderr_fd, **kw)
        return subProc

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GCCXMLProcessStep(ExternalProcessStep):
    # an example command
    command = r"gccxml <options> %(srcfile)s %(includes)s > '%(outfile)s'"
    command = None

    def getCmdLine(self, srcfile, outfile=None):
        kwargs = dict(srcfile=srcfile, includes=self._getIncludeList())
        if outfile:
            kwargs.update(outfile=outfile)
        return self.command % kwargs

    def _processSrcFile(self, srcfile, outfile=None, **kw):
        outfile = self._getOutFile(outfile)
        cmdline = self.getCmdLine(srcfile, outfile)
        process = self._subprocess(cmdline, **kw)
        if outfile:
            process.wait()
            process.outfile = open(outfile, 'rb')
        else:
            process.outfile = process.stdout
        return process

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _getIncludeList(self):
        return ' '.join('-I ' + d for d in self._getIncludeDirs())
    def _getIncludeDirs(self):
        return self.config.inc
    def _getSourceFiles(self):
        return self.config.src
    def _getBaselineFiles(self):
        return self.config.baseline
    def _getOutFile(self, outfile):
        return self.config.getOutFile(outfile)

