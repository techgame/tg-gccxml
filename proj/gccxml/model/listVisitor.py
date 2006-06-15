#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pprint
from atoms import ModelAtomVisitor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ListingVisitor(ModelAtomVisitor):
    def __init__(self):
        self.stack = []

    def onAtomCommon(self, item):
        if item in self.stack:
            return

        self.onItem(item)
        if self.predicate(item):
            self.stack.append(item)
            try:
                item.visitChildren(self)
            finally:
                stackItem = self.stack.pop()
            if stackItem is not item:
                raise Exception("Stack mismatch")

    def onItem(self, item):
        self.printItem(item, len(self.stack))

    def predicate(self, item):
        return True

    def printItem(self, item, indent=-1):
        if indent < 0: indent = len(self.stack)
        lineno = (getattr(item, 'line', 0) or '')
        indent *= "    "
        print '%08s|%s%r' % (lineno, indent, item)

