"""System Abilities Typings"""

from enum import IntEnum, IntFlag
from typing import Callable, Generic, TypeVar


class Permission(IntFlag):
    """Ability permissions (Permit)"""

    NONE = 0
    OPTION = 1
    WRITE = 2
    READ = 4


_T = TypeVar("_T")


class _Ability:
    def __init__(self, ability: dict, **kwargs) -> None:
        self._ability = ability
        super().__init__(**kwargs)

    @property
    def permissions(self):
        """permissions"""
        return Permission(self._ability.get("permit", 0))


class Ability(_Ability, Generic[_T]):
    """Ability"""

    def __init__(self, ability: dict, factory: Callable[[any], _T], default: any, **kwargs) -> None:
        super().__init__(ability=ability, **kwargs)
        self._value = factory
        self._default = default

    @property
    def value(self) -> _T:
        """value"""
        return self._value(self._ability.get("ver", self._default))


class BooleanAbility(Ability[bool]):
    """Boolean Ability"""

    def __init__(self, ability: dict, **kwargs) -> None:
        super().__init__(ability=ability, factory=bool, default=False, **kwargs)


class VideoClipValue(IntEnum):
    """Video Clip Ability Values"""

    NONE = 0
    FIXED = 1
    MOD = 2


class VideoClipAbility(Ability[VideoClipValue]):
    """Video Clip Ability"""

    def __init__(self, ability: dict, **kwargs) -> None:
        super().__init__(ability=ability, factory=VideoClipValue,
                         default=VideoClipValue.NONE, **kwargs)
