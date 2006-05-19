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

import sys
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Compiler(object):
    buildDir = 'build/gccxml/'
    compiler = 'gccxml'
    cmdCompileXML = r"%(compiler)s %(srcfile)s %(includeDirs)s -fxml='%(outfile)s'"
    cmdCompileDefines = r"%(compiler)s -E -dD %(srcfile)s %(includeDirs)s > '%(outfile)s'"

    def __init__(self, includeDirs=None):
        if includeDirs:
            self.addIncludeDirs(includeDirs)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _includeDirs = None
    def getIncludeDirs(self):
        if self._includeDirs is None:
            self.setIncludeDirs([])
        return self._includeDirs
    def setIncludeDirs(self, includeDirs):
        self._includeDirs = list(includeDirs)
    includeDirs = property(getIncludeDirs, setIncludeDirs)

    def addIncludeDirs(self, includeDirs):
        self.getIncludeDirs().extend(includeDirs)

    def _getIncludeDirsParam(self):
        includeDirs = self.includeDirs
        if not includeDirs:
            return ''
        return ' -I ' + " -I ".join(includeDirs)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def compile(self, srcfile, force=False):
        definesFilename = self._compileDefines(srcfile, force)
        xmlFilename = self._compileXML(srcfile, force)
        return (xmlFilename, definesFilename)
    __call__ = compile

    def compileAll(self, srcfiles):
        for src in srcfiles:
            yield self.compile(src)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _getXMLFilenameFrom(self, srcfile):
        if not os.path.exists(self.buildDir):
            os.makedirs(self.buildDir)
        return os.path.join(self.buildDir, srcfile + '.xml')
    def _compileXML(self, srcfile, force=False):
        xmlFilename = self._getXMLFilenameFrom(srcfile)
        if not force and os.path.exists(xmlFilename):
            if os.path.getmtime(xmlFilename) > os.path.getmtime(srcfile):
                return xmlFilename

        cmd = self.cmdCompileXML % dict(compiler=self.compiler, srcfile=srcfile, includeDirs=self._getIncludeDirsParam(), outfile=xmlFilename)

        r = self._execute(cmd)
        if r != 0 or not os.path.exists(xmlFilename): 
            raise Exception("Failed xml generation")

        return xmlFilename

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _getDefinesFilenameFrom(self, srcfile):
        if not os.path.exists(self.buildDir):
            os.makedirs(self.buildDir)
        return os.path.join(self.buildDir, srcfile + '.def')
    def _compileDefines(self, srcfile, force=False):
        definesFilename = self._getDefinesFilenameFrom(srcfile)
        if not force and os.path.exists(definesFilename):
            if os.path.getmtime(definesFilename) > os.path.getmtime(srcfile):
                return definesFilename

        cmd = self.cmdCompileDefines % dict(compiler=self.compiler, srcfile=srcfile, includeDirs=self._getIncludeDirsParam(), outfile=definesFilename)

        r = self._execute(cmd)
        if r != 0 or not os.path.exists(definesFilename): 
            raise Exception("Failed py module generation")

        return definesFilename
    
    def _execute(self, cmd):
        return os.system(cmd)


