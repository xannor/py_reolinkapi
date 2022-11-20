"""System typings"""

from abc import ABC
from enum import Enum, auto
from typing import Annotated, Protocol

from ..typing import DateTime, SimpleTime, WeekDays


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


class StorageTypes(Enum):
    """Storage Types"""

    HDD = auto()
    SDC = auto()


class StorageInfo(Protocol):
    """HDD Info"""

    id: int
    capacity: int
    formatted: bool
    mounted: bool
    free_space: int
    type: StorageTypes


class HourFormat(Enum):
    """Hour Format"""

    HR_24 = auto()
    HR_12 = auto()


class DaylightSavingsTimeInfo(Protocol):
    """Daylight Savings Time info"""

    enabled: bool
    hour_offset: Annotated[int, range(1, 2)]

    class TimeInfo(SimpleTime, Protocol):
        """Time info"""

        month: Annotated[int, range(1, 12)]
        week: Annotated[int, range(1, 5)]
        weekday: WeekDays

    start: TimeInfo
    end: TimeInfo


class TimeInfo(DateTime, Protocol):
    """Device Time Info"""

    hour_format: HourFormat
    timezone_offset: int
