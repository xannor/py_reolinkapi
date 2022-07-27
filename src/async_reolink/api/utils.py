"""Utilities and backports"""

from __future__ import annotations
from dataclasses import MISSING, Field, fields, is_dataclass

from typing import TYPE_CHECKING, AsyncGenerator, AsyncIterable, Callable, Generic, Iterable, Protocol, TypeVar, cast, overload, TypeGuard

_T = TypeVar("_T")
_S = TypeVar("_S")


class EnsureDataFields:
    """post init for dataclass to ensure field types"""

    def __post_init__(self):
        for _field in fields(self):
            v = getattr(self, _field.name)
            e = self.__ensure_type__(v, _field)
            if e is not v:
                setattr(self, _field.name, e)

    def __ensure_type__(self, __value: any, __field: str | Field, __type: type = None):
        if __value is None:
            if isinstance(__field, str):
                __field = next(filter(lambda f: f.name ==
                               __field), fields(self), __field)
            if isinstance(__field, Field):
                if __field.default is not MISSING:
                    return __field.default
                if __field.default_factory is not MISSING:
                    return __field.default_factory()
            return __value

        if not isinstance(__type, type):
            if isinstance(__field, str):
                __field = next(filter(lambda f: f.name ==
                               __field), fields(self), __field)
            __type = __field.type

        if isinstance(__value, __type):
            return __value

        if is_dataclass(__type) and isinstance(__value, dict):
            return __type(**__value)
        return __type(__value)


class _SupportsKeysAndGetItem(Protocol):
    def keys(self) -> Iterable[str]: ...
    def __getitem__(self, __name: str) -> any: ...


class Updateable(Generic[_T]):
    """Updateable mixin for dataclasses, etc"""

    def __update_item__(self, __name: str, __value: any):
        if not hasattr(self, __name):
            return False

        if (v := getattr(self, __name)) and (c := getattr(v, 'update')) and callable(c):
            if TYPE_CHECKING:
                c = cast(Updateable, c)
            c.update(__value)
            return True
        if isinstance(self, EnsureDataFields):
            __value = self.__ensure_type__(__value, __name)
        setattr(self, __name, __value)
        return True

    @overload
    def update(self, __m: _SupportsKeysAndGetItem, **kwargs) -> None: ...

    @overload
    def update(self, __m: Iterable[tuple[str, any]], **kwargs) -> None: ...

    @overload
    def update(self, **kwargs) -> None: ...

    def update(self, __m: any = None, **kwargs):
        """Update with new values"""
        if is_dataclass(__m):
            def _get_keys(field: Field):
                return field.name

            dc = __m

            def _getitem(key: str):
                return (key, getattr(dc, key))

            __m = map(_getitem, map(_get_keys, fields(__m)))
        elif __m is not None and hasattr(__m, 'keys') and hasattr(__m, '__getitem__'):
            skg = __m
            if TYPE_CHECKING:
                skg = cast(_SupportsKeysAndGetItem, __m)

            def _getitem(key: str):
                return (key, skg.__getitem__(key))

            __m = map(_getitem, skg.keys())

        if __m is not None:
            itr = __m
            if TYPE_CHECKING:
                itr = cast(Iterable[tuple[str, any]], __m)
            for pair in itr:
                self.__update_item__(*pair)

        for pair in kwargs.items():
            self.__update_item__(*pair)


class ConversionDescriptor(Generic[_T]):
    """Generic conversion descirptor for dataclasses"""

    def __init__(self, factory: type[_T], default: _T | None = None) -> None:
        super().__init__()
        self._name: str = None
        self._factory = factory
        self._default = default

    def __set_name__(self, owner, name: str):
        self._name = "_" + name

    def __get__(self, obj, _type):
        if obj is None:
            return self._default
        return getattr(obj, self._name, self._default)

    def __set__(self, obj, value):
        if value is self:
            value = self._default
        else:
            value = self._factory(value)
        setattr(obj, self._name, value)


@overload
async def afilter(
    __function: Callable[[_S], TypeGuard[_T]],
    __async_iterable: AsyncIterable[_S], /
) -> AsyncGenerator[_T, None, None]: ...


@overload
async def afilter(
    __function: Callable[[_T], any],
    __async_iterable: AsyncIterable[_T], /
) -> AsyncGenerator[_T, None, None]: ...


async def afilter(__function: Callable[[any], any], __iterable: AsyncIterable):
    """async filter()"""
    async for item in __iterable:
        if __function(item):
            yield item


@overload
async def amap(
    __function: Callable[[_S], _T],
    __async_iterable: AsyncIterable[_S]) -> AsyncGenerator[_T, None, None]: ...


async def amap(__function, __async_iterable):
    """async map()"""
    async for item in __async_iterable:
        yield __function(item)


@overload
async def alist(__async_iterable: AsyncIterable[_T]) -> list[_T]: ...


async def alist(__async_iterable):
    """async to list"""
    values = []
    async for item in __async_iterable:
        values.append(item)
    return values
