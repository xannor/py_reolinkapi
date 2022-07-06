"""Channel Abilities"""

from enum import IntEnum
from typing import Sequence, SupportsIndex

from .base import Ability, BooleanAbility, VideoClipAbility
from . import support


class OsdValues(IntEnum):
    """Osd Ability Values"""

    NONE = 0
    SUPPORTED = 1
    DISTINCT = 2


class _OsdAbilitiy(Ability[OsdValues]):
    def __init__(self, ability: dict, **kwargs) -> None:
        super().__init__(
            ability=ability, factory=OsdValues, default=OsdValues.NONE, **kwargs
        )


class LiveValues(IntEnum):
    """Live Ability Values"""

    NONE = 0
    MAIN_EXTERN_SUB = 1
    MAIN_SUB = 2


class _LiveAbility(Ability[LiveValues]):
    def __init__(self, ability: dict, **kwargs) -> None:
        super().__init__(
            ability=ability, factory=LiveValues, default=LiveValues.NONE, **kwargs
        )


class FtpValues(IntEnum):
    """FTP Ability Values"""

    NONE = 0
    STREAM = 1
    JPEG_STREAM = 2
    MODE = 3
    JPEG_STREAM_MODE = 4
    STREAM_MODE_TYPE = 5
    JPEG_STREAM_MODE_TYPE = 6


class _FtpAbility(Ability[FtpValues]):
    def __init__(self, ability: dict, **kwargs) -> None:
        super().__init__(
            ability=ability, factory=FtpValues, default=FtpValues.NONE, **kwargs
        )


class EncodingTypeValues(IntEnum):
    """Encoding Type Ability Values"""

    H264 = 0
    H265 = 1


class _EncodingTypeAbility(Ability[EncodingTypeValues]):
    def __init__(self, ability: dict, **kwargs) -> None:
        super().__init__(
            ability=ability,
            factory=EncodingTypeValues,
            default=EncodingTypeValues.H264,
            **kwargs
        )


class FloodLightValues(IntEnum):
    """Flood Light Ability Vers"""

    NONE = 0
    WHITE = 1
    AUTO = 2


class _FloodLightAbility(Ability[FloodLightValues]):
    def __init__(self, ability: dict, **kwargs) -> None:
        super().__init__(
            ability=ability,
            factory=FloodLightValues,
            default=FloodLightValues.NONE,
            **kwargs
        )


class PTZTypeValues(IntEnum):
    """PTZ Type Ability Values"""

    NONE = 0
    AF = 1
    PTZ = 2
    PT = 3
    BALL = 4
    PTZ_NO_SPEED = 5


class _PTZTypeAbility(Ability[PTZTypeValues]):
    def __init__(self, ability: dict, **kwargs) -> None:
        super().__init__(
            ability=ability, factory=PTZTypeValues, default=PTZTypeValues.NONE, **kwargs
        )


class PTZControlValues(IntEnum):
    """PTZ Control Ability Values"""

    NONE = 0
    ZOOM = 1
    ZOOM_FOCUS = 2


class _PTZControlAbility(Ability[PTZControlValues]):
    def __init__(self, ability: dict, **kwargs) -> None:
        super().__init__(
            ability=ability,
            factory=PTZControlValues,
            default=PTZControlValues.NONE,
            **kwargs
        )


class PTZDirectionValues(IntEnum):
    """PTZ Direction Ability Values"""

    AUTOSCAN_8 = 0
    NO_AUTOACAN_4 = 1


class _PTZDirectionAbility(Ability[PTZDirectionValues]):
    def __init__(self, ability: dict, **kwargs) -> None:
        super().__init__(
            ability=ability,
            factory=PTZDirectionValues,
            default=PTZDirectionValues.AUTOSCAN_8,
            **kwargs
        )


class _Abilities:
    def __init__(self, abilities: dict, **kwargs) -> None:
        super().__init__(**kwargs)
        self._abilities = abilities


class _PTZAbilities(_Abilities):
    @property
    def type(self):
        return _PTZTypeAbility(self._abilities.get("ptzType", {}))

    @property
    def control(self):
        return _PTZControlAbility(self._abilities.get("ptzCtrl", {}))

    @property
    def preset(self):
        return BooleanAbility(self._abilities.get("ptzPreset", {}))

    @property
    def patrol(self):
        return BooleanAbility(self._abilities.get("ptzPatrol", {}))

    @property
    def tattern(self):
        return BooleanAbility(self._abilities.get("ptzTattern", {}))

    @property
    def direction(self):
        return _PTZDirectionAbility(self._abilities.get("ptzDirection", {}))


class RecordScheduleValues(IntEnum):
    """Record Schedule Ability Values"""

    NONE = 0
    MD = 1
    MD_NORMAL = 2


class _RecordScheduleAbility(Ability[RecordScheduleValues]):
    def __init__(self, ability: dict) -> None:
        super().__init__(
            ability, factory=RecordScheduleValues, default=RecordScheduleValues.NONE
        )


class _RecordAbilities(_Abilities):
    @property
    def configure(self):
        return BooleanAbility(self._abilities.get("recCfg", {}))

    @property
    def schedule(self):
        return _RecordScheduleAbility(self._abilities.get("recSchedule", {}))

    @property
    def download(self):
        return BooleanAbility(self._abilities.get("recDownload", {}))

    @property
    def replay(self):
        return BooleanAbility(self._abilities.get("recReplay", {}))


class _AlarmAbilities(_Abilities):
    @property
    def ioIn(self):
        return BooleanAbility(self._abilities.get("alarmIoIn", {}))

    @property
    def ioOut(self):
        return BooleanAbility(self._abilities.get("alarmIoOut", {}))

    @property
    def rf(self):
        return BooleanAbility(self._abilities.get("alarmRf", {}))

    @property
    def motion(self):
        return BooleanAbility(self._abilities.get("alarmMd", {}))

    @property
    def audio(self):
        return BooleanAbility(self._abilities.get("alarmAudio", {}))


class DayNightValues(IntEnum):
    """Day/Night Ability Values"""

    NONE = 0
    DAY_NIGHT = 1
    THRESHOLD = 2


class _DayNightAbility(Ability[DayNightValues]):
    def __init__(self, ability: dict, **kwargs) -> None:
        super().__init__(
            ability=ability,
            factory=DayNightValues,
            default=DayNightValues.NONE,
            **kwargs
        )


class _ISPAbilities(_Abilities, BooleanAbility):
    def __init__(self, abilities: dict, **kwargs) -> None:
        super().__init__(
            abilities=abilities, ability=abilities.get("isp", {}), **kwargs
        )

    @property
    def dayNight(self):
        return _DayNightAbility(self._abilities.get("ispDayNight", {}))

    @property
    def antiFlicker(self):
        return BooleanAbility(self._abilities.get("ispAntiFlick", {}))

    @property
    def exposureMode(self):
        return BooleanAbility(self._abilities.get("ispExposureMode", {}))

    @property
    def whiteBalance(self):
        return BooleanAbility(self._abilities.get("ispWhiteBalance", {}))

    @property
    def backlight(self):
        return BooleanAbility(self._abilities.get("ispBackLight", {}))

    @property
    def threeDNR(self):
        return BooleanAbility(self._abilities.get("isp3Dnr", {}))

    @property
    def mirror(self):
        return BooleanAbility(self._abilities.get("ispMirror", {}))

    @property
    def flip(self):
        return BooleanAbility(self._abilities.get("ispFlip", {}))

    @property
    def brightness(self):
        return BooleanAbility(self._abilities.get("ispBright", {}))

    @property
    def contrast(self):
        return BooleanAbility(self._abilities.get("ispContrast", {}))

    @property
    def saturation(self):
        return BooleanAbility(self._abilities.get("ispSaturation", {}))

    @property
    def hue(self):
        return BooleanAbility(self._abilities.get("ispHue", {}))

    @property
    def sharpness(self):
        return BooleanAbility(self._abilities.get("ispSharpen", {}))


class _MotionTriggerAbilities(_Abilities):
    @property
    def audio(self):
        return BooleanAbility(self._abilities.get("mdTriggerAudio", {}))

    @property
    def record(self):
        return BooleanAbility(self._abilities.get("mdTriggerRecord", {}))


class _MotionAbilities(_Abilities):
    @property
    def trigger(self):
        return _MotionTriggerAbilities(self._abilities)


class _SupportAbilities(_Abilities):
    @property
    def ai(self):
        return support.AIAbilities(self._abilities)

    @property
    def floodlight(self):
        return support.FloodlightAbilities(self._abilities)

    @property
    def gop(self):
        return BooleanAbility(self._abilities.get("supportGop", {}))

    @property
    def ptzCheck(self):
        return BooleanAbility(self._abilities.get("supportPtzCheck", {}))

    @property
    def whiteDark(self):
        return BooleanAbility(self._abilities.get("supportWhiteDark", {}))


class _ChannelAbilities(_Abilities):
    @property
    def record(self):
        return _RecordAbilities(self._abilities)

    @property
    def ptz(self):
        return _PTZAbilities(self._abilities)

    @property
    def alarm(self):
        return _AlarmAbilities(self._abilities)

    @property
    def isp(self):
        return _ISPAbilities(self._abilities)

    @property
    def support(self):
        return _SupportAbilities(self._abilities)

    @property
    def mask(self):
        return BooleanAbility(self._abilities.get("mask", {}))

    @property
    def image(self):
        return BooleanAbility(self._abilities.get("image", {}))

    @property
    def while_balance(self):
        return BooleanAbility(self._abilities.get("while_balance", {}))

    @property
    def cameraMode(self):
        return BooleanAbility(self._abilities.get("cameraMode", {}))

    @property
    def osd(self):
        return _OsdAbilitiy(self._abilities.get("osd", {}))

    @property
    def waterMark(self):
        return BooleanAbility(self._abilities.get("waterMark", {}))

    @property
    def enc(self):
        return BooleanAbility(self._abilities.get("enc", {}))

    @property
    def live(self):
        return _LiveAbility(self._abilities.get("live", {}))

    @property
    def snap(self):
        return BooleanAbility(self._abilities.get("snap", {}))

    @property
    def ftp(self):
        return _FtpAbility(self._abilities.get("ftp", {}))

    @property
    def disableAutoFocus(self):
        return BooleanAbility(self._abilities.get("disableAutoFocus", {}))

    @property
    def battery(self):
        return BooleanAbility(self._abilities.get("battery", {}))

    @property
    def indicatorLight(self):
        return BooleanAbility(self._abilities.get("indicatorLight", {}))

    @property
    def videoClip(self):
        return VideoClipAbility(self._abilities.get("videoClip", {}))

    @property
    def powerLed(self):
        return BooleanAbility(self._abilities.get("powerLed", {}))

    @property
    def mainEncType(self):
        return _EncodingTypeAbility(self._abilities.get("mainEncType", {}))

    @property
    def floodLight(self):
        return _FloodLightAbility(self._abilities.get("floodLight", {}))

    @property
    def shelterCfg(self):
        return BooleanAbility(self._abilities.get("shelterCfg", {}))

    @property
    def batAnalysis(self):
        return BooleanAbility(self._abilities.get("batAnalysis", {}))

    @property
    def ledControl(self):
        return BooleanAbility(self._abilities.get("ledControl", {}))


class ChannelsAbilities(Sequence[_ChannelAbilities]):
    """Channel Abilities"""

    def __init__(self, ability: list) -> None:
        self._data = ability

    def __len__(self) -> int:
        return self._data.__len__()

    def __getitem__(self, __k: SupportsIndex):
        return _ChannelAbilities(abilities=self._data[__k])
