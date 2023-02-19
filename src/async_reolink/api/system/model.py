"""System Models"""

from abc import ABC
from datetime import date, datetime, timedelta, timezone
from typing import Final, TypeVar, final

from .capabilities import Capability, Permissions

from ..typing import WeekDays

from . import typing
from .. import model


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
class _DeviceInfo(typing.DeviceInfo):
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
        return None

    def __len__(self):
        return 0


NO_DEVICEINFO: Final = _DeviceInfo()


class DaylightSavingsTimeInfo(typing.DaylightSavingsTimeInfo, ABC):
    """Daylight Savings Time Info"""

    class TimeInfo(typing.DaylightSavingsTimeInfo.TimeInfo, model.SimpleTime, ABC):
        """Time Info"""

        # pylint: disable=no-self-argument
        def to_datetime(__time: typing.DaylightSavingsTimeInfo.TimeInfo, year: int):
            """get date time for dst point with given year"""
            _date = date(year, __time.month, 1)
            delta = timedelta(weeks=__time.week, days=int(__time.week))
            delta -= timedelta(days=_date.weekday())
            if __time.weekday != WeekDays.MONDAY:
                delta += timedelta(days=__time.weekday.value - WeekDays.MONDAY.value)
            _date += delta
            if isinstance(__time, TimeInfo):
                _time = __time.to_time()
            else:
                _time = model.SimpleTime.to_time(__time)
            return datetime.combine(_date, _time)

    start: TimeInfo
    end: TimeInfo


class TimeInfo(typing.TimeInfo, model.DateTime, ABC):
    """Time Info"""

    # pylint: disable=no-self-argument
    def to_datetime(__time: typing.TimeInfo):
        """Convert Time Info to datetime with timezone"""

        notz = model.DateTime.to_datetime(__time)
        # Reolink does positive offest python expects a negative one
        return notz.astimezone(timezone(timedelta(seconds=-__time.timezone_offset)))
