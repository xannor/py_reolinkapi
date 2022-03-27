"""System Helpers"""
from __future__ import annotations
from dataclasses import dataclass
import datetime

from typing import ClassVar, Final, Iterable, TypedDict

from ..typings.commands import (
    COMMAND_RESPONSE_VALUE,
    CommandRequest,
    CommandRequestTypes,
    CommandRequestWithParam,
    CommandResponse,
)
from ..typings.system import (
    DaylightSavingsTimeInfo,
    DeviceInfo,
    TimeValue,
    TimeValueInfo,
    UserInfo,
)
from ..typings.abilities import Abilities
from ..helpers import commands as commandHelpers


class GetAbilityResponseValue(TypedDict):
    """Get Abilities Resposne Value"""

    Ability: Abilities


class UserInfoRequestParameter(TypedDict):
    """User Info Request Parameter"""

    User: UserInfo


GET_ABILITY_COMMAND: Final = "GetAbility"

_isAbilitiesCmd = commandHelpers.create_is_command(GET_ABILITY_COMMAND)

_isAbilities = commandHelpers.create_value_has_key("Ability", GetAbilityResponseValue)


def create_get_ability(
    username: str | None = None,
    _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
):
    """Create GetAbility Request"""
    return CommandRequestWithParam(
        cmd=GET_ABILITY_COMMAND,
        action=_type,
        param=UserInfoRequestParameter(User=UserInfo(userName=username or "null")),
    )


def get_ability_responses(responses: Iterable[CommandResponse]):
    """Get GetAbility Responses"""

    return map(
        lambda response: response[COMMAND_RESPONSE_VALUE]["Ability"],
        filter(
            _isAbilities,
            filter(
                commandHelpers.isvalue,
                filter(_isAbilitiesCmd, responses),
            ),
        ),
    )


class GetDeviceInfoResponseValue(TypedDict):
    """Get Device Info Response Value"""

    DevInfo: DeviceInfo


DEVICE_INFO_COMMAND: Final = "GetDevInfo"

_isDevInfoCmd = commandHelpers.create_is_command(DEVICE_INFO_COMMAND)

_isDevInfo = commandHelpers.create_value_has_key("DevInfo", GetDeviceInfoResponseValue)


def create_get_device_info(
    _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
):
    """Create DeviceInfo Request"""
    return CommandRequestWithParam(cmd=DEVICE_INFO_COMMAND, action=_type)


def get_devinfo_responses(responses: Iterable[CommandResponse]):
    """Get DeviceInfo Responses"""

    return map(
        lambda response: response[COMMAND_RESPONSE_VALUE]["DevInfo"],
        filter(
            _isDevInfo,
            filter(
                commandHelpers.isvalue,
                filter(_isDevInfoCmd, responses),
            ),
        ),
    )


GET_TIME_COMMAND: Final = "GetTime"


def create_get_time(
    _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
):
    """Create Get Time Request"""

    return CommandRequest(cmd=GET_TIME_COMMAND, action=_type)


class GetTimeCommandResponseValue(TypedDict, total=False):
    """Get Time Response Value"""

    Dst: DaylightSavingsTimeInfo
    Time: TimeValueInfo


_isTimeCmd = commandHelpers.create_is_command(GET_TIME_COMMAND)

_isTime = commandHelpers.create_value_has_key("Time", GetTimeCommandResponseValue)


def get_time_responses(responses: Iterable[CommandResponse]):
    """Get Time Responses"""

    return map(
        lambda response: response[COMMAND_RESPONSE_VALUE],
        filter(
            _isTime,
            filter(
                commandHelpers.isvalue,
                filter(_isTimeCmd, responses),
            ),
        ),
    )


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
