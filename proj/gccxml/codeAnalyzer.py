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

from model.elements import RootElement
from analyzer.stepProcessor import StepProcessorBase
from analyzer import dependency, includes, defines, ifdef, code

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CodeAnalyzer(StepProcessorBase):
    RootElementFactory = RootElement

    def setup(self):
        StepProcessorBase.setup(self)
        self.steps += [
            dependency.DependencyProcessorStep(),
            includes.IncludesProcessorStep(),
            defines.DefinesProcessorStep(),
            ifdef.IfdefProcessorStep(),
            code.CodeProcessorStep(),
            ]

    def start(self):
        self.root = self.RootElementFactory()
    
    def visitStep(self, step):
        step.findElements(self.root)

    def end(self):
        pass

