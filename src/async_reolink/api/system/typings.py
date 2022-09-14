"""System typings"""

from abc import ABC
from datetime import date, datetime, timedelta, timezone
from enum import IntEnum, auto
from typing import Annotated, Protocol

from ..typings import DateTimeValue, TimeValue, WeekDays


class DeviceInfo(Protocol):
    """Device Info"""

    class IO(Protocol):
        """I/O"""

        inputs: int
        outputs: int

    class Version(Protocol):
        """Version"""

        firmware: str
        framework: str
        hardware: str
        config: str

    io: IO
    audio_sources: int
    build_day: str
    channels: int
    detail: str
    disks: int
    version: Version
    model: str
    name: str
    type: str
    wifi: bool
    # B845: int
    exact_type: str
    serial: str
    pak_suffix: str


class HourFormat(IntEnum):
    """Hour Format"""

    HR_24 = 0
    HR_12 = auto()


class DaylightSavingsTimeInfo(Protocol):
    """Daylight Savings Time info"""

    enabled: bool
    hour_offset: Annotated[int, range(1, 2)]

    class TimeInfo(TimeValue, ABC):
        """Time info"""

        month: Annotated[int, range(1, 12)]
        week: Annotated[int, range(1, 5)]
        weekday: WeekDays

        def to_datetime(self, year: int):
            """get date time for dst point with given year"""
            _date = date(year, self.month, 1)
            delta = timedelta(weeks=self.week, days=int(self.week))
            delta -= timedelta(days=_date.weekday())
            _date += delta
            return datetime.combine(_date, self.to_time())

    start: TimeInfo
    end: TimeInfo


class TimeInfo(DateTimeValue, ABC):
    """Device Time Info"""

    hour_format: HourFormat
    timezone_offset: int

    def to_datetime(self):
        notz = super().to_datetime()
        return notz.astimezone(timezone(timedelta(seconds=self.timezone_offset)))