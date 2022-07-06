"""System Abilities Typings"""

from enum import IntEnum, IntFlag
from typing import Callable, Generic, TypeVar, get_args


class Permission(IntFlag):
    """Ability permissions (Permit)"""

    NONE = 0
    OPTION = 1
    WRITE = 2
    READ = 4


_T = TypeVar("_T")


class _MISSING_TYPE:  # pylint: disable=invalid-name
    pass


MISSING = _MISSING_TYPE()


class _Ability:
    def __init__(self, ability: dict, **kwargs) -> None:
        self._ability = ability
        super().__init__(**kwargs)

    def _get_permit(self):
        return Permission(self._ability.get("permit", 0))

    @property
    def permissions(self):
        """permissions"""
        return self._get_permit()

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, _Ability):
            return self._get_permit() == __o._get_permit()
        return __o is self


class Ability(_Ability, Generic[_T]):
    """Ability"""

    def __init__(
        self,
        ability: dict,
        factory: Callable[[any], _T] = MISSING,
        default: _T = MISSING,
        **kwargs,
    ) -> None:
        super().__init__(ability=ability, **kwargs)
        self._default = default
        self._factory = factory

    def _get_ver(self):
        default = self._default if self._default is not MISSING else None
        value: _T = self._ability.get("ver", default)
        if self._factory is not MISSING:
            return self._factory(value)
        return value

    @property
    def value(self):
        """value"""
        return self._get_ver()

    def __getattr__(self, __name: str) -> any:
        value = self._get_ver()
        if value is None:
            raise AttributeError(self, __name)
        return getattr(value, __name)

    def __repr__(self) -> str:
        return f"<{self.__class__}:{repr(self._get_permit())}|{repr(self._get_ver())}>"

    def __bool__(self) -> bool:
        return bool(self._get_ver())

    def __eq__(self, __o: object) -> bool:
        if __o is self:
            return True
        if isinstance(__o, Ability):
            return (
                self._get_ver() == __o._get_ver()
                and self._get_permit() == __o._get_permit()
            )

        return self._get_ver() == __o


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
        super().__init__(
            ability=ability,
            factory=VideoClipValue,
            default=VideoClipValue.NONE,
            **kwargs,
        )
