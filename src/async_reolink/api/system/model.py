"""System Models"""

from typing import Final, TypeVar, final

from .capabilities import Capability, Permissions
from .typing import DeviceInfo

NO_PERMISSIONS: Final[Permissions] = 0

_T = TypeVar("_T")


@final
class _Capability(Capability[_T]):
    """No Capability"""

    __slots__ = ()

    @property
    def value(self):
        """Value"""
        return 0

    @property
    def permissions(self):
        """Permissions"""
        return NO_PERMISSIONS

    def __index__(self):
        return 0

    def __str__(self):
        return ""

    def __bool__(self):
        return False

    def __eq__(self, __o: object) -> bool:
        return False

    def __getattr__(self, __name: str):
        return NO_CAPABILITY

    def __len__(self):
        return 0

    def __getitem__(self, __key):
        return NO_CAPABILITY


NO_CAPABILITY: Final = _Capability()


@final
class _DeviceInfo(DeviceInfo):
    """No DeviceInfo"""

    __slots__ = ()

    def __index__(self):
        return 0

    def __str__(self):
        return ""

    def __bool__(self):
        return False

    def __eq__(self, __o: object) -> bool:
        return False

    def __getattr__(self, __name: str):
        return NO_DEVICEINFO

    def __len__(self):
        return 0


NO_DEVICEINFO: Final = _DeviceInfo()
