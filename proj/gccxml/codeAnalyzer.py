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

import os.path
from model.elements import RootElement
from analyzer.stepProcessor import StepProcessorBase
from analyzer import dependency, includes, defines, ifdef, code

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CodeAnalyzer(StepProcessorBase):
    RootElementFactory = RootElement

    def setupSteps(self):
        StepProcessorBase.setupSteps(self)
        self.steps += [
            dependency.DependencyProcessorStep(),
            includes.IncludesProcessorStep(),
            defines.DefinesProcessorStep(),
            ifdef.IfdefProcessorStep(),
            code.CodeProcessorStep(),
            ]

    def startVisitSteps(self):
        self.root = self.RootElementFactory()
    
    def visitStep(self, step):
        step.findElements(self.root)

    def endVisitSteps(self):
        modelFile = self.cfg.modelFile
        if modelFile:
            try:
                self.root.storeToFileNamed(modelFile)
            except RuntimeError:
                import traceback
                traceback.print_exc()
                return False
        return True

    def loadModel(self, runIfNotFound=True):
        modelFile = self.cfg.modelFile
        if os.path.exists(modelFile):
            self.root = self.RootElementFactory.loadFromFileNamed(modelFile)
        elif runIfNotFound:
            self.run()
        else:
            self.root = None
        return self.root

    def run(self):
        self.visitAllSteps()
        return self.root

