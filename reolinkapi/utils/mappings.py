""" Mappings """

from typing import MutableMapping, TypeVar


_K = TypeVar("_K")

_V = TypeVar("_V")


class Wrapped(MutableMapping[_K, _V]):
    """Generic dict Wrapper"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._wrapped: dict[_K, _V] = dict()
        self.update(*args, **kwargs)

    def __getitem__(self, key: _K):
        return self._wrapped[key]

    def __setitem__(self, key: _K, value: _V):
        self._wrapped[key] = value

    def __delitem__(self, key: _K):
        del self._wrapped[key]

    def __iter__(self):
        return iter(self._wrapped)

    def __len__(self):
        return len(self._wrapped)
