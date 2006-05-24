class LineScanner(object):
    def __call__(self, handler, fileToScan):
        return self.scanFile(handler, fileToScan)
    def scanFile(self, handler, fileToScan):
        scanLine = self.scanLine
        mode = None

        if handler:
            incLineno = handler.incLineno
        else: incLineno = lambda: None
        for line in fileToScan:
            line = line.strip('\r\n')
            if mode is not None:
                mode = mode(handler, line)
            else:
                mode = scanLine(handler, line)

            incLineno()

    def scanLine(self, handler, line):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LineScannerWithContinuations(LineScanner):
    lineContinuation = '\\'

    def scanLine(self, handler, line, totalLine=''):
        totalLine = totalLine + line
        if line.endswith(self.lineContinuation):
            totalLine = totalLine[:-len(self.lineContinuation) or None]
            # line continuation
            return lambda h,l: self.scanLine(h,l, totalLine)
        else:
            return self.scanCompleteLine(handler, totalLine)

    def scanCompleteLine(self, handler, line):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

