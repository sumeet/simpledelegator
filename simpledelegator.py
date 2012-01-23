class SimpleDelegator:

    def __init__(self, obj):
        self.__dict__['_obj'] = obj

    def __getattr__(self, name):
        return getattr(delegated(self), name)

    def __getinitargs__(self):
        return (delegated(self),)

    def __setattr__(self, name, value):
        descriptor = self.__class__.__dict__.get(name)
        if hasattr(descriptor, '__set__'):
            descriptor.__set__(self, value)
        else:
            setattr(delegated(self), name, value)

    def __eq__(self, other):
        return delegated(self) == other


def delegated(decorator):
    return decorator.__dict__['_obj']
