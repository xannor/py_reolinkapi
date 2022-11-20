"""Various Typings and TypeChecks"""

from __future__ import annotations
from datetime import date, datetime, time
from enum import Enum, auto
from typing import Annotated, Protocol


class size:  # pylint: disable=invalid-name
    """size limits"""

    def __init__(self, max: int, min: int = 0) -> None:  # pylint: disable=redefined-builtin
        self._max = max
        self._min = min

    def min(self):
        """minimum size"""
        return self._min

    @property
    def max(self):
        """maximum size"""
        return self._max


PercentValue = Annotated[int, range(0, 100)]
"""Integer represeting a percentage value, 0-100"""

MonthValue = Annotated[int, range(1, 12)]
"""Integer representing calendar months, 1-12"""

DaysValue = Annotated[int, range(1, 31)]
"""Integer representing calendar days, 1-31"""

HoursValue = Annotated[int, range(0, 23)]
"""Integer representing 24hr clock range, 0-23"""

MinutesValue = Annotated[int, range(0, 59)]
"""Integer representing clock minutes range, 0-59 """

SecondsValue = Annotated[int, range(0, 59)]
"""Integer representing clock seconds range, 0-59 """


class WeekDays(Enum):
    """Day of the week"""

    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()


class Date(Protocol):
    """Date Value"""

    year: int
    month: Annotated[int, range(1, 12)]
    day: Annotated[int, range(1, 31)]


class SimpleTime(Protocol):
    """Simple Time Value"""

    hour: Annotated[int, range(0, 23)]
    minute: Annotated[int, range(0, 59)]


class Time(SimpleTime, Protocol):
    """Time Value"""

    second: Annotated[int, range(0, 59)]


class DateTime(Date, Time, Protocol):
    """Date Time Value"""


class StreamTypes(Enum):
    """Stream Types"""

    MAIN = auto()
    SUB = auto()
    EXT = auto()
