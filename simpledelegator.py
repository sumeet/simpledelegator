class SimpleDelegator:

    def __init__(self, obj):
        self.__dict__['_obj'] = obj

    def __getattr__(self, name):
        return getattr(self.__dict__['_obj'], name)

    def __getinitargs__(self):
        return (self.__dict__['_obj'],)

    def __setattr__(self, name, value):
        descriptor = self.__class__.__dict__.get(name)
        if hasattr(descriptor, '__set__'):
            descriptor.__set__(self, value)
        else:
            setattr(self.__dict__['_obj'], name, value)

    def __eq__(self, other):
        return self.__dict__['_obj'] == other
