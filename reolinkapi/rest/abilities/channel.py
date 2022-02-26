""" Change Abilities """

from dataclasses import dataclass, field
from enum import IntEnum

from .base import Ability
from .common import BooleanAbility as BoolAbility, VideoClipAbility
from ...utils.dataclasses import flatten, keyword


class OsdAbilitySupport(IntEnum):
    """Support"""

    NONE = 0
    SUPPORTED = 1
    DISTINCT = 2


@dataclass
class OsdAbility(Ability[OsdAbilitySupport]):
    """OSD Ability"""


class LiveAbilitySupport(IntEnum):
    """Support"""

    NONE = 0
    MAIN_EXTERN_SUB = 1
    MAIN_SUB = 2


@dataclass
class LiveAbility(Ability[LiveAbilitySupport]):
    """Live Ability"""


class FtpAbilitySupport(IntEnum):
    """Support"""

    NONE = 0
    STREAM = 1
    JPEG_STREAM = 2
    MODE = 3
    JPEG_STREAM_MODE = 4
    STREAM_MODE_TYPE = 5
    JPEG_STREAM_MODE_TYPE = 6


@dataclass
class FtpAbility(Ability[FtpAbilitySupport]):
    """FTP Ability"""


class RecordScheduleAbilitySupport(IntEnum):
    """Support"""

    NONE = 0
    MD = 1
    MD_NORMAL = 2


@dataclass
class RecordScheduleAbility(Ability[RecordScheduleAbilitySupport]):
    """Schedule Ability"""


@dataclass
class RecordAbilities:
    """Record Abilities"""

    configure: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("recCfg")
    )
    schedule: RecordScheduleAbility = field(
        default_factory=RecordScheduleAbility, metadata=keyword("recSchedule")
    )
    download: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("recDownload")
    )
    replay: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("recReplay")
    )


class PTZTypeAbilitySupport(IntEnum):
    """Support"""

    NONE = 0
    AF = 1
    PTZ = 2
    PT = 3
    BALL = 4
    PTZ_NO_SPEED = 5


@dataclass
class PTZTypeAbility(Ability[PTZTypeAbilitySupport]):
    """Type Ability"""


class PTZControlAbilitySupport(IntEnum):
    """Support"""

    NONE = 0
    ZOOM = 1
    ZOOM_FOCUS = 2


@dataclass
class PTZControlAbility(Ability[PTZControlAbilitySupport]):
    """Control Ability"""


class PTZDirectionAbilitySupport(IntEnum):
    """Support"""

    AUTOSCAN_8 = 0
    NO_AUTOACAN_4 = 1


@dataclass
class PTZDirectionAbility(Ability[PTZDirectionAbilitySupport]):
    """Direction Ability"""


@dataclass
class PTZAbilities:
    """PTZ Abilities"""

    type: PTZTypeAbility = field(
        default_factory=PTZTypeAbility, metadata=keyword("ptzType")
    )
    control: PTZControlAbility = field(
        default_factory=PTZControlAbility, metadata=keyword("ptzCtrl")
    )
    preset: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ptzPreset")
    )
    patrol: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ptzPatrol")
    )
    tattern: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ptzTattern")
    )
    direction: PTZDirectionAbility = field(
        default_factory=PTZDirectionAbility, metadata=keyword("ptzDirection")
    )


@dataclass
class AlarmAbilities:
    """Alarm Abilities"""

    io_in: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("alarmIoIn")
    )
    io_out: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("alarmIoOut")
    )
    pir: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("alarmRf"))
    motion: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("alarmMd")
    )
    audio: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("alarmAudio")
    )


class EncodingTypeAbilitySupport(IntEnum):
    """Support"""

    H264 = 0
    H265 = 1


@dataclass
class EncodingTypeAbility(Ability[EncodingTypeAbilitySupport]):
    """EncodingType Ability"""


class DayNightAbilitySupport(IntEnum):
    """Support"""

    NONE = 0
    DAY_NIGHT = 1
    THRESHOLD = 2


@dataclass
class DayNightAbility(Ability[DayNightAbilitySupport]):
    """Day/Night Ability"""


@dataclass
class ISPAbilities:
    """ISP Abilities"""

    day_night: DayNightAbility = field(
        default_factory=DayNightAbility, metadata=keyword("ispDayNight")
    )
    anti_flicker: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ispAntiFlick")
    )
    exposure_mode: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ispExposureMode")
    )
    white_balance: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ispWhiteBalance")
    )
    back_light: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ispBackLight")
    )
    three_d_nr: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("isp3Dnr")
    )
    mirror: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ispMirror")
    )
    flip: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("ispFlip"))
    bright: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ispBright")
    )
    contrast: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ispContrast")
    )
    saturation: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ispSaturation")
    )
    hue: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("ispHue"))
    sharpen: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ispSharpen")
    )


class FloodLightAbilitySupport(IntEnum):
    """Support"""

    NONE = 0
    WHITE = 1
    AUTO = 2


@dataclass
class FloodLightAbility(Ability[FloodLightAbilitySupport]):
    """Flood Light Ability"""


@dataclass
class MotionTriggerAbilities:
    """Trigger Abilities"""

    audio: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("mdTriggerAudio")
    )
    record: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("mdTriggerRecord")
    )


@dataclass
class MotionAbilities:
    """Motion Detection Abilities"""

    with_pir: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("mdWithPir")
    )
    trigger: MotionTriggerAbilities = field(
        default_factory=MotionTriggerAbilities, metadata=flatten()
    )


@dataclass
class ChannelAbilities:
    """Channel Abilities"""

    mask: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("mask"))
    image: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("image"))
    isp: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("isp"))
    white_balance: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("white_balance")
    )
    camera_mode: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("cameraMode")
    )
    osd: OsdAbility = field(default_factory=OsdAbility, metadata=keyword("osd"))
    water_mark: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("waterMark")
    )
    encode_config: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("enc")
    )
    live: LiveAbility = field(default_factory=LiveAbility, metadata=keyword("live"))
    snap: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("snap"))
    ftp: FtpAbility = field(default_factory=FtpAbility, metadata=keyword("ftp"))
    record: RecordAbilities = field(default_factory=RecordAbilities, metadata=flatten())
    ptz: PTZAbilities = field(default_factory=PTZAbilities, metadata=flatten())
    alarm: AlarmAbilities = field(default_factory=AlarmAbilities, metadata=flatten())
    disable_auto_focus: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("disableAutoFocus")
    )
    battery: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("battery")
    )
    indicator_light: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("indicatorLight")
    )
    video_clip: VideoClipAbility = field(
        default_factory=VideoClipAbility, metadata=keyword("videoClip")
    )
    power_led: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("powerLed")
    )
    main_encoding_type: EncodingTypeAbility = field(
        default_factory=EncodingTypeAbility, metadata=keyword("mainEncType")
    )
    isp: ISPAbilities = field(default_factory=ISPAbilities, metadata=flatten())
    flood_light: FloodLightAbility = field(
        default_factory=FloodLightAbility, metadata=keyword("floodLight")
    )
    motion: MotionAbilities = field(default_factory=MotionAbilities, metadata=flatten())
    shelter_config: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("shelterCfg")
    )
    battery_analysis: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("batAnalysis")
    )
    led_control: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ledControl")
    )
    support_ptz_check: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportPtzCheck")
    )
