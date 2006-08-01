#!/usr/bin/env python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
from TG.gccxml.model.emitters import FileBasedEmitter, emitKind
from TG.gccxml.analyzer.handlers.makefileRule import MakefileRuleScanner

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MakeEmitter(FileBasedEmitter):
    emitKindMap = FileBasedEmitter.emitKindMap.copy()

    def getFrameworkInfo(self, path):
        try:
            ri = path.rindex('.framework') + len('.framework/')
        except ValueError:
            return []

        frameworkPath, remaining = path[:ri-1], path[ri:]
        frameworkParent, frameworkName = os.path.split(frameworkPath)
        frameworkName = os.path.splitext(frameworkName)[0]
        return [(frameworkName, frameworkPath, remaining)] + self.getFrameworkInfo(frameworkParent)

    @emitKind(emitKindMap, 'includes')
    def onIncludes(self, kind, srcfile, dependencyList):
        for dep in dependencyList:
            info = self.getFrameworkInfo(dep)

            for sfi in info[:-1]:
                self.addSubFramework(sfi)

            for fi in info[-1:]:
                self.addFramework(fi)


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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    frameworks = {}
    emitter = MakeEmitter(frameworks)
    scanner = MakefileRuleScanner()

    if os.path.exists('Makefile.deps'):
        makefile = open('Makefile.deps')
    else:
        depsProcess = subprocess.Popen('gcc -E -MT TARGET -M src/genQuickTime.c -I inc  > Makefile.deps ', shell=True, stdout=subprocess.PIPE)
        makefile = depsProcess.stdout

    try:
        scanner(emitter, makefile)
    finally:
        makefile.close()

    createLinks = True
    for name, incPath in frameworks.iteritems():
        print name

        if createLinks:
            linkName = os.path.join('inc', name)
            parent = os.path.split(linkName)[0]
            if not os.path.exists(parent):
                os.makedirs(parent)

            if os.path.islink(linkName):
                os.unlink(linkName)

            os.symlink(incPath, linkName)

