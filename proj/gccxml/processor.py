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

from steps.stepProcessor import StepProcessorBase

import steps.dependency
import steps.includes
import steps.defines
import steps.ifdef
import steps.code

import model.elements

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StepProcessor(StepProcessorBase):
    RootElementFactory = model.elements.RootElement

    def setup(self):
        StepProcessorBase.setup(self)
        self.steps += [
            steps.dependency.DependencyProcessorStep(),
            steps.includes.IncludesProcessorStep(),
            steps.defines.DefinesProcessorStep(),
            steps.ifdef.IfdefProcessorStep(),
            steps.code.CodeProcessorStep(),
            ]

    def start(self):
        self.root = self.RootElementFactory()
    
    def visitStep(self, step):
        step.findElements(self.root)

    def end(self):
        from pprint import pprint
        for n, f in self.root.files.iteritems():
            print
            print 'File:', n, f
            for lineno, atom in f.lines:
                if not atom.isPPInclude(): 
                    continue
                print ' ', lineno, ':', atom
                pprint(vars(atom), indent=10)

