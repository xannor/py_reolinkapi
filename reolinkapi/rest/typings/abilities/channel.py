"""Channel Abilities"""

from enum import IntEnum
from typing import TypedDict

from .base import Ability


class OsdAbilityVers(IntEnum):
    """Osd Ability Values"""

    NONE = 0
    SUPPORTED = 1
    DISTINCT = 2


class LiveAbilityVers(IntEnum):
    """Live Ability Values"""

    NONE = 0
    MAIN_EXTERN_SUB = 1
    MAIN_SUB = 2


class FtpAbilityVers(IntEnum):
    """FTP Ability Values"""

    NONE = 0
    STREAM = 1
    JPEG_STREAM = 2
    MODE = 3
    JPEG_STREAM_MODE = 4
    STREAM_MODE_TYPE = 5
    JPEG_STREAM_MODE_TYPE = 6


class EncodingTypeAbilityVers(IntEnum):
    """Encoding Type Ability Values"""

    H264 = 0
    H265 = 1


class FloodLightAbilitVers(IntEnum):
    """Flood Light Ability Vers"""

    NONE = 0
    WHITE = 1
    AUTO = 2


class PTZTypeAbilityVers(IntEnum):
    """PTZ Type Ability Values"""

    NONE = 0
    AF = 1
    PTZ = 2
    PT = 3
    BALL = 4
    PTZ_NO_SPEED = 5


class PTZControlAbilityVers(IntEnum):
    """PTZ Control Ability Values"""

    NONE = 0
    ZOOM = 1
    ZOOM_FOCUS = 2


class PTZDirectionAbilityVers(IntEnum):
    """PTZ Direction Ability Values"""

    AUTOSCAN_8 = 0
    NO_AUTOACAN_4 = 1


class PTZAbilities(TypedDict):
    """PTZ Abilities"""

    ptzType: Ability
    """hint: PTZTypeAbilityVers"""
    ptzCtrl: Ability
    """hint: PTZControlAbilityVers"""
    ptzPreset: Ability
    """hint: BoolAbilityVer"""
    ptzPatrol: Ability
    """hint: BoolAbilityVer"""
    ptzTattern: Ability
    """hint: BoolAbilityVer"""
    ptzDirection: Ability
    """hint: PTZDirectionAbilityVers"""


class RecordScheduleAbilityVers(IntEnum):
    """Record Schedule Ability Values"""

    NONE = 0
    MD = 1
    MD_NORMAL = 2


class RecordAbilities(TypedDict):
    """Record Abilities"""

    recCfg: Ability
    """hint: BoolAbilityVer"""
    recSchedule: Ability
    """hint: RecordScheduleAbilityVers"""
    recDownload: Ability
    """hint: BoolAbilityVer"""
    recReplay: Ability
    """hint: BoolAbilityVer"""


class AlarmAbilities(TypedDict):
    """Alarm Abilities"""

    alarmIoIn: Ability
    """hint: BoolAbilityVer"""
    alarmIoOut: Ability
    """hint: BoolAbilityVer"""
    alarmRf: Ability
    """hint: BoolAbilityVer"""
    alarmMd: Ability
    """hint: BoolAbilityVer"""
    alarmAudio: Ability
    """hint: BoolAbilityVer"""


class DayNightAbilityVers(IntEnum):
    """Day/Night Ability Values"""

    NONE = 0
    DAY_NIGHT = 1
    THRESHOLD = 2


class ISPAbilities(TypedDict):
    """ISP Abilities"""

    ispDayNight: Ability
    """hint: DayNightAbilityVers"""
    ispAntiFlick: Ability
    """hint: BoolAbilityVer"""
    ispExposureMode: Ability
    """hint: BoolAbilityVer"""
    ispWhiteBalance: Ability
    """hint: BoolAbilityVer"""
    ispBackLight: Ability
    """hint: BoolAbilityVer"""
    isp3Dnr: Ability
    """hint: BoolAbilityVer"""
    ispMirror: Ability
    """hint: BoolAbilityVer"""
    ispFlip: Ability
    """hint: BoolAbilityVer"""
    ispBright: Ability
    """hint: BoolAbilityVer"""
    ispContrast: Ability
    """hint: BoolAbilityVer"""
    ispSaturation: Ability
    """hint: BoolAbilityVer"""
    ispHue: Ability
    """hint: BoolAbilityVer"""
    ispSharpen: Ability
    """hint: BoolAbilityVer"""


class MotionAbilities(TypedDict):
    """Motion Abilities"""

    mdTriggerAudio: Ability
    """hint: BoolAbilityVer"""
    mdTriggerRecord: Ability
    """hint: BoolAbilityVer"""


class ChannelAbilities(RecordAbilities, PTZAbilities, AlarmAbilities, ISPAbilities):
    """Channel Abilities"""

    mask: Ability
    """hint: BoolAbilityVer"""
    image: Ability
    """hint: BoolAbilityVer"""
    isp: Ability
    """hint: BoolAbilityVer"""
    while_balance: Ability
    """hint: BoolAbilityVer"""
    cameraMode: Ability
    """hint: BoolAbilityVer"""
    osd: Ability
    """hint: OsdAbilityVer"""
    waterMark: Ability
    """hint: BoolAbilityVer"""
    enc: Ability
    """hint: BoolAbilityVer"""
    live: Ability
    """hint: LiveAbilityVer"""
    snap: Ability
    """hint: BoolAbilityVer"""
    ftp: Ability
    """hint: FtpAbilityVers"""
    disableAutoFocus: Ability
    """hint: BoolAbilityVer"""
    battery: Ability
    """hint: BoolAbilityVer"""
    indicatorLight: Ability
    """hint: BoolAbilityVer"""
    videoClip: Ability
    """hint: VideoClipAbilityVers"""
    powerLed: Ability
    """hint: BoolAbilityVer"""
    mainEncType: Ability
    """hint: EncodingTypeAbilityVers"""
    floodLight: Ability
    """hint: FloodLightAbilitVers"""
    shelterCfg: Ability
    """hint: BoolAbilityVer"""
    batAnalysis: Ability
    """hint: BoolAbilityVer"""
    ledControl: Ability
    """hint: BoolAbilityVer"""
    ledControl: Ability
    """hint: supportPtzCheck"""
