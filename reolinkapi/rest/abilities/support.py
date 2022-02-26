""" Support Abilities """

from dataclasses import dataclass, field

from ...utils.dataclasses import flatten, keyword
from .common import BooleanAbility as BoolAbility


@dataclass
class AudioAbilities:
    """Audio Abilities"""

    alarm: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportAudioAlarm")
    )
    alarm_enable: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportAudioAlarmEnable")
    )
    alarm_schedule: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportAudioAlarmSchedule")
    )
    alarm_task_enable: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportAudioAlarmTaskEnable")
    )


@dataclass
class AIAbilities:
    """AI Abilities"""

    supported: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportAi")
    )
    animal: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportAiAnimal")
    )
    detect_config: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportAiDetectConfig")
    )
    dog_cat: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportAiDogCat")
    )
    face: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportAiFace")
    )
    people: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportAiPeople")
    )
    sensitivity: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportAiSensitivity")
    )
    say_time: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportAiSayTime")
    )
    target_size: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportAiTargetSize")
    )
    vehicle: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportAiVehicle")
    )
    adjust: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportAoAdjust")
    )


@dataclass
class FloodLightAbilities:
    """Floodlight Abilities"""

    brightness: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportFLBrightness")
    )
    intelligent: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportFLIntelligent")
    )
    keep_on: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportFLKeepOn")
    )
    schedule: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportFLSchedule")
    )
    switch: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportFLSwitch")
    )


@dataclass
class FtpAbilities:
    """FTP Abilities"""

    enable: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportFtpEnable")
    )
    cover_picture: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportFtpCoverPicture")
    )
    cover_video: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportFtpCoverVideo")
    )
    dir_ym: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportFtDirYM")
    )
    pic_capture_mode: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportFtpPicCaptureMode")
    )
    pic_custom_resolution: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportFtpPicResoCustom")
    )
    picture_swap: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportFtpPictureSwap")
    )
    task: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportFtpTask")
    )
    task_enable: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportFtpTaskEnable")
    )
    video_swap: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportFtpVideoSwap")
    )
    encrypt: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportFtpsEncrypt")
    )


@dataclass
class SupportAbilities:
    """Change Abilities"""

    audio: AudioAbilities = field(default_factory=AudioAbilities, metadata=flatten())
    buzzer: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportBuzzer")
    )
    buzzer_enable: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportBuzzerEnable")
    )
    buzzer_task: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportBuzzerTask")
    )
    buzzer_task_enable: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportBuzzerTaskEnable")
    )
    record_enable: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportRecordEnable")
    )
    record_schedule_enable: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportRecScheduleEnable")
    )
    email_enable: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportEmailEnable")
    )
    email_schedule_enable: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportEmailTaskEnable")
    )
    ai: AIAbilities = field(default_factory=AIAbilities, metadata=flatten())
    floodlight: FloodLightAbilities = field(
        default_factory=FloodLightAbilities, metadata=flatten()
    )
    gop: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportGop")
    )
    ptz_check: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportPtzCheck")
    )
    threshhold_adjust: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportThresholdAdjust")
    )
    white_dark: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportWhiteDark")
    )
    ftp: FtpAbilities = field(default_factory=FtpAbilities, metadata=flatten())
    http_enable: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportHttpEnable")
    )
    https_enable: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportHttpsEnable")
    )
    onvif_enable: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportOnvifEnable")
    )
    push_interval: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportPushInterval")
    )
    rtmp_enable: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportRtmpEnable")
    )
    rtsp_enable: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("supportRtspEnable")
    )
