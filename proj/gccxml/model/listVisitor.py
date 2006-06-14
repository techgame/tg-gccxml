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

    level = 0
    def onAtomCommon(self, item):
        print self.level * "  " + repr(item)

        self.level += 1
        item.visitChildren(self)
        self.level -= 1
        return item

