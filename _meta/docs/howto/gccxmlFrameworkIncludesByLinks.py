#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
## Copyright (c) 2002-2006, TechGame Networks, LLC.
## All rights reserved.
## 
## Redistribution and use in source and binary forms, with or without modification, are permitted 
## provided that the following conditions are met:
## 
## 
##     * Redistributions of source code must retain the above copyright notice, 
##       this list of conditions and the following disclaimer.
## 
##     * Redistributions in binary form must reproduce the above copyright notice, 
##       this list of conditions and the following disclaimer in the documentation and/or 
##       other materials provided with the distribution.
## 
##     * Neither the name of TechGame Networks, LLC nor the names of its contributors may 
##       be used to endorse or promote products derived from this software without specific 
##       prior written permission.
## 
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS 
## OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY 
## AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR 
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
## DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER 
## IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT 
## OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import subprocess

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FindFrameworkIncPaths(object):
    root = None

    def __init__(self, dependencyList=None):
        self.dependencyList = dependencyList

    def __call__(self, dependencyList=None):
        dependencyList = dependencyList or self.dependencyList
        self.root = {}
        for dep in dependencyList:
            info = self.getFrameworkInfo(dep)

            for sfi in info[:-1]:
                self.addSubFramework(sfi)

            for fi in info[-1:]:
                self.addFramework(fi)

    def __iter__(self):
        if not self.root:
            self(self.dependencyList)
        return self.root.iteritems()

    def getFrameworkInfo(self, path):
        try:
            ri = path.rindex('.framework') + len('.framework/')
        except ValueError:
            return []

        frameworkPath, remaining = path[:ri-1], path[ri:]
        frameworkParent, frameworkName = os.path.split(frameworkPath)
        frameworkName = os.path.splitext(frameworkName)[0]
        return [(frameworkName, frameworkPath, remaining)] + self.getFrameworkInfo(frameworkParent)

    def addSubFramework(self, subframeworkInfo):
        frameworkName, frameworkPath, remaining = subframeworkInfo

        subframeworkRoot, subframeworkName = os.path.split(frameworkPath)
        supframeworkPath = os.path.split(subframeworkRoot)[1]
        subframeworkName = os.path.join(supframeworkPath, subframeworkName)

        self._addLink(subframeworkName, frameworkPath)
        self.addFramework(subframeworkInfo)

    def addFramework(self, frameworkInfo):
        frameworkName, frameworkPath, remaining = frameworkInfo
        self._addLink(frameworkName, os.path.join(frameworkPath, 'Headers'))

    def _addLink(self, key, value):
        value = os.path.abspath(value)
        existing = self.root.get(key, value)
        if existing != value:
            print "KEY COLLISION:", key
            print "  Old:", existing
            print "  New:", value
            print

        self.root[key] = value

def getDependenciesFromMakefile(makefile):
    lines = makefile.read()
    lines = lines.replace("\\ ", "\\%20").replace("\\\n", "")
    root, depends = lines.split(':')

    return (e.strip().replace("\\%20", "\\ ") for e in depends.split(' '))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    if os.path.exists('Makefile.deps'):
        makefile = open('Makefile.deps')
    else:
        depsProcess = subprocess.Popen('gcc -E -MT TARGET -M src/genQuickTime.c -I inc  > Makefile.deps ', shell=True, stdout=subprocess.PIPE)
        makefile = depsProcess.stdout

    try:
        depends = getDependenciesFromMakefile(makefile)
    finally:
        makefile.close()

    frameworks = FindFrameworkIncPaths(depends)
    createLinks = True

    for name, incPath in frameworks:
        print name

        if createLinks:
            linkName = os.path.join('inc', name)
            parent = os.path.split(linkName)[0]
            if not os.path.exists(parent):
                os.makedirs(parent)

            if os.path.islink(linkName):
                os.unlink(linkName)

            os.symlink(incPath, linkName)

