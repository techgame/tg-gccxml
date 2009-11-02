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

try:
    import cPickle as _pickle
except ImportError:
    import pickle as _pickle
import pickle as _pickle

import emitters
import atoms

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Elements
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RootElement(atoms.Root):
    def getDependencies(self):
        return self.files.iterkeys()
    def addDependency(self, filename):
        return self.addFile(filename)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    emitterFactoryMap = emitters.emitterFactoryMap
    def getEmitterFor(self, section, kind):
        factory = emitters.getEmitterFactoryFromMap(section, kind, 
                        self.emitterFactoryMap)
        return factory(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Pickle tools
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def storeToFileNamed(self, filename):
        modelFile = file(filename+'~', 'wb')
        try:
            result = self.storeToFile(modelFile)
        finally:
            modelFile.close()
        os.rename(filename+'~', filename)
        return result

    def storeToFile(self, file):
        s = _pickle.dumps(self, _pickle.HIGHEST_PROTOCOL)
        me = _pickle.loads(s)

        return _pickle.dump(self, file, _pickle.HIGHEST_PROTOCOL)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def loadFromFileNamed(klass, filename):
        modelFile = file(filename, 'rb')
        try:
            self = klass.loadFromFile(modelFile)
        finally:
            modelFile.close()
        return self

    @classmethod
    def loadFromFile(klass, file):
        self = _pickle.load(file)
        if not isinstance(self, klass):
            raise TypeError("File did not contain a RootElement")
        return self

