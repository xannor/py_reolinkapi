""" System Mixin """

from dataclasses import dataclass, field
from typing import ClassVar, Optional

from ..utils.dataclasses import flatten, ignore_none, keyword

from .command import (
    CommandRequest,
    CommandRequestParameter,
    CommandValueResponse,
    CommandValueResponseValue,
    response_type,
)

from ..meta.connection import ConnectionInterface

from .abilities import Abilities


@dataclass
class AbilityResponseValue(CommandValueResponseValue):
    """Abilities Response Value"""

    abilities: Abilities = field(default_factory=Abilities, metadata=keyword("Ability"))


@dataclass
class AbilityResponse(CommandValueResponse):
    """Abilities Response"""

    value: AbilityResponseValue = field(default_factory=AbilityResponseValue)


@dataclass
class UserInfo:
    """User info"""

    username: str = field(default=None, metadata=keyword("userName"))


@dataclass
class AbilityRequestParameter(CommandRequestParameter):
    """Ability Parameter"""

    info: UserInfo = field(metadata=keyword("User"))


@dataclass
@response_type(AbilityResponse)
class AbilityRequest(CommandRequest):
    """Authentication Login Request"""

    COMMAND: ClassVar = "GetAbility"
    param: AbilityRequestParameter = field(
        default=AbilityRequestParameter, metadata=ignore_none()
    )

    def __post_init__(self):
        self.command = type(self).COMMAND


@dataclass
class DeviceIO:
    """Device IO Info"""

    input: int = field(default=0, metadata=keyword("IOInputNum"))
    output: int = field(default=0, metadata=keyword("IOOutputNum"))


@dataclass
class DeviceVersions:
    """Device Version Info"""

    config: str = field(default="", metadata=keyword("cfgVer"))
    firmware: str = field(default="", metadata=keyword("firmVer"))
    hardware: str = field(default="", metadata=keyword("hardVer"))
    framework: str = field(default="", metadata=keyword("frameworkVer"))


@dataclass
class DeviceInfo:
    """Device Info"""

    io: DeviceIO = field(default_factory=DeviceIO, metadata=flatten())
    audio_count: int = field(default=0, metadata=keyword("audioNum"))
    build_day: str = field(default="", metadata=keyword("buildDay"))
    channels: int = field(default=0, metadata=keyword("channelNum"))
    detail: str = field(default="")
    disks: int = field(default=0, metadata=keyword("diskNum"))
    name: str = field(default="", metadata=keyword("name"))
    type: str = field(default="", metadata=keyword("type"))
    wifi: bool = field(default=False, metadata=keyword("wifi"))
    B485: int = field(default="", metadata=keyword("B485"))
    exact_type: str = field(default="", metadata=keyword("exactType"))
    versions: DeviceVersions = field(default_factory=DeviceVersions, metadata=flatten())
    serial: str = field(default="")
    pak_suffix: str = field(default="", metadata=keyword("pakSuffix"))


@dataclass
class DeviceInfoResponseValue(CommandValueResponseValue):
    """Device Info Response Value"""

    info: DeviceInfo = field(default_factory=DeviceInfo, metadata=keyword("DevInfo"))


@dataclass
class DeviceInfoResponse(CommandValueResponse):
    """DevInfo Command Response"""

    value: DeviceInfoResponseValue = field(default_factory=DeviceInfoResponseValue)


@dataclass
@response_type(DeviceInfoResponse)
class DeviceInfoRequest(CommandRequest):
    """DevInfo Command Request"""

    COMMAND: ClassVar = "GetDevInfo"

    def __post_init__(self):
        self.command = type(self).COMMAND
        self.param = None


class System:
    """System Commands Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self, ConnectionInterface) and not hasattr(self, "_execute"):
            # type "interface"
            self._execute = self._execute

    async def get_ability(self, username: Optional[str] = None):
        """Get User Permisions"""

        results = await self._execute(
            AbilityRequest(AbilityRequestParameter(UserInfo(username or "NULL")))
        )
        if len(results) != 1 or not isinstance(results[0], AbilityResponse):
            return None

        return results[0].value.abilities

    async def get_device_info(self):
        """Get Device Information"""

        results = await self._execute(DeviceInfoRequest())
        if len(results) != 1 or not isinstance(results[0], DeviceInfoResponse):
            return None

        return results[0].value.info
