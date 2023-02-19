"""ABC helpers"""

import inspect
from typing import TypeVar

_C = TypeVar("_C", bound=type)


def abstractclass(decorated_cls: _C):
    def abc_new(cls: type, *args, **kwargs):
        if cls is decorated_cls:
            raise TypeError("Cannot instanciate abstract class {}".format(decorated_cls.__name__))
        return super(decorated_cls, cls).__new__(cls)

    setattr(decorated_cls, "__abstract_class__", True)
    decorated_cls.__new__ = abc_new
    return decorated_cls


def isabstract(obj: object):
    if obj is type:
        try:
            object.__getattribute__(obj, "__abstract_class__")
        except AttributeError:
            pass
        else:
            return True
    return inspect.isabstract(obj)
