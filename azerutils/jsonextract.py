class JsonHeaderExtractionException(Exception):
    def __init__(self, _message=None):
        if _message:
            self.message = _message
        else:
            self.message = "An Error occured while extracting JsonHeader"

class JsonInvalidBracketsException(JsonHeaderExtractionException):
    def __init__(self, _message=None, _iterator=None):
        if _message:
            self.message = _message
        elif _iterator:
            self.message = f"JsonHeader has {_iterator.openBracketCount}"
        else:
            self.message = "An Error occured while extracting JsonHeader"

class __jsonExtractIterator__:
    def __init__(self, _stream):
        self.source = _stream
        self.openBracketCount = 0
        self.__firstIter__ = True

    def __iter__(self):
        return self
    
    def __next__(self):
        if not self.openBracketCount and not self.__firstIter__:
            raise StopIteration
        self.__firstIter__ = False
        b = self.source.read(1)
        if b == b'{':
            self.openBracketCount += 1
        elif b == b'}':
            self.openBracketCount -= 1
        return self.openBracketCount

def SpliceJsonHeader(stream, supressParseError=False):
    startPosition = stream.tell()
    position = 0
    iterator = __jsonExtractIterator__(stream)
    for i in iterator:
        position += 1
    if not supressParseError and iterator.openBracketCount != 0:
        raise JsonInvalidBracketsException(_iterator=iterator)
    stream.seek(startPosition)
    return stream.read(position).decode('utf-8')