"""System Typings"""


from enum import IntEnum
from typing import TypedDict


class UserInfo(TypedDict):
    """User Info"""

    userName: str


class DeviceVersions(TypedDict):
    """Device Version Info"""

    cfgVer: str
    firmVer: str
    hardVer: str
    frameworkVer: str


class DeviceInfo(DeviceVersions):
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
