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

from steps.stepProcessor import StepProcessorBase

import steps.includes
import steps.defines
import steps.ifdef
import steps.code

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StepProcessor(StepProcessorBase):
    def setup(self):
        StepProcessorBase.setup(self)
        self.steps += [
            steps.includes.IncludesProcessorStep(),
            steps.defines.DefinesProcessorStep(),
            steps.ifdef.IfdefProcessorStep(),
            steps.code.CodeProcessorStep(),
            ]

    def start(self):
        self.root = RootElement()
    
    def visitStep(self, step):
        step.findElements(self.root)

    def end(self):
        pass

