"""System Commands"""


from abc import ABC
from datetime import datetime, timedelta, timezone, tzinfo
from typing import Final, Mapping, Protocol, TypeGuard

from ..connection.typing import CommandFactory as WithCommandFactory
from ..connection.typing import CommandRequest, CommandResponse
from .capabilities import Capabilities
from .typing import DaylightSavingsTimeInfo, DeviceInfo, StorageInfo, TimeInfo


class GetAbilitiesRequest(CommandRequest, Protocol):
    """Get Capabilities"""

    user_name: str | None


class GetAbilitiesResponse(CommandResponse, Protocol):
    """Get Capabilities Response"""

    capabilities: Capabilities


class GetDeviceInfoRequest(CommandRequest, Protocol):
    """Get Device Info"""


class GetDeviceInfoResponse(CommandResponse, Protocol):
    """Get Device Info Response"""

    info: DeviceInfo


class GetTimeRequest(CommandRequest, Protocol):
    """Get Time"""


_ZERO: Final = timedelta(0)


class _timezone(tzinfo):
    _cache: dict[(bool, int), "_timezone"] = {}
    __slots__ = ("_hr_chg", "_ofs", "_start", "_end", "_point_cache")

    @classmethod
    def get(cls, dst: DaylightSavingsTimeInfo, _time: TimeInfo):
        """get or create tinezone object"""
        key = (dst.enabled, _time.timezone_offset)
        if key in cls._cache:
            return cls._cache[key]

        return cls._cache.setdefault(key, _timezone(dst, _time))

    def __init__(self, dst: DaylightSavingsTimeInfo, _time: TimeInfo) -> None:
        self._hr_chg = timedelta(hours=dst.hour_offset)
        self._ofs = timedelta(seconds=_time.timezone_offset)
        self._start = dst.start
        self._end = dst.end
        self._point_cache: dict[int, (datetime, datetime)] = {}

    def tzname(self, __dt: datetime | None) -> str | None:
        return None

    def _get_start_end(self, year: int):
        if year in self._point_cache:
            return self._point_cache[year]
        return self._point_cache.setdefault(
            year, (self._start.to_datetime(year), self._end.to_datetime(year))
        )

    def utcoffset(self, __dt: datetime | None) -> timedelta | None:
        if __dt is None:
            return self._ofs
        if __dt.tzinfo is not None:
            if __dt.tzinfo is not self:
                return __dt.utcoffset()
            __dt = __dt.replace(tzinfo=None)
        (start, end) = self._get_start_end(__dt.year)
        if start <= __dt < end:
            return self._ofs + self._hr_chg
        return self._ofs

    def dst(self, __dt: datetime | None) -> timedelta | None:
        if __dt is None:
            return self._hour_offset
        if __dt.tzinfo is not None:
            if __dt.tzinfo is not self:
                return __dt.dst()
            __dt = __dt.replace(tzinfo=None)
        (start, end) = self._get_start_end(__dt.year)
        if start <= __dt < end:
            return self._hr_chg
        return _ZERO


class GetTimeResponse(CommandResponse, ABC):
    """Get Time Response"""

    dst: DaylightSavingsTimeInfo
    time: TimeInfo

    def to_timezone(self) -> timezone:
        """Convert dst and time info into timezone"""
        return _timezone.get(self.dst, self.time)

    def to_datetime(self):
        """Get device time as full datetime and timezone"""
        return datetime.combine(
            self.time.to_date(), self.time.to_time(), self.to_timezone()
        )


class RebootRequest(CommandRequest, Protocol):
    """Reboot Request"""


class GetHddInfoRequest(CommandRequest, Protocol):
    """Get HDD Info Request"""


class GetHddInfoResponse(CommandResponse, Protocol):
    """Get HDD Info Response"""

    info: Mapping[int, StorageInfo]


class CommandFactory(WithCommandFactory, Protocol):
    """System Command Factory"""

    def create_get_capabilities_request(
        self, username: str | None
    ) -> GetAbilitiesRequest:
        """create GetAbilitiesRequest"""

    def is_get_capabilities_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetAbilitiesResponse]:
        """is GetAbilitiesResponse"""

    def create_get_device_info_request(self) -> GetDeviceInfoRequest:
        """create GetDeviceInfoRequest"""

    def is_get_device_info_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetDeviceInfoResponse]:
        """is GetDeviceInfoResponse"""

    def create_get_time_request(self) -> GetTimeRequest:
        """create GetTimeRequest"""

    def is_get_time_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetTimeResponse]:
        """is GetTimeResponse"""

    def create_reboot_request(self) -> RebootRequest:
        """create RebootRequest"""

    def create_get_hdd_info_request(self) -> GetHddInfoRequest:
        """create GetHddInfoRequest"""

    def is_get_hdd_info_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetHddInfoResponse]:
        """is GetHddInfoResponse"""