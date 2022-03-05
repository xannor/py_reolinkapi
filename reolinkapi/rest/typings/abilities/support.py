"""Support Abilities"""

from typing import TypedDict

from .base import Ability


class AudioAbilities(TypedDict):
    """Audio Abilities"""

    supportAudioAlarm: Ability
    """hint: BoolAbilityVer"""
    supportAudioAlarmEnable: Ability
    """hint: BoolAbilityVer"""
    supportAudioAlarmSchedule: Ability
    """hint: BoolAbilityVer"""
    supportAudioAlarmTaskEnable: Ability
    """hint: BoolAbilityVer"""


class AIAbilities(TypedDict):
    """AI Abilities"""

    supportAi: Ability
    """hint: BoolAbilityVer"""
    supportAiAnimal: Ability
    """hint: BoolAbilityVer"""
    supportAiDetectConfig: Ability
    """hint: BoolAbilityVer"""
    supportAiDogCat: Ability
    """hint: BoolAbilityVer"""
    supportAiFace: Ability
    """hint: BoolAbilityVer"""
    supportAiPeople: Ability
    """hint: BoolAbilityVer"""
    supportAiSensitivity: Ability
    """hint: BoolAbilityVer"""
    supportAiSayTime: Ability
    """hint: BoolAbilityVer"""
    supportAiTargetSize: Ability
    """hint: BoolAbilityVer"""
    supportAiVehicle: Ability
    """hint: BoolAbilityVer"""
    supportAoAdjust: Ability
    """hint: BoolAbilityVer"""


class FloodLightAbilities(TypedDict):
    """Floodlight Abilities"""

    supportFLBrightness: Ability
    """hint: BoolAbilityVer"""
    supportFLIntelligent: Ability
    """hint: BoolAbilityVer"""
    supportFLKeepOn: Ability
    """hint: BoolAbilityVer"""
    supportFLSchedule: Ability
    """hint: BoolAbilityVer"""
    supportFLSwitch: Ability
    """hint: BoolAbilityVer"""


class FTPAbilities(TypedDict):
    """FTP Abilities"""

    supportFtpEnable: Ability
    """hint: BoolAbilityVer"""
    supportFtpCoverPicture: Ability
    """hint: BoolAbilityVer"""
    supportFtpCoverVideo: Ability
    """hint: BoolAbilityVer"""
    supportFtDirYM: Ability
    """hint: BoolAbilityVer"""
    supportFtpPicCaptureMode: Ability
    """hint: BoolAbilityVer"""
    supportFtpPicResoCustom: Ability
    """hint: BoolAbilityVer"""
    supportFtpPictureSwap: Ability
    """hint: BoolAbilityVer"""
    supportFtpTask: Ability
    """hint: BoolAbilityVer"""
    supportFtpTaskEnable: Ability
    """hint: BoolAbilityVer"""
    supportFtpVideoSwap: Ability
    """hint: BoolAbilityVer"""
    supportFtpsEncrypt: Ability
    """hint: BoolAbilityVer"""


class SupportAbilities(AudioAbilities, AIAbilities, FloodLightAbilities, FTPAbilities):
    """Support Abilities"""

    supportBuzzer: Ability
    """hint: BoolAbilityVer"""
    supportBuzzerEnable: Ability
    """hint: BoolAbilityVer"""
    supportBuzzerTask: Ability
    """hint: BoolAbilityVer"""
    supportBuzzerTaskEnable: Ability
    """hint: BoolAbilityVer"""
    supportRecordEnable: Ability
    """hint: BoolAbilityVer"""
    supportRecScheduleEnable: Ability
    """hint: BoolAbilityVer"""
    supportEmailEnable: Ability
    """hint: BoolAbilityVer"""
    supportEmailTaskEnable: Ability
    """hint: BoolAbilityVer"""
    supportGop: Ability
    """hint: BoolAbilityVer"""
    supportPtzCheck: Ability
    """hint: BoolAbilityVer"""
    supportThresholdAdjust: Ability
    """hint: BoolAbilityVer"""
    supportWhiteDark: Ability
    """hint: BoolAbilityVer"""
    supportHttpEnable: Ability
    """hint: BoolAbilityVer"""
    supportHttpsEnable: Ability
    """hint: BoolAbilityVer"""
    supportOnvifEnable: Ability
    """hint: BoolAbilityVer"""
    supportPushInterval: Ability
    """hint: BoolAbilityVer"""
    supportRtmpEnable: Ability
    """hint: BoolAbilityVer"""
    supportRtspEnable: Ability
    """hint: BoolAbilityVer"""
