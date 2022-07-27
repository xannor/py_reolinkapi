"""System"""
from __future__ import annotations

from dataclasses import dataclass
import datetime
from enum import IntEnum
from typing import ClassVar, Final, TypedDict, TypeGuard

from ..utils import afilter, alist, amap

from ..commands import (
    CommandRequestTypes,
    CommandRequest,
    CommandRequestWithParam,
    CommandResponseValue,
    async_trap_errors,
)

from .abilities import Abilities

from .. import connection


@dataclass
class User:
    """User Info"""

    userName: str  # pylint: disable=invalid-name


class DeviceVersionsType(TypedDict):
    """Device Version Info"""

    cfgVer: str
    firmVer: str
    hardVer: str
    frameworkVer: str


class DeviceInfoType(DeviceVersionsType):
    """Device Info"""

    IOInputNum: int
    IOOutputNum: int
    audioNum: int
    buildDay: str
    channelNum: int
    detail: str
    diskNum: int
    name: str
    type: str
    wifi: bool
    B485: int
    exactType: str
    serial: str
    pakSuffix: str


@dataclass
class TimeValue:
    """Time Value"""

    year: int
    mon: int
    day: int
    hour: int
    min: int
    sec: int

    def as_datetime(self):
        """convert to datetime"""
        return datetime.datetime(
            self.year, self.mon, self.day, self.hour, self.min, self.sec
        )

    @classmethod
    def from_datetime(cls, value: datetime):
        """Create TimeValue from datetime"""
        return cls(
            value.year, value.month, value.day, value.hour, value.minute, value.second
        )


class TimeValueType(TypedDict, total=False):
    """Time Value"""

    year: int
    mon: int
    day: int
    hour: int
    min: int
    sec: int


class DaylightSavingsTimeInfo(TypedDict):
    """Daylight Savings Time Info"""

    enable: int
    endMonth: int
    endWeek: int
    endWeekday: int
    endHour: int
    endMin: int
    endSec: int
    offset: int
    startMon: int
    startWeek: int
    startWeekday: int
    startHour: int
    startMin: int
    startSec: int


class HourFormats(IntEnum):
    """Hour Format"""

    TWENTYFOUR = 0
    TWELVE = 1


class TimeValueInfo(TimeValueType):
    """Time Value with additional info"""

    timeFmt: str
    timeZone: int
    """Note: this is the offset to get GMT from localtime not the offset from GMT, i.e. -5GMT(ETD) is 18000 """
    hourFmt: int


class System:
    """System Commands Mixin"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__timeinfo: TimeValueInfo | None = None
        self.__time: datetime.datetime | None = None
        self.__abilities: Abilities | None = None

        if isinstance(self, connection.Connection):
            self._disconnect_callbacks.append(self.__clear)

    def __clear(self):
        self.__abilities = None
        self.__timeinfo = None
        self.__time = None

    async def get_ability(self, username: str | None = None):
        """Get User Permisions"""

        if username is None:
            self.__abilities = None

        Command = GetAbilitiesCommand
        if isinstance(self, connection.Connection):
            responses = async_trap_errors(
                self._execute(Command(User(username) if username else None))
            )

            result = await anext(
                amap(Command.get_value, afilter(
                    Command.is_response, responses)),
                None,
            )

            if result:
                abilities = Abilities(result)
                if username is None:
                    self.__abilities = abilities
                return abilities

        return Abilities({})

    async def _ensure_abilities(self):
        if self.__abilities:
            return self.__abilities
        return await self.get_ability()

    async def get_device_info(self):
        """Get Device Information"""

        Command = GetDeviceInfoCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(Command()))
        else:
            return None

        result = await anext(
            amap(Command.get_value, afilter(Command.is_response, responses)),
            None,
        )

        return result

    async def get_time(self):
        """Get Device Time Information"""

        self.__timeinfo = None
        self.__time = None

        Command = GetTimeCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(Command()))
        else:
            return None

        result = await anext(
            amap(Command.get_value, afilter(Command.is_response, responses)),
            None,
        )

        if result:
            self.__timeinfo = result["Time"]
            self.__time = as_dateime(result["Time"], tzinfo=get_tzinfo(result))

        return self.__time

    async def _ensure_time(self):
        if self.__time:
            return self.__time
        return await self.get_time()

    async def get_time_info(self):
        """Get DST Info"""
        await self._ensure_time()
        return self.__timeinfo

    async def reboot(self):
        """Reboot device"""

        Command = RebootCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(Command()))
        else:
            return False

        await alist(responses)  # eat all results looking for errors
        return True


class GetAbilityResponseValue(TypedDict):
    """Get Abilities Resposne Value"""

    Ability: dict


@dataclass
class UserInfoRequestParameter:
    """User Info Request Parameter"""

    User: User


class GetAbilitiesCommand(CommandRequestWithParam[UserInfoRequestParameter]):
    """Get Abilities"""

    COMMAND: Final = "GetAbility"
    RESPONSE: Final = "Ability"

    def __init__(
        self,
        user: User | None = None,
        action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    ) -> None:
        super().__init__(
            type(self).COMMAND,
            action,
            UserInfoRequestParameter(user or User("null")),
        )

    @classmethod
    def is_response(  # pylint: disable=arguments-differ
        cls, value: any
    ) -> TypeGuard[CommandResponseValue[GetAbilityResponseValue]]:
        """Is response a search result"""
        return cls._is_response(value, command=cls.COMMAND) and cls._is_typed_value(
            value, cls.RESPONSE, GetAbilityResponseValue
        )

    @classmethod
    def get_value(cls, value: CommandResponseValue[GetAbilityResponseValue]):
        """Get Response Value"""
        return cls._get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]


class GetDeviceInfoResponseValueType(TypedDict):
    """Get Device Info Response Value"""

    DevInfo: DeviceInfoType


class GetDeviceInfoCommand(CommandRequest):
    """Get Device Info"""

    COMMAND: Final = "GetDevInfo"
    RESPONSE: Final = "DevInfo"

    def __init__(
        self, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY
    ) -> None:
        super().__init__(type(self).COMMAND, action)

    @classmethod
    def is_response(  # pylint: disable=arguments-differ
        cls, value: any
    ) -> TypeGuard[CommandResponseValue[GetDeviceInfoResponseValueType]]:
        """Is response a search result"""
        return super().is_response(
            value, command=cls.COMMAND
        ) and super()._is_typed_value(
            value, cls.RESPONSE, GetDeviceInfoResponseValueType
        )

    @classmethod
    def get_value(cls, value: CommandResponseValue[GetDeviceInfoResponseValueType]):
        """Get Response Value"""
        return super().get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]


class GetTimeCommandResponseValueType(TypedDict, total=False):
    """Get Time Response Value"""

    Dst: DaylightSavingsTimeInfo
    Time: TimeValueInfo


class GetTimeCommand(CommandRequest):
    """Get Time"""

    COMMAND: Final = "GetTime"
    RESPONSE: Final = "Time"

    def __init__(
        self, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY
    ) -> None:
        super().__init__(type(self).COMMAND, action)

    @classmethod
    def is_response(  # pylint: disable=arguments-differ
        cls, value: any
    ) -> TypeGuard[CommandResponseValue[GetTimeCommandResponseValueType]]:
        """Is response a search result"""
        return cls._is_response(value, command=cls.COMMAND) and cls._is_typed_value(
            value, cls.RESPONSE, GetTimeCommandResponseValueType
        )


@dataclass
class _DstPoint:

    month: int
    week: int
    weekday: int
    hour: int
    minute: int
    second: int

    def __post_init__(self):
        self._cache: dict[int, datetime.datetime] = {}

    def as_datetime(self, year: int):
        """datetime"""

        if year in self._cache:
            return self._cache[year]

        value = datetime.datetime(
            year, self.month, 1, self.hour, self.minute, self.second
        )
        value += datetime.timedelta(weeks=self.week, days=-value.weekday())
        return self._cache.setdefault(
            year, value + datetime.timedelta(days=self.weekday)
        )


_ZERO = datetime.timedelta(0)


class _timezone(datetime.tzinfo):
    _cache: ClassVar[dict[tuple[int, int], _timezone]] = {}

    def __init__(self, dst_info: DaylightSavingsTimeInfo, time_info: TimeValueInfo):
        self._hour_offset = datetime.timedelta(hours=dst_info["offset"])
        self._std_offset = -datetime.timedelta(seconds=time_info["timeZone"])

        self._start = _DstPoint(
            dst_info["startMon"],
            dst_info["startWeek"],
            dst_info["startWeekday"],
            dst_info["startHour"],
            dst_info["startMin"],
            dst_info["startSec"],
        )
        self._end = _DstPoint(
            dst_info["endMon"],
            dst_info["endWeek"],
            dst_info["endWeekday"],
            dst_info["endHour"],
            dst_info["endMin"],
            dst_info["endSec"],
        )

    @classmethod
    def get_or_create(cls, dst_info: DaylightSavingsTimeInfo, time_info: TimeValueInfo):
        """Get existing or create new"""
        return cls._cache.setdefault(
            (dst_info["enable"], time_info["timeZone"]
             ), _timezone(dst_info, time_info)
        )

    def tzname(self, __dt: datetime.datetime | None):
        return None

    def utcoffset(self, __dt: datetime.datetime | None):
        if __dt is None:
            return self._dst_offset
        if __dt.tzinfo is not None:
            if __dt.tzinfo is not self:
                return __dt.utcoffset()
            __dt = __dt.replace(tzinfo=None)
        if (
            self._start.as_datetime(__dt.year)
            <= __dt
            < self._end.as_datetime(__dt.year)
        ):
            return self._std_offset + self._hour_offset
        return self._std_offset

    def dst(self, __dt: datetime.datetime | None):
        if __dt is None:
            return self._hour_offset
        if __dt.tzinfo is not None:
            if __dt.tzinfo is not self:
                return __dt.dst()
            __dt = __dt.replace(tzinfo=None)
        if (
            self._start.as_datetime(__dt.year)
            <= __dt
            < self._end.as_datetime(__dt.year)
        ):
            return self._hour_offset
        return _ZERO


def get_tzinfo(info: GetTimeCommandResponseValueType) -> datetime.tzinfo:
    """Get tzinfo"""

    if "Dst" in info:
        return _timezone.get_or_create(info["Dst"], info["Time"])
    return datetime.timezone(datetime.timedelta(seconds=-info["Time"]["timeZone"]))


def as_dateime(value: TimeValueType, *, tzinfo: datetime.tzinfo | None = None):
    """TimeValue to datetime"""

    return datetime.datetime(
        value["year"],
        value["mon"],
        value["day"],
        value["hour"],
        value["min"],
        value["sec"],
        tzinfo=tzinfo,
    )


class RebootCommand(CommandRequest):
    """Reboot Command"""

    COMMAND: Final = "Reboot"

    def __init__(
        self, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY
    ) -> None:
        super().__init__(type(self).COMMAND, action)
