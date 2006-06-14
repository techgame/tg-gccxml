#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pprint
from atoms import ModelAtomVisitor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ListingVisitor(ModelAtomVisitor):
    useCommonCalls = True

    def __init__(self):
        self.stack = []
    def onAtomCommon(self, item):
        if item in self.stack:
            return

        print '%08s|' % (getattr(item, 'line', 0) or ''), len(self.stack)*"  " + repr(item)


        self.stack.append(item)
        item.visitChildren(self)
        if self.stack.pop() is not item:
            raise Exception("Stack mismatch")
        return item

