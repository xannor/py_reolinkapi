"""Support Abilities"""

from typing import Annotated, TypedDict

from .base import Ability, BooleanAbilityVers


class AudioAbilities(TypedDict, total=False):
    """Audio Abilities"""

    supportAudioAlarm: Annotated[Ability, BooleanAbilityVers]
    supportAudioAlarmEnable: Annotated[Ability, BooleanAbilityVers]
    supportAudioAlarmSchedule: Annotated[Ability, BooleanAbilityVers]
    supportAudioAlarmTaskEnable: Annotated[Ability, BooleanAbilityVers]


class AIAbilities(TypedDict, total=False):
    """AI Abilities"""

    supportAi: Annotated[Ability, BooleanAbilityVers]
    supportAiAnimal: Annotated[Ability, BooleanAbilityVers]
    supportAiDetectConfig: Annotated[Ability, BooleanAbilityVers]
    supportAiDogCat: Annotated[Ability, BooleanAbilityVers]
    supportAiFace: Annotated[Ability, BooleanAbilityVers]
    supportAiPeople: Annotated[Ability, BooleanAbilityVers]
    supportAiSensitivity: Annotated[Ability, BooleanAbilityVers]
    supportAiSayTime: Annotated[Ability, BooleanAbilityVers]
    supportAiTargetSize: Annotated[Ability, BooleanAbilityVers]
    supportAiVehicle: Annotated[Ability, BooleanAbilityVers]
    supportAoAdjust: Annotated[Ability, BooleanAbilityVers]


class FloodLightAbilities(TypedDict, total=False):
    """Floodlight Abilities"""

    supportFLBrightness: Annotated[Ability, BooleanAbilityVers]
    supportFLIntelligent: Annotated[Ability, BooleanAbilityVers]
    supportFLKeepOn: Annotated[Ability, BooleanAbilityVers]
    supportFLSchedule: Annotated[Ability, BooleanAbilityVers]
    supportFLSwitch: Annotated[Ability, BooleanAbilityVers]


class FTPAbilities(TypedDict, total=False):
    """FTP Abilities"""

    supportFtpEnable: Annotated[Ability, BooleanAbilityVers]
    supportFtpCoverPicture: Annotated[Ability, BooleanAbilityVers]
    supportFtpCoverVideo: Annotated[Ability, BooleanAbilityVers]
    supportFtDirYM: Annotated[Ability, BooleanAbilityVers]
    supportFtpPicCaptureMode: Annotated[Ability, BooleanAbilityVers]
    supportFtpPicResoCustom: Annotated[Ability, BooleanAbilityVers]
    supportFtpPictureSwap: Annotated[Ability, BooleanAbilityVers]
    supportFtpTask: Annotated[Ability, BooleanAbilityVers]
    supportFtpTaskEnable: Annotated[Ability, BooleanAbilityVers]
    supportFtpVideoSwap: Annotated[Ability, BooleanAbilityVers]
    supportFtpsEncrypt: Annotated[Ability, BooleanAbilityVers]


class SupportAbilities(AudioAbilities, FTPAbilities, total=False):
    """Support Abilities"""

    supportBuzzer: Annotated[Ability, BooleanAbilityVers]
    supportBuzzerEnable: Annotated[Ability, BooleanAbilityVers]
    supportBuzzerTask: Annotated[Ability, BooleanAbilityVers]
    supportBuzzerTaskEnable: Annotated[Ability, BooleanAbilityVers]
    supportRecordEnable: Annotated[Ability, BooleanAbilityVers]
    supportRecScheduleEnable: Annotated[Ability, BooleanAbilityVers]
    supportEmailEnable: Annotated[Ability, BooleanAbilityVers]
    supportEmailTaskEnable: Annotated[Ability, BooleanAbilityVers]
    supportThresholdAdjust: Annotated[Ability, BooleanAbilityVers]
    supportHttpEnable: Annotated[Ability, BooleanAbilityVers]
    supportHttpsEnable: Annotated[Ability, BooleanAbilityVers]
    supportOnvifEnable: Annotated[Ability, BooleanAbilityVers]
    supportPushInterval: Annotated[Ability, BooleanAbilityVers]
    supportRtmpEnable: Annotated[Ability, BooleanAbilityVers]
    supportRtspEnable: Annotated[Ability, BooleanAbilityVers]
