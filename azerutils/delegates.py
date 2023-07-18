import inspect

class InvalidInvocationException(Exception):
     def __init__(self, _invocation):
          self.message = str(_invocation)

class Delegate:
    def __init__(self, _invocationList=[], _positionals=0, _names=[]):
        self.invocationList = _invocationList if hasattr(_invocationList, "__iter__") else [_invocationList]
        self.positionals = _positionals
        self.names = _names

        invalid = self.__validateInvocationList__()
        if invalid:
             raise InvalidInvocationException(invalid)

    def __validateInvocationList__(self):
        for invocation in self.invocationList:
                parameters = inspect.signature(invocation).parameters.values()
                if any([parameter.kind in (parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD) for parameter in parameters ]):
                     continue
                if len(parameters) < self.positionals:
                     return invocation
                if len([p for p in parameters if p.default == inspect.Parameter.empty]) > self.positionals:
                     return invocation
                if not set([p.name for p in parameters][self.positionals:]).issubset(set(self.names)):
                     return invocation
        return None
                     

    def __call__(self, *args, **kwargs):
        rtn = None
        if len(args) != self.positionals:
             raise TypeError(f"Expected {self.positionals} positional arguments, received {len(args)}")
        for kwarg in kwargs.keys():
             if not kwarg in self.names:
                  raise TypeError(f"Unexpected Keyword Argument :'{kwarg}'")          
        for invocation in self.invocationList:
            rtn = invocation(*args, **kwargs)
        return rtn
    
    def __iadd__(self, other):
        self.invocationList.append(other)
        invalid = self.__validateInvocationList__()
        if invalid:
            raise InvalidInvocationException(invalid)
        
    def __isub__(self, other):
        if other in self.invocationList:
            self.invocationList.pop(other)

class Transform(Delegate):
     def __init__(self, _invocationList=[], _carry=1, _positionals=0, _names=[]):
          self.carry = _carry
          super().__init__(_invocationList, _positionals, _names)

     def __call__(self, *args, **kwargs):
        rtn = None
        for i in range(len(self.invocationList)):
                if i == 0:
                    rtn = self.invocationList[i](*args, **kwargs)
                else:
                    rtn = self.invocationList[i](*rtn, *args[self.carry:], **kwargs) if hasattr(rtn, "__iter__") else self.invocationList[i](rtn, *args[1:], **kwargs)
        return rtn