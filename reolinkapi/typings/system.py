"""System Typings"""


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
