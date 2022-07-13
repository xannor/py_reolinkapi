"""Support Abilities"""

from .base import BooleanAbility


class _Abilities:
    def __init__(self, abilities: dict, **kwargs) -> None:
        super().__init__(**kwargs)
        self._abilities = abilities


class _AudioAlarmAbilities(_Abilities, BooleanAbility):
    def __init__(self, abilities: dict, **kwargs) -> None:
        super().__init__(
            abilities=abilities,
            ability=abilities.get("supportAudioAlarm", {}),
            **kwargs
        )

    @property
    def enable(self):
        return BooleanAbility(self._abilities.get("supportAudioAlarmEnable", {}))

    @property
    def schedule(self):
        return BooleanAbility(self._abilities.get("supportAudioAlarmSchedule", {}))

    @property
    def taskEnable(self):
        return BooleanAbility(self._abilities.get("supportAudioAlarmTaskEnable", {}))


class _AudioAbilities(_Abilities):
    @property
    def alarm(self):
        return _AudioAlarmAbilities(self._abilities)


class AIAbilities(_Abilities, BooleanAbility):
    """AI Abilities"""

    def __init__(self, abilities: dict, **kwargs) -> None:
        super().__init__(abilities, ability=abilities.get("supportAi", {}), **kwargs)

    @property
    def animal(self):
        return BooleanAbility(self._abilities.get("supportAiAnimal", {}))

    @property
    def detectConfig(self):
        return BooleanAbility(self._abilities.get("supportAiDetectConfig", {}))

    @property
    def pet(self):
        return BooleanAbility(self._abilities.get("supportAiDogCat", {}))

    @property
    def face(self):
        return BooleanAbility(self._abilities.get("supportAiFace", {}))

    @property
    def people(self):
        return BooleanAbility(self._abilities.get("supportAiPeople", {}))

    @property
    def sensitivity(self):
        return BooleanAbility(self._abilities.get("supportAiSensitivity", {}))

    @property
    def sayTime(self):
        return BooleanAbility(self._abilities.get("supportAiSayTime", {}))

    @property
    def targetSize(self):
        return BooleanAbility(self._abilities.get("supportAiTargetSize", {}))

    @property
    def vehicle(self):
        return BooleanAbility(self._abilities.get("supportAiVehicle", {}))

    @property
    def aoAdjust(self):
        return BooleanAbility(self._abilities.get("supportAoAdjust", {}))


class FloodlightAbilities(_Abilities):
    @property
    def brightness(self):
        return BooleanAbility(self._abilities.get("supportFLBrightness", {}))

    @property
    def intelligent(self):
        return BooleanAbility(self._abilities.get("supportFLIntelligent", {}))

    @property
    def keepOn(self):
        return BooleanAbility(self._abilities.get("supportFLKeepOn", {}))

    @property
    def schedule(self):
        return BooleanAbility(self._abilities.get("supportFLSchedule", {}))

    @property
    def switch(self):
        return BooleanAbility(self._abilities.get("supportFLSwitch", {}))


class _FTPAbilities(_Abilities):
    @property
    def enable(self):
        return BooleanAbility(self._abilities.get("supportFtpEnable", {}))

    @property
    def coverPicture(self):
        return BooleanAbility(self._abilities.get("supportFtpCoverPicture", {}))

    @property
    def coverVideo(self):
        return BooleanAbility(self._abilities.get("supportFtpCoverVideo", {}))

    @property
    def dirYM(self):
        return BooleanAbility(self._abilities.get("supportFtpDirYM", {}))

    @property
    def pictureCaptureMode(self):
        return BooleanAbility(self._abilities.get("supportFtpPicCaptureMode", {}))

    @property
    def pictureCustomResolution(self):
        return BooleanAbility(self._abilities.get("supportFtpPicResoCustom", {}))

    @property
    def pictureSwap(self):
        return BooleanAbility(self._abilities.get("supportFtpPictureSwap", {}))

    @property
    def task(self):
        return BooleanAbility(self._abilities.get("supportFtpTask", {}))

    @property
    def taskEnable(self):
        return BooleanAbility(self._abilities.get("supportFtpTaskEnable", {}))

    @property
    def videoSwap(self):
        return BooleanAbility(self._abilities.get("supportFtpVideoSwap", {}))

    @property
    def secureFTP(self):
        return BooleanAbility(self._abilities.get("supportFtpsEncrypt", {}))


class SupportAbilities(_Abilities):
    @property
    def audio(self):
        return _AudioAbilities(self._abilities)

    @property
    def ftp(self):
        return _FTPAbilities(self._abilities)

    @property
    def buzzer(self):
        return BooleanAbility(self._abilities.get("supportBuzzer", {}))

    @property
    def buzzerEnable(self):
        return BooleanAbility(self._abilities.get("supportBuzzerEnable", {}))

    @property
    def buzzerTask(self):
        return BooleanAbility(self._abilities.get("supportBuzzerTask", {}))

    @property
    def buzzerTaskEnable(self):
        return BooleanAbility(self._abilities.get("supportBuzzerTaskEnable", {}))

    @property
    def recordEnable(self):
        return BooleanAbility(self._abilities.get("supportRecordEnable", {}))

    @property
    def recordScheduleEnable(self):
        return BooleanAbility(self._abilities.get("supportRecScheduleEnable", {}))

    @property
    def emailEnable(self):
        return BooleanAbility(self._abilities.get("supportEmailEnable", {}))

    @property
    def emailTaskEnable(self):
        return BooleanAbility(self._abilities.get("supportEmailTaskEnable", {}))

    @property
    def threshholdAdjust(self):
        return BooleanAbility(self._abilities.get("supportThresholdAdjust", {}))

    @property
    def httpEnable(self):
        return BooleanAbility(self._abilities.get("supportHttpEnable", {}))

    @property
    def httpsEnable(self):
        return BooleanAbility(self._abilities.get("supportHttpsEnable", {}))

    @property
    def onvifEnable(self):
        return BooleanAbility(self._abilities.get("supportOnvifEnable", {}))

    @property
    def pushInterval(self):
        return BooleanAbility(self._abilities.get("supportPushInterval", {}))

    @property
    def rtmpEnable(self):
        return BooleanAbility(self._abilities.get("supportRtmpEnable", {}))

    @property
    def rtspEnable(self):
        return BooleanAbility(self._abilities.get("supportRtspEnable", {}))
