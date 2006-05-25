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

from base import StepVisitor
from config import StepConfigVisitorMixin

from TG.gccxml.model.elements import RootElement

from includes import IncludesProcessorStep
from defines import DefinesProcessorStep
from ifdef import IfdefProcessorStep
from code import CodeProcessorStep

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StepProcessorBase(StepConfigVisitorMixin):
    def __init__(self):
        self.setup()

    def setup(self):
        self.steps = []

    def __call__(self):
        self.run()
    def run(self):
        self.start()
        for step in self.steps:
            step.visit(self)
        self.end()

    def start(self): pass
    def end(self): pass

    def visitStep(self, step):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StepProcessor(StepProcessorBase):
    def setup(self):
        StepProcessorBase.setup(self)
        self.steps += [
            IncludesProcessorStep(),
            DefinesProcessorStep(),
            IfdefProcessorStep(),
            CodeProcessorStep(),
            ]

    def start(self):
        self.root = RootElement()
    
    def visitStep(self, step):
        step.findElements(self.root)

    def end(self):
        pass

