"""Channel Abilities"""

from enum import IntEnum
from typing import Annotated, TypedDict

from .base import Ability, BooleanAbilityVers, VideoClipAbilityVers
from . import support


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


class PTZAbilities(TypedDict, total=False):
    """PTZ Abilities"""

    ptzType: Annotated[Ability, PTZTypeAbilityVers]
    ptzCtrl: Annotated[Ability, PTZControlAbilityVers]
    ptzPreset: Annotated[Ability, BooleanAbilityVers]
    ptzPatrol: Annotated[Ability, BooleanAbilityVers]
    ptzTattern: Annotated[Ability, BooleanAbilityVers]
    ptzDirection: Annotated[Ability, PTZDirectionAbilityVers]


class RecordScheduleAbilityVers(IntEnum):
    """Record Schedule Ability Values"""

    NONE = 0
    MD = 1
    MD_NORMAL = 2


class RecordAbilities(TypedDict, total=False):
    """Record Abilities"""

    recCfg: Annotated[Ability, BooleanAbilityVers]
    recSchedule: Annotated[Ability, RecordScheduleAbilityVers]
    recDownload: Annotated[Ability, BooleanAbilityVers]
    recReplay: Annotated[Ability, BooleanAbilityVers]


class AlarmAbilities(TypedDict, total=False):
    """Alarm Abilities"""

    alarmIoIn: Annotated[Ability, BooleanAbilityVers]
    alarmIoOut: Annotated[Ability, BooleanAbilityVers]
    alarmRf: Annotated[Ability, BooleanAbilityVers]
    alarmMd: Annotated[Ability, BooleanAbilityVers]
    alarmAudio: Annotated[Ability, BooleanAbilityVers]


class DayNightAbilityVers(IntEnum):
    """Day/Night Ability Values"""

    NONE = 0
    DAY_NIGHT = 1
    THRESHOLD = 2


class ISPAbilities(TypedDict, total=False):
    """ISP Abilities"""

    ispDayNight: Annotated[Ability, DayNightAbilityVers]
    ispAntiFlick: Annotated[Ability, BooleanAbilityVers]
    ispExposureMode: Annotated[Ability, BooleanAbilityVers]
    ispWhiteBalance: Annotated[Ability, BooleanAbilityVers]
    ispBackLight: Annotated[Ability, BooleanAbilityVers]
    isp3Dnr: Annotated[Ability, BooleanAbilityVers]
    ispMirror: Annotated[Ability, BooleanAbilityVers]
    ispFlip: Annotated[Ability, BooleanAbilityVers]
    ispBright: Annotated[Ability, BooleanAbilityVers]
    ispContrast: Annotated[Ability, BooleanAbilityVers]
    ispSaturation: Annotated[Ability, BooleanAbilityVers]
    ispHue: Annotated[Ability, BooleanAbilityVers]
    ispSharpen: Annotated[Ability, BooleanAbilityVers]


class MotionAbilities(TypedDict, total=False):
    """Motion Abilities"""

    mdTriggerAudio: Annotated[Ability, BooleanAbilityVers]
    mdTriggerRecord: Annotated[Ability, BooleanAbilityVers]


class SupportAbilities(support.AIAbilities, support.FloodLightAbilities):
    """Support Abilities"""

    supportGop: Annotated[Ability, BooleanAbilityVers]
    supportPtzCheck: Annotated[Ability, BooleanAbilityVers]
    supportWhiteDark: Annotated[Ability, BooleanAbilityVers]


class ChannelAbilities(
    RecordAbilities,
    PTZAbilities,
    AlarmAbilities,
    ISPAbilities,
    SupportAbilities,
    total=False,
):
    """Channel Abilities"""

    mask: Annotated[Ability, BooleanAbilityVers]
    image: Annotated[Ability, BooleanAbilityVers]
    isp: Annotated[Ability, BooleanAbilityVers]
    while_balance: Annotated[Ability, BooleanAbilityVers]
    cameraMode: Annotated[Ability, BooleanAbilityVers]
    osd: Annotated[Ability, OsdAbilityVers]
    waterMark: Annotated[Ability, BooleanAbilityVers]
    enc: Annotated[Ability, BooleanAbilityVers]
    live: Annotated[Ability, LiveAbilityVers]
    snap: Annotated[Ability, BooleanAbilityVers]
    ftp: Annotated[Ability, FtpAbilityVers]
    disableAutoFocus: Annotated[Ability, BooleanAbilityVers]
    battery: Annotated[Ability, BooleanAbilityVers]
    indicatorLight: Annotated[Ability, BooleanAbilityVers]
    videoClip: Annotated[Ability, VideoClipAbilityVers]
    powerLed: Annotated[Ability, BooleanAbilityVers]
    mainEncType: Annotated[Ability, EncodingTypeAbilityVers]
    floodLight: Annotated[Ability, FloodLightAbilitVers]
    shelterCfg: Annotated[Ability, BooleanAbilityVers]
    batAnalysis: Annotated[Ability, BooleanAbilityVers]
    ledControl: Annotated[Ability, BooleanAbilityVers]
