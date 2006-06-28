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

import atoms

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
    root = None
    def __init__(self, root):
        self.root = root

    emitKindMap = {}
    def emit(self, kind, *args):
        emitCmd = self.emitKindMap.get(kind) or self.emitKindMap.get(None)
        if emitCmd:
            return emitCmd(self, kind, *args)

def emitKind(emitKindMap, key):
    def addToEmitKindMap(func):
        emitKindMap[key] = func
        return func
    return addToEmitKindMap

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FileBasedEmitter(BaseEmitter):
    fileAtom = None
    filename, lineno = "", 0

    def setFilename(self, filename, lineno=1):
        self.filename = filename
        self.lineno = int(lineno)
        self.fileAtom = self.root.getFile(filename)

    def incLineno(self, delta=1):
        self.lineno += 1

    def addElement(self, kind, data):
        self.fileAtom.addElement(self.lineno, kind, data)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    emitKindMap = BaseEmitter.emitKindMap.copy()

    @emitKind(emitKindMap, None)
    def onEmitDefault(self, kind, *args):
        print 'emit:', '"%s":%d' % (self.filename, self.lineno)
        print '   ', kind, args

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DependencyEmitter(FileBasedEmitter):
    def addFile(self, filename):
        self.fileAtom = self.root.addFile(filename)
    def addDependency(self, filename):
        self.root.addDependency(filename)

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
        # set to the previous line because we will be incremented before the
        # next line is read
        self.setFilename(filename, lineno-1)

    @emitKind(emitKindMap, 'position-push')
    def onPositionPush(self, kind, filename, lineno, flags=None):
        """This is generated as a result of a #include"""
        
    @emitKind(emitKindMap, 'position-load')
    def onPositionLoad(self, kind, filename, lineno, flags=None):
        """This is generated as a result of conditional (#if/#ifdef/#else/#elif) blocks"""

    @emitKind(emitKindMap, 'position-pop')
    def onPositionPop(self, kind, filename, lineno, flags=None):
        """This is generated after a #include is complete"""

    @emitKind(emitKindMap, 'conditional')
    def onCondition(self, kind, directive, body):
        return self.setItemAttrs(atoms.PPConditional(), directive=directive, body=body)

    @emitKind(emitKindMap, 'include')
    def onInclude(self, kind, filename, isSystemInclude):
        includedFile = self.root.getFile(filename)
        return self.setItemAttrs(atoms.PPInclude(), filename=filename, isSystemInclude=isSystemInclude, includedFile=includedFile)

    @emitKind(emitKindMap, 'define')
    def onDefine(self, kind, ident, body):
        return self.setItemAttrs(atoms.PPDefine(), ident=ident, body=body)

    @emitKind(emitKindMap, 'macro')
    def onMacro(self, kind, ident, args, body):
        return self.setItemAttrs(atoms.PPMacro(), ident=ident, args=args, body=body)

    def setItemAttrs(self, item, **attrs):
        file = self.fileAtom
        attrs.update(file=file, line=self.lineno)

        item._updateAttrs(attrs)
        if file is not None:
            self.linkConditional(item, file)
            file.addAtom(item)
        self.root.addPPAtom(item)
        return item

    def linkConditional(self, item, file):
        if not item.isPPConditional():
            return
        elif item.isOpening():
            item.prev = None
            item.next = None
        else:

            for lineno, lineItem in file.lines[::-1]:
                if lineItem.isPPConditional():
                    if lineItem.next or lineItem.isClosing():
                        continue

                    lineItem.next = item
                    item.prev = lineItem
                    break

registerEmitter(PreprocessorEmitter, 'preprocess')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GCCXMLCodeEmitter(FileBasedEmitter):
    emitKindMap = FileBasedEmitter.emitKindMap.copy()

    itemKindToAtoms = dict(
        FundamentalType=atoms.FundamentalType,
        CvQualifiedType=atoms.CvQualifiedType,
        Enumeration=atoms.Enumeration,
        EnumValue=atoms.EnumValue,
        Typedef=atoms.Typedef,
        PointerType=atoms.PointerType,
        ReferenceType=atoms.ReferenceType,
        ArrayType=atoms.ArrayType,
        Namespace=atoms.Namespace,
        Union=atoms.Union,
        Struct=atoms.Struct,
        Class=atoms.Class,
        Base=atoms.Base,
        Variable=atoms.Variable,
        Field=atoms.Field,
        Argument=atoms.Argument,
        Ellipsis=atoms.Ellipsis,
        FunctionType=atoms.FunctionType,
        Function=atoms.Function,
        Method=atoms.Method,
        Constructor=atoms.Constructor,
        Destructor=atoms.Destructor,
        )

    @emitKind(emitKindMap, 'create')
    def onCreate(self, kind, itemKind, topLevel, staticAttrs):
        # return item model to link
        if itemKind == 'File':
            filename = staticAttrs['name']
            item = self.root.getFile(filename)
            if item is None:
                item = atoms.File(filename)
        else:
            factory = self.itemKindToAtoms[itemKind]
            item = factory()
        item = self.setItemAttrs(item, staticAttrs)
        return item

    @emitKind(emitKindMap, 'add-child')
    def onAddChild(self, kind, model, childModel):
        model.addAtom(childModel)

    @emitKind(emitKindMap, 'linked')
    def onLinked(self, kind, itemKind, topLevel, item, linkedAttrs):
        item = self.setItemAttrs(item, linkedAttrs)

        if topLevel:
            file = getattr(item, 'file', None)
            if file is not None:
                file.addAtom(item)

        return item

    @emitKind(emitKindMap, 'link-child')
    def onLinkChild(self, kind, model, childModel):
        model.linkAtom(childModel)

    def setItemAttrs(self, item, attrs):
        item._updateAttrs(attrs)
        return item

registerEmitter(GCCXMLCodeEmitter, 'code', 'gccxml')

