""" extended dataclasses """

import dataclasses
from json import JSONEncoder
from typing import (
    Callable,
    Mapping,
    Optional,
    TypeVar,
    Union,
    get_args,
    get_origin,
    overload,
)


_T = TypeVar("_T")


def is_optional(_type: type):
    """is optional"""
    return get_origin(_type) is Union and type(None) in get_args(_type)


def non_optional_type(_type: type):
    """get non optional type"""
    if get_origin(_type) is not Union:
        return _type
    args = get_args(_type)
    nargs = tuple(filter(lambda t: t is not type(None), args))
    if len(nargs) == args:
        return _type
    if len(nargs) == 1:
        return nargs[0]
    return Union[args]


_KEYWORD_NAME = "keyword"


def keyword(name: str, metadata: Mapping = None) -> Mapping:
    """add keyword to metadata"""
    if metadata is None:
        metadata = {}
    metadata[_KEYWORD_NAME] = name
    return metadata


_FLATTEN_NAME = "flatten"


def flatten(prefix: bool = False, metadata: Mapping = None) -> Mapping:
    """prevent heirarcal decent"""
    if metadata is None:
        metadata = {}
    metadata[_FLATTEN_NAME] = prefix
    return metadata


_IGNORE_NAME = "ignore_none"


def ignore_none(metadata: Mapping = None) -> Mapping:
    """ignore fields with none in dict"""
    if metadata is None:
        metadata = {}

    metadata[_IGNORE_NAME] = True
    return metadata


@overload
def asdict(obj, *, dict_factory: Callable[[list[tuple[str, any]]], _T]) -> _T:
    """as dict wrapper"""


@overload
def asdict(obj) -> dict[str, any]:
    """as dict wrapper"""


def _inner_asdict(_dict: dict, cls: type):
    if not dataclasses.is_dataclass(cls):
        return _dict
    for _field in dataclasses.fields(cls):
        if _field.name not in _dict:
            continue
        _type = non_optional_type(_field.type)
        if dataclasses.is_dataclass(_type):
            value = _dict.get(_field.name)
            if isinstance(value, dict):
                _inner_asdict(value, _type)
        key = _field.metadata.get(_KEYWORD_NAME, _field.name)
        if not isinstance(key, str):
            continue
        # dirty "rename" will change key order
        value = _dict.pop(_field.name)
        if value is None and _field.metadata.get(_IGNORE_NAME, False):
            continue
        prefix = _field.metadata.get(_FLATTEN_NAME)
        if isinstance(value, dict) and prefix is not None:
            if isinstance(prefix, str):
                value = dict({prefix + k: v for k, v in value.items()})
            dict.update(value)
            continue

        _dict[key] = value

    return _dict


def asdict(obj, *, dict_factory=dict):
    """as dict wrapper"""
    _dict = dataclasses.asdict(obj, dict_factory=dict_factory)
    return _inner_asdict(_dict, type(obj))


def isdictof(
    __dict: dict,
    cls: type,
):
    """is dictionary of dataclass"""
    if not dataclasses.is_dataclass(cls):
        return False
    for _field in dataclasses.fields(cls):
        key = _field.metadata.get(_KEYWORD_NAME, _field.name)
        _type = non_optional_type(_field.type)
        if dataclasses.is_dataclass(_type):
            value = __dict.get(key)
            if not isinstance(value, dict):
                return False
            if not isdictof(value, _type):
                return False
        elif not isinstance(__dict.get(key), _field.type):
            return False
    return True


def _resolve_typevar(cls: type, __type: type):
    if not isinstance(__type, TypeVar):
        return __type
    bases = getattr(cls, "__orig_bases__", [])
    args = get_args(bases[0])
    origin = get_origin(bases[0])
    params = getattr(origin, "__parameters__", [])
    idx = params.index(__type)
    return args[idx]


def _inner_fromdict(__dict: dict, cls: type, prefix: str = ""):
    if not dataclasses.is_dataclass(cls):
        return None

    init_kwargs = {}
    for _field in dataclasses.fields(cls):
        if not _field.init:
            continue
        _type = _resolve_typevar(cls, non_optional_type(_field.type))
        _prefix = _field.metadata.get(_FLATTEN_NAME)
        if _prefix is not None:
            if not isinstance(_prefix, str):
                _prefix = prefix + _field.name if _prefix else ""
            value = _inner_fromdict(__dict, _type, _prefix)
        else:
            value = __dict.get(prefix + _field.metadata.get(_KEYWORD_NAME, _field.name))
        if value is None:
            if _field.default is not dataclasses.MISSING:
                value = _field.default
            elif _field.default_factory is not dataclasses.MISSING:
                value = _field.default_factory()
        elif dataclasses.is_dataclass(_type) and isinstance(value, dict):
            value = _inner_fromdict(value, _type)
        elif isinstance(value, list) and get_origin(_type) is list:
            value = _inner_fromlist(value, _type)
        elif not isinstance(value, _type):
            try:
                value = _type(value)
            except Exception:
                # TODO : limit to just cannot cast style exceptions
                value = None
        if value is None:
            continue
        init_kwargs[_field.name] = value

    return cls(**init_kwargs)


def fromdict(__dict: dict, cls: type[_T]) -> Optional[_T]:
    """create dataclass from"""
    return _inner_fromdict(__dict, cls)


def _inner_fromlist(__list: list, cls: type):
    args = get_args(cls)
    _type = args[0]
    if not dataclasses.is_dataclass(_type):
        return __list
    return list(map(lambda i: _inner_fromdict(i, _type), __list))


class DataclassesJSONEncoder(JSONEncoder):
    """JSON Encoder"""

    def default(self, o: any) -> any:
        if dataclasses.is_dataclass(o):
            return asdict(o)
        return super().default(o)
