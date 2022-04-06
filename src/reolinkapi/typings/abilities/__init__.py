"""Abilities Typings"""

from enum import IntEnum
from typing import Annotated, TypedDict

from .base import Ability, BooleanAbilityVers, VideoClipAbilityVers
from .channel import All as ChannelAbilities
from .support import SupportAbilities


class TimeAbilityVers(IntEnum):
    """Time Ability Values"""

    NONE = 0
    SUNDAY = 1
    ANYDAY = 2


class UpgradeAbilityVers(IntEnum):
    """Upgrade Ability Values"""

    NONE = 0
    MANUAL = 1
    ONLINE = 2


class DDnsAbilityVers(IntEnum):
    """DDNS Ability Values"""

    NONE = 0
    SWANN = 1
    THREE322 = 2
    DYNDNS = 3
    SWANN_3322 = 4
    SWANN_DYNDNS = 5
    DYNDNS_3322 = 6
    SWAN_DYNDNS_3322 = 7
    NOIP = 8
    DYNDNS_NOIP = 9


class EmailAbilityVers(IntEnum):
    """Email Ability Values"""

    NONE = 0
    JPEG = 1
    VIDEO_JPEG = 2
    VIDEO_JPEG_NICK = 3


class VersionAbilityVers(IntEnum):
    """Version Ability Values"""

    BASIC = 0
    V20 = 1


class AlarmAbilities(TypedDict, total=False):
    """Alarm Abilities"""

    alarmHddErr: Annotated[Ability, BooleanAbilityVers]
    alarmHddFull: Annotated[Ability, BooleanAbilityVers]
    alarmDisconnect: Annotated[Ability, BooleanAbilityVers]
    alarmIpConfict: Annotated[Ability, BooleanAbilityVers]
    alarmAudio: Annotated[Ability, BooleanAbilityVers]


class FTPAbilities(TypedDict, total=False):
    """FTP Abilities"""

    ftpTest: Annotated[Ability, BooleanAbilityVers]
    ftpSubStream: Annotated[Ability, BooleanAbilityVers]
    ftpExtStream: Annotated[Ability, BooleanAbilityVers]
    ftpPic: Annotated[Ability, BooleanAbilityVers]
    ftpAutoDir: Annotated[Ability, BooleanAbilityVers]


class RecordAbilities(TypedDict, total=False):
    """Record Abilities"""

    recOverWrite: Annotated[Ability, BooleanAbilityVers]
    recPackDuration: Annotated[Ability, BooleanAbilityVers]
    recPreRecord: Annotated[Ability, BooleanAbilityVers]
    recExtensionTimeList: Annotated[Ability, BooleanAbilityVers]


class Abilities(
    AlarmAbilities,
    FTPAbilities,
    RecordAbilities,
    SupportAbilities,
    total=False,
):
    """Abilities"""

    abilityChn: list[ChannelAbilities]
    hourFmt: Annotated[Ability, BooleanAbilityVers]
    time: Annotated[Ability, TimeAbilityVers]
    tvSystem: Annotated[Ability, BooleanAbilityVers]
    display: Annotated[Ability, BooleanAbilityVers]
    ipcManager: Annotated[Ability, BooleanAbilityVers]
    devInfo: Annotated[Ability, BooleanAbilityVers]
    autoMaint: Annotated[Ability, BooleanAbilityVers]
    restore: Annotated[Ability, BooleanAbilityVers]
    reboot: Annotated[Ability, BooleanAbilityVers]
    log: Annotated[Ability, BooleanAbilityVers]
    performance: Annotated[Ability, BooleanAbilityVers]
    upgrade: Annotated[Ability, UpgradeAbilityVers]
    importCfg: Annotated[Ability, BooleanAbilityVers]
    exportCfg: Annotated[Ability, BooleanAbilityVers]
    disk: Annotated[Ability, BooleanAbilityVers]
    sdCard: Annotated[Ability, BooleanAbilityVers]
    devName: Annotated[Ability, BooleanAbilityVers]
    auth: Annotated[Ability, BooleanAbilityVers]
    user: Annotated[Ability, BooleanAbilityVers]
    online: Annotated[Ability, BooleanAbilityVers]
    rtsp: Annotated[Ability, BooleanAbilityVers]
    rtmp: Annotated[Ability, BooleanAbilityVers]
    ddns: Annotated[Ability, DDnsAbilityVers]
    ddnsCfg: Annotated[Ability, BooleanAbilityVers]
    email: Annotated[Ability, EmailAbilityVers]
    emailSchedule: Annotated[Ability, BooleanAbilityVers]
    upnp: Annotated[Ability, BooleanAbilityVers]
    onvif: Annotated[Ability, BooleanAbilityVers]
    ntp: Annotated[Ability, BooleanAbilityVers]
    mediaPort: Annotated[Ability, BooleanAbilityVers]
    http: Annotated[Ability, BooleanAbilityVers]
    https: Annotated[Ability, BooleanAbilityVers]
    http_flv: Annotated[Ability, BooleanAbilityVers]
    p2p: Annotated[Ability, BooleanAbilityVers]
    mediaPort: Annotated[Ability, BooleanAbilityVers]
    localLink: Annotated[Ability, BooleanAbilityVers]
    pppoe: Annotated[Ability, BooleanAbilityVers]
    Wifi: Annotated[Ability, BooleanAbilityVers]
    Push: Annotated[Ability, BooleanAbilityVers]
    pushSchedule: Annotated[Ability, BooleanAbilityVers]
    Talk: Annotated[Ability, BooleanAbilityVers]
    ledControl: Annotated[Ability, BooleanAbilityVers]
    disableAutoFocus: Annotated[Ability, BooleanAbilityVers]
    videoClip: Annotated[Ability, VideoClipAbilityVers]
    cloudStorage: Annotated[Ability, BooleanAbilityVers]
    scheduleVersion: Annotated[Ability, VersionAbilityVers]
    customAudio: Annotated[Ability, BooleanAbilityVers]
    wifiTest: Annotated[Ability, BooleanAbilityVers]
    simModule: Annotated[Ability, BooleanAbilityVers]
    dateFormat: Annotated[Ability, BooleanAbilityVers]
    emailInterval: Annotated[Ability, BooleanAbilityVers]
    showQrCode: Annotated[Ability, BooleanAbilityVers]


ABILITIES_3G = "3g"
