# XXX: Can this be done with a new-style class?
class SimpleDelegator:

    def __init__(self, obj):
        set_delegated(self, obj)

    def __getattr__(self, name):
        return getattr(get_delegated(self), name)

    def __getinitargs__(self):
        return (get_delegated(self),)

    def __setattr__(self, name, value):
        descriptor = self.__class__.__dict__.get(name)
        if hasattr(descriptor, '__set__'):
            descriptor.__set__(self, value)
        else:
            setattr(get_delegated(self), name, value)

    def __eq__(self, other):
        return get_delegated(self) == other


def get_delegated(delegator):
    return delegator.__dict__['_obj']


def set_delegated(delegator, obj):
    delegator.__dict__['_obj'] = obj
