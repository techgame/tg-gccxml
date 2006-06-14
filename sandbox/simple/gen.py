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
from TG.gccxml.processor import StepProcessor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def inspectResult(root):
    from pprint import pprint
    for n, f in root.files.iteritems():
        print
        print 'File:', n, f
        for lineno, atom in f.lines:
            print ' ', lineno, ':', atom
            pprint(vars(atom), indent=10)

def main():
    sp = StepProcessor()

    sp.cfg.inc = ['.']
    sp.cfg.src = ['genSource.cpp']
    sp.cfg.baseline = ['baseline.cpp']

    sp.run()

    return sp

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    sp = main()

    genFile = file('gen.pickle', 'wb')
    print 'Dumping root to:', genFile.name
    try:
        cPickle.dump(sp.root, genFile, cPickle.HIGHEST_PROTOCOL)
    finally:
        genFile.close()

    #inspectResult(sp.root)

