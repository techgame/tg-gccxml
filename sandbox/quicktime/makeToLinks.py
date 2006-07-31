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
        existing = self.root.get(key, value)
        if existing != value:
            print "KEY COLLISION:", key
            print

        self.root[key] = value

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    frameworks = {}
    emitter = MakeEmitter(frameworks)
    scanner = MakefileRuleScanner()
    scanner(emitter, open('inc/make', 'rb'))

    for n, v in frameworks.iteritems():
        if len(v) == 1: continue
        print n, '->', v

        n = os.path.join('inc', n)
        if os.path.islink(n):
            os.unlink(n)
        os.symlink(v, n)

