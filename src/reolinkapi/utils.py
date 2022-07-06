"""Utilities and backports"""

from __future__ import annotations

from typing import AsyncGenerator, AsyncIterable, AsyncIterator, Callable, TypeVar, overload
from typing_extensions import TypeGuard

_T = TypeVar("_T")


@overload
async def anext(__async_iterator: AsyncIterator[_T]) -> _T: ...

_VT = TypeVar("_VT")


@overload
async def anext(
    __async_iterator: AsyncIterator[_T], __default: _VT
) -> _T | _VT: ...


class _undefined:
    pass


_UNDEFINED = _undefined()


async def anext(async_iterator: AsyncIterator, __default: any = _UNDEFINED):
    """async next"""
    try:
        return await async_iterator.__anext__()
    except StopAsyncIteration:
        if __default is not _UNDEFINED:
            return __default
        raise

_S = TypeVar("_S")


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
