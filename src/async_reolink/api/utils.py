"""Utilities and backports"""

from __future__ import annotations

from typing import AsyncGenerator, AsyncIterable, Callable, TypeVar, overload
from typing_extensions import TypeGuard

_T = TypeVar("_T")
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
