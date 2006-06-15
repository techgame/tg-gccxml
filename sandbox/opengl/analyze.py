#!/usr/bin/env python
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

import cPickle
from TG.gccxml.model.atoms import ModelAtomVisitor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FunctionListing(ModelAtomVisitor):
    def onCallableCommon(self, item):
        if not item.isFunction(): return 
        if not item.extern: return

        args = (x[0] for x in self.iterArgNames(item))
        returns = item.returns.getTypeString()

        print '%s(%s): %s' % (item.name, ', '.join(args), returns)

    def iterArgNames(self, item, template='arg_%d'):
        return ((a.name or (template % i),a) for i, a in enumerate(item.arguments))
        

if __name__=='__main__':
    root = cPickle.load(file('gen.pickle', 'rb'))
    root.visitAll(FunctionListing())

