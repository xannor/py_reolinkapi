"""Abilities Typings"""

from enum import IntEnum
from typing import TypedDict

from .base import Ability
from .channel import ChannelAbilities
from .support import SupportAbilities

_Abilities = TypedDict("_Abilities", {"3g": Ability})


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


class AlarmAbilities(TypedDict):
    """Alarm Abilities"""

    alarmHddErr: Ability
    """hint: BoolAbilityVer"""
    alarmHddFull: Ability
    """hint: BoolAbilityVer"""
    alarmDisconnect: Ability
    """hint: BoolAbilityVer"""
    alarmIpConfict: Ability
    """hint: BoolAbilityVer"""
    alarmAudio: Ability
    """hint: BoolAbilityVer"""


class FTPAbilities(TypedDict):
    """FTP Abilities"""

    ftpTest: Ability
    """hint: BoolAbilityVer"""
    ftpSubStream: Ability
    """hint: BoolAbilityVer"""
    ftpExtStream: Ability
    """hint: BoolAbilityVer"""
    ftpPic: Ability
    """hint: BoolAbilityVer"""
    ftpAutoDir: Ability
    """hint: BoolAbilityVer"""


class RecordAbilities(TypedDict):
    """Record Abilities"""

    recOverWrite: Ability
    """hint: BoolAbilityVer"""
    recPackDuration: Ability
    """hint: BoolAbilityVer"""
    recPreRecord: Ability
    """hint: BoolAbilityVer"""
    recExtensionTimeList: Ability
    """hint: BoolAbilityVer"""


class Abilities(SupportAbilities, AlarmAbilities, FTPAbilities, RecordAbilities):
    """Abilities"""

    abilityChn: list[ChannelAbilities]
    hourFmt: Ability
    """hint: BoolAbilityVer"""
    time: Ability
    """hint: TimeAbilityVers"""
    tvSystem: Ability
    """hint: BoolAbilityVer"""
    display: Ability
    """hint: BoolAbilityVer"""
    ipcManager: Ability
    """hint: BoolAbilityVer"""
    devInfo: Ability
    """hint: BoolAbilityVer"""
    autoMaint: Ability
    """hint: BoolAbilityVer"""
    restore: Ability
    """hint: BoolAbilityVer"""
    reboot: Ability
    """hint: BoolAbilityVer"""
    log: Ability
    """hint: BoolAbilityVer"""
    performance: Ability
    """hint: BoolAbilityVer"""
    upgrade: Ability
    """hint: UpgradeAbilityVers"""
    importCfg: Ability
    """hint: BoolAbilityVer"""
    exportCfg: Ability
    """hint: BoolAbilityVer"""
    disk: Ability
    """hint: BoolAbilityVer"""
    sdCard: Ability
    """hint: BoolAbilityVer"""
    devName: Ability
    """hint: BoolAbilityVer"""
    auth: Ability
    """hint: BoolAbilityVer"""
    user: Ability
    """hint: BoolAbilityVer"""
    online: Ability
    """hint: BoolAbilityVer"""
    rtsp: Ability
    """hint: BoolAbilityVer"""
    rtmp: Ability
    """hint: BoolAbilityVer"""
    ddns: Ability
    """hint: DDnsAbilityVers"""
    ddnsCfg: Ability
    """hint: BoolAbilityVer"""
    email: Ability
    """hint: EmailAbilityVers"""
    emailSchedule: Ability
    """hint: BoolAbilityVer"""
    upnp: Ability
    """hint: BoolAbilityVer"""
    onvif: Ability
    """hint: BoolAbilityVer"""
    ntp: Ability
    """hint: BoolAbilityVer"""
    mediaPort: Ability
    """hint: BoolAbilityVer"""
    http: Ability
    """hint: BoolAbilityVer"""
    https: Ability
    """hint: BoolAbilityVer"""
    http_flv: Ability
    """hint: BoolAbilityVer"""
    p2p: Ability
    """hint: BoolAbilityVer"""
    mediaPort: Ability
    """hint: BoolAbilityVer"""
    localLink: Ability
    """hint: BoolAbilityVer"""
    pppoe: Ability
    """hint: BoolAbilityVer"""
    Wifi: Ability
    """hint: BoolAbilityVer"""
    Push: Ability
    """hint: BoolAbilityVer"""
    pushSchedule: Ability
    """hint: BoolAbilityVer"""
    Talk: Ability
    """hint: BoolAbilityVer"""
    ledControl: Ability
    """hint: BoolAbilityVer"""
    disableAutoFocus: Ability
    """hint: BoolAbilityVer"""
    videoClip: Ability
    """hint: VideoClipAbilityVers"""
    cloudStorage: Ability
    """hint: BoolAbilityVer"""
    scheduleVersion: Ability
    """hint: VersionAbilityVers"""
    customAudio: Ability
    """hint: BoolAbilityVer"""
    wifiTest: Ability
    """hint: BoolAbilityVer"""
    simModule: Ability
    """hint: BoolAbilityVer"""
    dateFormat: Ability
    """hint: BoolAbilityVer"""
    emailInterval: Ability
    """hint: BoolAbilityVer"""
    showQrCode: Ability
    """hint: BoolAbilityVer"""
