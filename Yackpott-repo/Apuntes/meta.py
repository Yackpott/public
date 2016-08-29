class CustomMetaclass(type):

    def __init__(cls, name, bases, dct):
        print(bases, len(bases))
        print(cls)
        print(name)
        if len(bases) > 0:
            raise AttributeError
        print("Creating class %s using CustomMetaclass" % name)
        return super(CustomMetaclass, cls).__init__(name, bases, dct)


class BaseClass(metaclass=CustomMetaclass):
    pass


class Subclass1(BaseClass):
    pass
