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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

emitterFactoryMap = {}

def registerEmitter(handlerFactory, section, kind=None):
    if kind: key = (section, kind)
    else: key = (section,)
    emitterFactoryMap[key] = handlerFactory

def getEmitterFactoryFromMap(section, kind, factoryMap=emitterFactoryMap):
    factory = (factoryMap.get((section, kind)) or 
                factoryMap.get((section, )) or 
                factoryMap.get(())
                )

    if factory:
        return factory
    else:
        raise KeyError("No factory registered for (%s, %s)" % (section, kind))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Emitters
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BaseEmitter(object):
    rootElement = None
    def __init__(self, rootElement):
        self.rootElement = rootElement

    emitKindMap = {}
    def emit(self, kind, *args):
        emitCmd = self.emitKindMap.get(kind) or self.emitKindMap.get(None)
        if emitCmd:
            emitCmd(self, kind, *args)

def emitKind(emitKindMap, key):
    def addToEmitKindMap(func):
        emitKindMap[key] = func
        return func
    return addToEmitKindMap

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FileBasedEmitter(BaseEmitter):
    fileElement = None
    filename, lineno = "", 0

    def setFilename(self, filename, lineno=1):
        self.filename = filename
        self.lineno = int(lineno)
        self.fileElement = self.rootElement.files.get(filename, None)

    def incLineno(self, delta=1):
        self.lineno += 1

    def addElement(self, kind, data):
        self.fileElement.addElement(self.lineno, kind, data)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    emitKindMap = BaseEmitter.emitKindMap.copy()

    @emitKind(emitKindMap, None)
    def onEmitDefault(self, kind, *args):
        print 'emit:', '"%s":%d' % (self.filename, self.lineno)
        print '   ', kind, args

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DependencyEmitter(FileBasedEmitter):
    def addFile(self, filename):
        self.fileElement = self.rootElement.addFile(filename)
    def addDependency(self, filename):
        self.rootElement.addDependency(filename)

    emitKindMap = FileBasedEmitter.emitKindMap.copy()

    @emitKind(emitKindMap, 'includes')
    def onIncludes(self, kind, srcfile, dependencyList):
        self.addFile(srcfile)
        for d in dependencyList:
            self.addDependency(d)

    @emitKind(emitKindMap, 'includes-baseline')
    def onIncludesBaseline(self, kind, srcfile, dependencyList):
        pass

registerEmitter(DependencyEmitter, 'dependency')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PreprocessorEmitter(FileBasedEmitter):
    emitKindMap = FileBasedEmitter.emitKindMap.copy()

    @emitKind(emitKindMap, 'position')
    def onPosition(self, kind, filename, lineno, flags=None):
        self.setFilename(filename, lineno)

    @emitKind(emitKindMap, 'conditional')
    def onCondition(self, kind, directive, body):
        pass

    @emitKind(emitKindMap, 'define')
    def onDefine(self, kind, ident, body):
        pass

    @emitKind(emitKindMap, 'macro')
    def onMacro(self, kind, ident, args, body):
        pass

registerEmitter(PreprocessorEmitter, 'preprocess')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GCCXMLCodeEmitter(FileBasedEmitter):
    emitKindMap = FileBasedEmitter.emitKindMap.copy()

    @emitKind(emitKindMap, 'gccxml-model')
    def onModel(self, kind, model):
        pass

registerEmitter(GCCXMLCodeEmitter, 'code', 'gccxml')

