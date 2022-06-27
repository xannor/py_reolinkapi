"""Abilities Typings"""

from enum import IntEnum
from typing import Annotated, TypedDict

from .base import Ability, BooleanAbility, BooleanAbilityVers, VideoClipAbility, VideoClipValue
from .channel import ChannelsAbilities
from .support import SupportAbilities


class TimeValues(IntEnum):
    """Time Ability Values"""

    NONE = 0
    SUNDAY = 1
    ANYDAY = 2

class _TimeAbilitiy(Ability[TimeValues]):
    def __init__(self, source: dict) -> None:
        super().__init__(source, factory=TimeValues, default=TimeValues.NONE)


class UpgradeValues(IntEnum):
    """Upgrade Ability Values"""

    NONE = 0
    MANUAL = 1
    ONLINE = 2


class _UpgradeAbilitiy(Ability[UpgradeValues]):
    def __init__(self, source: dict) -> None:
        super().__init__(source, factory=UpgradeValues, default=UpgradeValues.NONE)

class DDnsValues(IntEnum):
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

class _DDnsAbilitiy(Ability[DDnsValues]):
    def __init__(self, source: dict) -> None:
        super().__init__(source, factory=DDnsValues, default=DDnsValues.NONE)

class EmailValues(IntEnum):
    """Email Ability Values"""

    NONE = 0
    JPEG = 1
    VIDEO_JPEG = 2
    VIDEO_JPEG_NICK = 3

class _EmailAbilitiy(Ability[EmailValues]):
    def __init__(self, source: dict) -> None:
        super().__init__(source, factory=EmailValues, default=EmailValues.NONE)

class VersionValues(IntEnum):
    """Version Ability Values"""

    BASIC = 0
    V20 = 1

class _VersionAbilitiy(Ability[VersionValues]):
    def __init__(self, source: dict) -> None:
        super().__init__(source, factory=VersionValues, default=VersionValues.NONE)

class _Abilities:

    def __init__(self, abilities:dict)-> None:
        self._abilities = abilities

class _AlarmHddAbilities(_Abilities):
    @property
    def error(self):
        return BooleanAbility(self._abilities.get("alarmHddErr", {}))

    @property
    def full(self):
        return BooleanAbility(self._abilities.get("alarmHddFull", {}))


class _AlarmAbilities(_Abilities):

    @property
    def hdd(self):
        return _AlarmHddAbilities(self._abilities)

    @property
    def disconnect(self):
        return BooleanAbility(self._abilities.get("alarmDisconnect", {}))

    @property
    def ipConflict(self):
        return BooleanAbility(self._abilities.get("alarmIpConfict", {}))

    @property
    def audio(self):
        return BooleanAbility(self._abilities.get("alarmAudio", {}))


class _FTPAbilities(_Abilities):

    @property
    def test(self):
        return BooleanAbility(self._abilities.get("ftpTest", {}))

    @property
    def subStream(self):
        return BooleanAbility(self._abilities.get("ftpSubStream", {}))

    @property
    def extStream(self):
        return BooleanAbility(self._abilities.get("ftpExtStream", {}))

    @property
    def picture(self):
        return BooleanAbility(self._abilities.get("ftpPic", {}))

    @property
    def autoDirectory(self):
        return BooleanAbility(self._abilities.get("ftpAutoDir", {}))

class _RecordAbilities(_Abilities):

    @property
    def overwrite(self):
        return BooleanAbility(self._abilities.get("recOverWrite", {}))

    @property
    def packDuration(self):
        return BooleanAbility(self._abilities.get("recPackDuration", {}))

    @property
    def preRecord(self):
        return BooleanAbility(self._abilities.get("recPreRecord", {}))

    @property
    def extensionTimeList(self):
        return BooleanAbility(self._abilities.get("recExtensionTimeList", {}))


class Abilities(_Abilities):

    @property
    def alarm(self):
        return _AlarmAbilities(self._abilities)

    @property
    def ftp(self):
        return _FTPAbilities(self._abilities)

    @property
    def record(self):
        return _RecordAbilities(self._abilities)

    @property
    def supports(self):
        return None

    @property
    def channels(self):
        return ChannelsAbilities(self._abilities.get("abilityChn", []))

    @property
    def hourFormat(self):
        return BooleanAbility(self._abilities.get("hourFmt", {}))

    @property
    def time(self):
        return _TimeAbilitiy(self._abilities.get("time", {}))

    @property
    def tvSystem(self):
        return BooleanAbility(self._abilities.get("tvSystem", {}))

    @property
    def display(self):
        return BooleanAbility(self._abilities.get("display", {}))

    @property
    def ipcManager(self):
        return BooleanAbility(self._abilities.get("ipcManager", {}))

    @property
    def devInfo(self):
        return BooleanAbility(self._abilities.get("devInfo", {}))

    @property
    def autoMaint(self):
        return BooleanAbility(self._abilities.get("autoMaint", {}))

    @property
    def restore(self):
        return BooleanAbility(self._abilities.get("restore", {}))

    @property
    def reboot(self):
        return BooleanAbility(self._abilities.get("reboot", {}))

    @property
    def log(self):
        return BooleanAbility(self._abilities.get("log", {}))

    @property
    def performance(self):
        return BooleanAbility(self._abilities.get("performance", {}))

    @property
    def upgrade(self):
        return BooleanAbility(self._abilities.get("upgrade", {}))

    @property
    def importCfg(self):
        return BooleanAbility(self._abilities.get("importCfg", {}))

    @property
    def exportCfg(self):
        return BooleanAbility(self._abilities.get("exportCfg", {}))

    @property
    def disk(self):
        return BooleanAbility(self._abilities.get("disk", {}))

    @property
    def sdCard(self):
        return BooleanAbility(self._abilities.get("sdCard", {}))

    @property
    def devName(self):
        return BooleanAbility(self._abilities.get("devName", {}))

    @property
    def auth(self):
        return BooleanAbility(self._abilities.get("auth", {}))

    @property
    def user(self):
        return BooleanAbility(self._abilities.get("user", {}))

    @property
    def online(self):
        return BooleanAbility(self._abilities.get("online", {}))

    @property
    def rtsp(self):
        return BooleanAbility(self._abilities.get("rtsp", {}))

    @property
    def rtmp(self):
        return BooleanAbility(self._abilities.get("rtmp", {}))

    @property
    def ddns(self):
        return _DDnsAbilitiy(self._abilities.get("ddns", {}))

    @property
    def ddnsCfg(self):
        return BooleanAbility(self._abilities.get("ddnsCfg", {}))

    @property
    def email(self):
        return _EmailAbilitiy(self._abilities.get("email", {}))

    @property
    def emailSchedule(self):
        return BooleanAbility(self._abilities.get("emailSchedule", {}))

    @property
    def upnp(self):
        return BooleanAbility(self._abilities.get("upnp", {}))

    @property
    def onvif(self):
        return BooleanAbility(self._abilities.get("onvif", {}))

    @property
    def ntp(self):
        return BooleanAbility(self._abilities.get("ntp", {}))

    @property
    def mediaPort(self):
        return BooleanAbility(self._abilities.get("mediaPort", {}))

    @property
    def http(self):
        return BooleanAbility(self._abilities.get("http", {}))

    @property
    def https(self):
        return BooleanAbility(self._abilities.get("https", {}))

    @property
    def http_flv(self):
        return BooleanAbility(self._abilities.get("http_flv", {}))

    @property
    def p2p(self):
        return BooleanAbility(self._abilities.get("p2p", {}))

    @property
    def localLink(self):
        return BooleanAbility(self._abilities.get("localLink", {}))

    @property
    def pppoe(self):
        return BooleanAbility(self._abilities.get("pppoe", {}))

    @property
    def wifi(self):
        return BooleanAbility(self._abilities.get("Wifi", {}))

    @property
    def push(self):
        return BooleanAbility(self._abilities.get("Push", {}))

    @property
    def pushSchedule(self):
        return BooleanAbility(self._abilities.get("pushSchedule", {}))

    @property
    def talk(self):
        return BooleanAbility(self._abilities.get("Talk", {}))

    @property
    def ledControl(self):
        return BooleanAbility(self._abilities.get("ledControl", {}))

    @property
    def disableAutoFocus(self):
        return BooleanAbility(self._abilities.get("disableAutoFocus", {}))

    @property
    def videoClip(self):
        return VideoClipAbility(self._abilities.get("videoClip", {}))

    @property
    def cloudStorage(self):
        return BooleanAbility(self._abilities.get("cloudStorage", {}))

    @property
    def scheduleVersion(self):
        return _VersionAbilitiy(self._abilities.get("scheduleVersion", {}))

    @property
    def customAudio(self):
        return BooleanAbility(self._abilities.get("customAudio", {}))

    @property
    def wifiTest(self):
        return BooleanAbility(self._abilities.get("wifiTest", {}))

    @property
    def simModule(self):
        return BooleanAbility(self._abilities.get("simModule", {}))

    @property
    def dateFormat(self):
        return BooleanAbility(self._abilities.get("dateFormat", {}))

    @property
    def emailInterval(self):
        return BooleanAbility(self._abilities.get("emailInterval", {}))

    @property
    def showQrCode(self):
        return BooleanAbility(self._abilities.get("showQrCode", {}))

    @property
    def threeG(self):
        return BooleanAbility(self._abilities.get("3g", {}))
