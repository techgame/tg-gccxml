class LineScanner(object):
    def __call__(self, emitter, fileToScan):
        return self.scanFile(emitter, fileToScan)
    def scanFile(self, emitter, fileToScan):
        scanLine = self.scanLine
        mode = None

        if emitter:
            incLineno = emitter.incLineno
        else: incLineno = lambda: None
        for line in fileToScan:
            line = line.strip('\r\n')
            if mode is not None:
                mode = mode(emitter, line)
            else:
                mode = scanLine(emitter, line)

            incLineno()

    def scanLine(self, emitter, line):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LineScannerWithContinuations(LineScanner):
    lineContinuation = '\\'

    def scanLine(self, emitter, line, totalLine=''):
        totalLine = totalLine + line
        if line.endswith(self.lineContinuation):
            totalLine = totalLine[:-len(self.lineContinuation) or None]
            # line continuation
            return lambda h,l: self.scanLine(h,l, totalLine)
        else:
            return self.scanCompleteLine(emitter, totalLine)

    def scanCompleteLine(self, emitter, line):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

