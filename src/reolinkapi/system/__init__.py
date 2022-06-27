"""System"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from typing import ClassVar, Final, Iterable, TypedDict

from ..commands import COMMAND_RESPONSE_VALUE, CommandRequest, CommandRequestTypes, CommandRequestWithParam, CommandResponse, create_is_command, create_value_has_key, isvalue

from .abilities import Abilities, AbilitiesType

from .. import connection

@dataclass
class UserInfo:
    """User Info"""

    userName: str

class DeviceVersions(TypedDict):
    """Device Version Info"""

    cfgVer: str
    firmVer: str
    hardVer: str
    frameworkVer: str


class DeviceInfoType(DeviceVersions):
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


class TimeValue(TypedDict, total=False):
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


class TimeValueInfo(TimeValue):
    """Time Value with additional info"""

    timeFmt: str
    timeZone: int
    """Note: this is the offset to get GMT from localtime not the offset from GMT, i.e. -5GMT(ETD) is 18000 """
    hourFmt: int

class System:
    """System Commands Mixin"""

    def __init__(self) -> None:
        self.__timeinfo: TimeValueInfo | None = None
        self.__time: datetime | None = None

        if isinstance(self, connection.Connection):
            self._disconnect_callbacks.append(self.__clear)

    def __clear(self):
        self.__timeinfo = None
        self.__time = None

    async def get_ability(self, username: str | None = None):
        """Get User Permisions"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(GetAbilityRequest(username))
        else:
            return None

        return next(GetAbilityRequest.get_responses(responses), None)

    async def get_device_info(self):
        """Get Device Information"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(GetDeviceInfoRequest())
        else:
            return None

        return next(GetDeviceInfoRequest.get_responses(responses), None)

    async def get_time(self):
        """Get Device Time Information"""

        self.__clear()
        if isinstance(self, connection.Connection):
            responses = await self._execute(GetTimeRequest())
        else:
            return None
        time = next(GetTimeRequest.get_responses(responses), None)
        if time is not None:
            self.__timeinfo = time["Time"]
            self.__time = as_dateime(
                time["Time"], tzinfo=get_tzinfo(time)
            )

        return self.__time

    async def _ensure_time(self):
        if self.__time is None:
            return await self.get_time()
        return self.__time

    async def get_time_info(self):
        """Get DST Info"""
        await self.get_time()
        return self.__timeinfo

class GetAbilityResponseValue(TypedDict):
    """Get Abilities Resposne Value"""

    Ability: dict

@dataclass
class UserInfoRequestParameter:
    """User Info Request Parameter"""

    User: UserInfo

class GetAbilityRequest(CommandRequestWithParam[UserInfoRequestParameter]):
    """Get Abilities"""

    COMMAND:Final = "GetAbility"
    RESPONSE:Final = "Ability"

    def __init__(self, user:UserInfo|None=None, action:CommandRequestTypes=CommandRequestTypes.VALUE_ONLY)->None:
        super().__init__(type(self).COMMAND, action, UserInfoRequestParameter(user or UserInfo("null")))

    @classmethod
    def get_responses(cls, responses: Iterable[CommandResponse]):
        """get responses"""
        return map(
            lambda response: response[COMMAND_RESPONSE_VALUE][cls.RESPONSE],
            filter(
                _isAbilities,
                filter(
                    isvalue,
                    filter(_isAbilitiesCmd, responses),
                ),
            ),
        )


_isAbilitiesCmd = create_is_command(GetAbilityRequest.COMMAND)

_isAbilities = create_value_has_key(GetAbilityRequest.RESPONSE, GetAbilityResponseValue)

class GetDeviceInfoResponseValue(TypedDict):
    """Get Device Info Response Value"""

    DevInfo: DeviceInfoType

class GetDeviceInfoRequest(CommandRequest):
    """Get Device Info"""

    COMMAND: Final = "GetDevInfo"
    RESPONSE: Final = "DevInfo"

    def __init__(self, action:CommandRequestTypes=CommandRequestTypes.VALUE_ONLY)->None:
        super().__init__(type(self).COMMAND, action)

    @classmethod
    def get_responses(cls, responses: Iterable[CommandResponse]):
        """"Get Responses"""
        return map(
            lambda response: _make_abilities(response[COMMAND_RESPONSE_VALUE][cls.RESPONSE]),
            filter(
                _isDevInfo,
                filter(
                    isvalue,
                    filter(
                        _isDevInfoCmd,
                        responses
                    )
                )
            )
        )

def _make_abilities(abilities:dict|None):
    return Abilities(abilities) if abilities else None

_isDevInfoCmd = create_is_command(GetDeviceInfoRequest.COMMAND)

_isDevInfo = create_value_has_key(GetDeviceInfoRequest.RESPONSE, GetDeviceInfoResponseValue)

class GetTimeCommandResponseValue(TypedDict, total=False):
    """Get Time Response Value"""

    Dst: DaylightSavingsTimeInfo
    Time: TimeValueInfo

class GetTimeRequest(CommandRequest):
    """Get Time"""

    COMMAND: Final = "GetTime"
    RESPONSE: Final = "Time"

    def __init__(self, action:CommandRequestTypes=CommandRequestTypes.VALUE_ONLY)->None:
        super().__init__(type(self).COMMAND, action)

    @classmethod
    def get_responses(cls, responses: Iterable[CommandResponse]):
        """"Get Responses"""
        return map(
            lambda response: response[COMMAND_RESPONSE_VALUE][cls.RESPONSE],
            filter(
                _isTime,
                filter(
                    isvalue,
                    filter(
                        _isTimeCmd,
                        responses
                    )
                )
            )
        )

_isTimeCmd = create_is_command(GetTimeRequest.COMMAND)

_isTime = create_value_has_key(GetTimeRequest.RESPONSE, GetTimeCommandResponseValue)

def as_time_value(value: datetime.datetime):
    """datetime to TimeValue"""

    return TimeValue(
        year=value.year,
        mon=value.month,
        day=value.day,
        hour=value.hour,
        min=value.minute,
        sec=value.second,
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
            (dst_info["enable"], time_info["timeZone"]), _timezone(dst_info, time_info)
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


def get_tzinfo(info: GetTimeCommandResponseValue) -> datetime.tzinfo:
    """Get tzinfo"""

    if "Dst" in info:
        return _timezone.get_or_create(info["Dst"], info["Time"])
    return datetime.timezone(datetime.timedelta(seconds=-info["Time"]["timeZone"]))


def as_dateime(value: TimeValue, *, tzinfo: datetime.tzinfo | None = None):
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
