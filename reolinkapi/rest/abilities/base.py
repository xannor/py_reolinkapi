""" Base Ability Code """

from dataclasses import dataclass, field
from enum import IntFlag
from typing import Generic, TypeVar, get_args

from ...utils.dataclasses import keyword


class Permission(IntFlag):
    """Permission"""

    NONE = 0
    OPTION = 1
    WRITE = 2
    READ = 4


_T = TypeVar("_T")


class _GENERIC_FACTORY:
    pass


GENERIC_FACTORY = _GENERIC_FACTORY


@dataclass
class Ability(Generic[_T]):
    """Ability"""

    supported: _T = field(default=GENERIC_FACTORY, metadata=keyword("ver"))
    permission: Permission = field(default=Permission.NONE, metadata=keyword("permit"))

    def __post_init__(self):
        if self.supported is GENERIC_FACTORY:
            bases = getattr(type(self), "__orig_bases__") or []
            args = get_args(bases[0])
            _type = args[0]

            self.supported = _type(0)
