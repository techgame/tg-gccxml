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

from handlers import RootElement

from codeDepends import CodeDependencyStep
from defines import DefinesProcessorStep
from ifdef import IfdefProcessorStep

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StepProcessorBase(StepConfigVisitorMixin):
    def __init__(self):
        self.setup()

    def __call__(self):
        self.run()

    def setup(self):
        self.steps = []

    def run(self):
        self.start()
        for step in self.steps:
            step.visit(self)
        self.end()

    def visitStep(self, step):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StepProcessor(StepProcessorBase):
    def setup(self):
        StepProcessorBase.setup(self)
        self.steps += [
            CodeDependencyStep(),
            DefinesProcessorStep(),
            #IfdefProcessorStep(),
            #CodeProcessorStep(),
            ]

    def start(self):
        print 'start:'
        self.root = RootElement()
    
    def end(self):
        print 'end:'

    def visitDependencyStep(self, step):
        print 'visitDependencyStep:'
        depList = step.findDependencies()
        for dep in depList:
            self.root.addFile(dep)

    def visitElementStep(self, step):
        print 'visitElementStep:'
        step.findElements(self.root)

