""" helpers """

import dataclasses
import json
from typing import Optional, Type, TypeVar, TypedDict, cast

MISSING = dataclasses.MISSING


class CustomJSONEncoder(json.JSONEncoder):
    """custom JSON Encoder that supports the dataclasses"""

    def default(self, o):
        """json.dumps"""

        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o, dict_factory=getattr(type(o), "dict_factory"))
        return super().default(o)


T = TypeVar("T")


def typeddict_validate(o: dict, _type: Type[T]) -> Optional[T]:
    """check if dict is TypedDict and cast"""
    unseen = set(_type.__annotations__.keys())
    for key, value in o.items():
        if key in _type.__annotations__:
            _t = type.__annotations__[key]
            if issubclass(_t, TypedDict) and typeddict_validate(value, _t) is None:
                return None
            if isinstance(value, _type.__annotations__[key]):
                unseen.remove(key)
            else:
                return None
    # TODO: check totality flag and skip if set false
    if unseen != set():
        return None
    return cast(o, T)
