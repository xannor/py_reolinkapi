""" extended dataclasses """

import copy
import dataclasses
from json import JSONEncoder
from typing import (
    Callable,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
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
    return Union[nargs]


_KEYWORD_NAME = "keyword"


def keyword(value: str, metadata: Mapping = None) -> Mapping:
    """add keyword to metadata"""
    if metadata is None:
        metadata = {}
    metadata[_KEYWORD_NAME] = value
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


def _asdict_inner_field(
    value,
    _field: dataclasses.Field,
    dict_factory: Callable[[list[tuple[str, any]]], dict],
):
    key = _field.metadata.get(_KEYWORD_NAME, _field.name)
    value = _asdict_inner(value, dict_factory)
    if value is None and _field.metadata.get(_IGNORE_NAME, False):
        return None

    return (key, value)


def _asdict_inner_dataclass(obj, dict_factory: Callable[[list[tuple[str, any]]], dict]):
    result = []
    for _field in dataclasses.fields(obj):
        value_tuple = _asdict_inner_field(
            getattr(obj, _field.name), _field, dict_factory
        )
        if not value_tuple is None:
            if isinstance(value_tuple[1], dict):
                prefix = _field.metadata.get(_FLATTEN_NAME)
                if prefix is not None:
                    if not isinstance(prefix, str):
                        prefix = value_tuple[0] if prefix is True else ""
                    for k, v in value_tuple[1].items():
                        result.append((prefix + k, v))
                    continue
            result.append(value_tuple)

    if len(result) == 0:
        return None
    return dict_factory(result)


def _asdict_inner(obj, dict_factory: Callable[[list[tuple[str, any]]], dict]):
    if dataclasses.is_dataclass(obj):
        return _asdict_inner_dataclass(obj, dict_factory)
    if isinstance(obj, tuple) and hasattr(obj, "__fields__"):
        return type(obj)(*[_asdict_inner(v, dict_factory) for v in obj])
    if isinstance(obj, Sequence) and not isinstance(obj, str):
        return list(_asdict_inner(v, dict_factory) for v in obj)
    if isinstance(obj, Mapping):
        return dict(
            (_asdict_inner(k, dict_factory), _asdict_inner(v, dict_factory))
            for k, v in obj.items()
        )
    return copy.deepcopy(obj)


@overload
def asdict(obj, *, dict_factory: Callable[[list[tuple[str, any]]], _T]) -> _T:
    pass


@overload
def asdict(obj) -> dict[str, any]:
    pass


def asdict(obj, *, dict_factory=dict):
    """wrapper for dataclasses.asdict"""
    if not dataclasses.is_dataclass(obj):
        raise TypeError("asdict() should be called on dataclass instances")

    return _asdict_inner_dataclass(obj, dict_factory)


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


def _inner_fromvalue(value, cls: type, factory: Callable = None):
    cls = non_optional_type(cls)
    if isinstance(value, dict):
        return _inner_fromdict(value, cls, factory)
    if isinstance(value, list):
        return _inner_fromlist(value, cls, factory)
    if not isinstance(value, cls):
        try:
            return cls(value)
        except:
            return None  # TODO : catach all?
    return value


def _inner_fromdataclass(__dict: dict, cls: type, prefix: str = ""):
    init_kwargs = {}
    for _field in dataclasses.fields(cls):
        if not _field.init:
            continue
        _type = _resolve_typevar(cls, non_optional_type(_field.type))
        _prefix = _field.metadata.get(_FLATTEN_NAME)
        if _prefix is not None:
            if not isinstance(_prefix, str):
                _prefix = prefix + _field.name if _prefix else ""
            value = _inner_fromdataclass(__dict, _type, _prefix)
        else:
            value = __dict.get(prefix + _field.metadata.get(_KEYWORD_NAME, _field.name))
        if value is None:
            if _field.default is not dataclasses.MISSING:
                value = _field.default
            elif _field.default_factory is not dataclasses.MISSING:
                value = _field.default_factory()
        else:
            value = _inner_fromvalue(
                value,
                _type,
                _field.default_factory
                if _field.default_factory is not dataclasses.MISSING
                else None,
            )
        if value is None:
            continue
        init_kwargs[_field.name] = value

    return cls(**init_kwargs)


def _inner_fromdict(
    __dict: dict, cls: type, factory: Callable[[], MutableMapping] = None
):
    if dataclasses.is_dataclass(cls):
        return _inner_fromdataclass(__dict, cls)
    if cls is not Mapping and cls is not dict:
        return None
    args = get_args(cls) or get_args(get_origin(cls))
    if factory is not None:
        value = factory()
        value.update({k: _inner_fromvalue(v, args[1]) for k, v in __dict.items()})
        return value
    return cls({k: _inner_fromvalue(v, args[1]) for k, v in __dict.items()})


def _inner_fromlist(
    __list: list, cls: type, factory: Callable[[], MutableSequence] = None
):
    origin = get_origin(cls)
    if origin not in (list, tuple, Sequence):
        return None
    args = get_args(cls) or get_args(get_origin(cls))
    if factory is not None:
        value = factory()
        for v in __list:
            value.append(_inner_fromvalue(v, args[0]))
    return cls((_inner_fromvalue(v, args[0]) for v in __list))


def fromdict(__dict: dict, cls: type[_T]) -> Optional[_T]:
    """create dataclass from"""
    return _inner_fromdict(__dict, cls)


class DataclassesJSONEncoder(JSONEncoder):
    """JSON Encoder"""

    def default(self, o: any) -> any:
        if dataclasses.is_dataclass(o):
            return asdict(o)
        return super().default(o)
