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
import sys
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

class GCCXMLException(Exception):
    pass

class GCCXMLProcessStep(ExternalProcessStep):
    # an example command
    command = r"gccxml <options> %(srcfile)s %(includes)s > '%(outfile)s'"
    command = None
    allowFrameworkInclude = False

    def getCmdLine(self, srcfile, outfile=None):
        kwargs = dict(srcfile=srcfile, includes=self._getIncludeList())
        if outfile:
            kwargs.update(outfile=outfile)
        return self.command % kwargs

    def _processSrcFile(self, srcfile, outfile=None, **kw):
        outfile = self._getOutFile(outfile)
        if os.path.exists(outfile):
            print 'Using existing:', outfile
            return None, open(outfile, 'rb')

        cmdline = self.getCmdLine(srcfile, outfile)
        ##print cmdline
        process = self._subprocess(cmdline, **kw)
        if outfile:
            retcode = process.wait()
            if retcode != 0:
                # unsuccessful compile, proceed
                raise GCCXMLException("GCCXML subprocess returned failure code: %d (%08x)\ncmd: %r" % (retcode, retcode, cmdline))
            process.outfile = open(outfile, 'rb')
        else:
            process.outfile = process.stdout
        return process, process.outfile

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _getIncludeList(self):
        result = []
        result.extend('-I ' + d for d in self._getIncludeDirs())
        if self.allowFrameworkInclude:
            result.extend('-framework ' + f for f in self._getFrameworkDirs())
        return ' '.join(result)
    def _getIncludeDirs(self):
        return self.config.inc
    def _getFrameworkDirs(self):
        if sys.platform == 'darwin':
            return self.config.frameworks
        else: return []
    def _getSourceFiles(self):
        return self.config.src
    def _getBaselineFiles(self):
        return self.config.baseline
    def _getOutFile(self, outfile):
        return self.config.getOutFile(outfile)

