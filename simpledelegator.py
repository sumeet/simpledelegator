# XXX: Old-style class required to delegate magic methods with __getattr__.
class SimpleDelegator:

    def __init__(self, obj):
        set_delegated(self, obj)

    def __getattr__(self, name):
        return getattr(get_delegated(self), name)

    def __getinitargs__(self):
        return (get_delegated(self),)

    def __setattr__(self, name, value):
        descriptor = vars(self.__class__).get(name)
        if hasattr(descriptor, '__set__'):
            descriptor.__set__(self, value)
        else:
            setattr(get_delegated(self), name, value)

    def __eq__(self, other):
        return get_delegated(self) == other


def get_delegated(delegator):
    return vars(delegator)['_obj']


def set_delegated(delegator, obj):
    vars(delegator)['_obj'] = obj
