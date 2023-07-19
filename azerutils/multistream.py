import threading
import uuid

class MultiStream:
    __BASESTREAM__ = 0
    def __init__(self, _source):
        self.source = _source
        self.sourceBasePosition = self.source.tell()
        self.seekDict = {MultiStream.__BASESTREAM__ : self.sourceBasePosition}
        
        self.accessLock = threading.Lock()
        self.baseStream = MultiStreamAccessor(self, MultiStream.__BASESTREAM__)

    def read(self, _key, *args, **kwargs):
        rtn = None
        try:
            self.accessLock.acquire()
            self.source.seek(self.sourceBasePosition + self.seekDict[_key])
            rtn = self.source.read(*args, **kwargs)
            self.seekDict[_key] = self.source.tell()
            self.source.seek(self.sourceBasePosition)
        finally:
            self.accessLock.release()
        return rtn
    
    def readline(self, _key, *args, **kwargs):
        rtn = None
        try:
            self.accessLock.acquire()
            self.source.seek(self.sourceBasePosition + self.seekDict[_key])
            rtn = self.source.readline(*args, **kwargs)
            self.seekDict[_key] = self.source.tell()
            self.source.seek(self.sourceBasePosition)
        finally:
            self.accessLock.release()
        return rtn
    
    def seek(self, _key, offset, whence=0, *args, **kwargs):
        if whence == 0:
            self.seekDict[_key] = offset
        elif whence == 1:
            self.seekDict[_key] += offset
        elif whence == 2:
            self.read(_key)
            self.seekDict[_key] = self.tell() - offset

    def tell(self, _key, *args, **kwargs):
        return self.seekDictp[_key]

    def write(self, _key=0, *args, **kwargs):
        return self.source.write(*args, **kwargs)
    
    def close(self, _key=0, *args, **kwargs):
        if _key == 0:
            self.source.close()
    
    def getNewAccessor(self):
        key = 0
        while key in self.seekDict:
            key = uuid.uuid4()
        return MultiStreamAccessor(self, key)
    
    def getAccessor(self, _key):
        if _key in self.seekDict:
            return MultiStreamAccessor(self, _key)
        raise KeyError(f"Stream {_key} does not exist. Did you mean to call getNewAccessor() instead?")

class MultiStreamAccessor:
    def __init__(self, _multistream, _key):
        self.multistream = _multistream
        self.key = _key

    def __getattr__(self, name):
        return lambda *args, **kwargs: getattr(self.multistream, name)(self.key, *args, **kwargs)
    
    def write(self, *args, **kwargs):
        return self.multistream.write(*args, **kwargs)