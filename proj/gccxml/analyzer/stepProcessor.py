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

from config import StepConfigVisitorMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StepProcessorBase(StepConfigVisitorMixin):
    def __init__(self, **cfgkw):
        self.configure(**cfgkw)

    def setupProcess(self):
        self.config.setup()
        self.setupSteps()

    steps = None
    def setupSteps(self):
        self.steps = []

    def __call__(self):
        self.run()

    def visitAllSteps(self):
        if self.steps is None:
            self.setupProcess()
        self.startVisitSteps()
        for step in self.steps:
            step.visit(self)
        self.endVisitSteps()

    def startVisitSteps(self): 
        pass
    def endVisitSteps(self): 
        pass

    def visitStep(self, step):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

