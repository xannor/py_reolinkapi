""" Abilities """

from dataclasses import dataclass, field
from enum import IntEnum

from reolinkapi.rest.abilities.base import Ability

from .support import SupportAbilities

from ...utils.dataclasses import flatten, keyword

from .channel import ChannelAbilities
from .common import BooleanAbility as BoolAbility, VideoClipAbility


class TimeAbilitySupport(IntEnum):
    """Support"""

    NONE = 0
    SUNDAY = 1
    ANYDAY = 2


@dataclass
class TimeAbility(Ability[TimeAbilitySupport]):
    """Time Ability"""


class UpgradeAbilitySupport(IntEnum):
    """Support"""

    NONE = 0
    MANUAL = 1
    ONLINE = 2


@dataclass
class UpgradeAbility(Ability[UpgradeAbilitySupport]):
    """Upgrade Ability"""


class DdnsAbilitySupport(IntEnum):
    """Support"""

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


@dataclass
class DdnsAbility(Ability[DdnsAbilitySupport]):
    """DDNS Ability"""


class EmailAbilitySupport(IntEnum):
    """Support"""

    NONE = 0
    JPEG = 1
    VIDEO_JPEG = 2
    VIDEO_JPEG_NICK = 3


@dataclass
class EmailAbility(Ability[EmailAbilitySupport]):
    """Email Ability"""


@dataclass
class AlarmHDDAbilities:
    """HDD Abilities"""

    error: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("alarmHddErr")
    )
    full: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("alarmHddFull")
    )


@dataclass
class AlarmAbilities:
    """Alarm Abilities"""

    hdd: AlarmHDDAbilities = field(
        default_factory=AlarmHDDAbilities, metadata=flatten()
    )
    disconnect: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("alarmDisconnect")
    )
    ip_conflict: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("alarmIpConfict")
    )
    audio: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("alarmAudio")
    )


class VersionAbilitySupport(IntEnum):
    """Support"""

    BASIC = 0
    V20 = 1


@dataclass
class VersionAbility(Ability[VersionAbilitySupport]):
    """Version Ability"""


@dataclass
class FtpAbilities:
    """FTP Abilities"""

    test: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("ftpTest"))
    sub_stream: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ftpSubStream")
    )
    ext_stream: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ftpExtStream")
    )
    pic: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("ftpPic"))
    auto_dir: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ftpAutoDir")
    )


@dataclass
class RecordAbilities:
    """Record Abilities"""

    overwrite: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("recOverWrite")
    )
    pack_duration: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("recPackDuration")
    )
    pre_record: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("recPreRecord")
    )
    extension_time_list: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("recExtensionTimeList")
    )


@dataclass
class Abilities:
    """Abilities"""

    channel: list[ChannelAbilities] = field(
        default_factory=list, metadata=keyword("abilityChn")
    )
    support: SupportAbilities = field(
        default_factory=SupportAbilities, metadata=flatten()
    )
    hour_format: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("hourFmt")
    )
    time: TimeAbility = field(default_factory=TimeAbility, metadata=keyword("time"))
    tv_system: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("tvSystem")
    )
    display: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("display")
    )
    ipc_manager: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ipcManager")
    )
    device_info: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("devInfo")
    )
    auto_maint: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("autoMaint")
    )
    restore: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("restore")
    )
    reboot: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("reboot"))
    log: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("log"))
    performance: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("performance")
    )
    upgrade: UpgradeAbility = field(
        default_factory=UpgradeAbility, metadata=keyword("upgrade")
    )
    import_config: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("importCfg")
    )
    export_config: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("exportCfg")
    )
    disk: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("disk"))
    sd_card: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("sdCard")
    )
    device_name: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("devName")
    )
    auth: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("auth"))
    user: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("user"))
    online: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("online"))
    rtsp: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("rtsp"))
    rtmp: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("rtmp"))
    ddns: DdnsAbility = field(default_factory=DdnsAbility, metadata=keyword("ddns"))
    ddns_server: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ddnsCfg")
    )
    email: EmailAbility = field(default_factory=EmailAbility, metadata=keyword("email"))
    email_schedule: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("emailSchedule")
    )
    upnp: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("upnp"))
    onvif: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("onvif"))
    ntp: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("ntp"))
    media_port: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("mediaPort")
    )
    http: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("http"))
    https: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("https"))
    http_flv: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("httpFlv")
    )
    p2p: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("p2p"))
    three_g: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("3g"))
    local_link: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("localLink")
    )
    pppoe: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("pppoe"))
    wifi: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("Wifi"))
    push: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("Push"))
    push_schedule: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("pushSchedule")
    )
    talk: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("Talk"))
    alarm: AlarmAbilities = field(default_factory=AlarmAbilities, metadata=flatten())
    led_control: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("ledControl")
    )
    disable_auto_focus: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("disableAutoFocus")
    )
    video_clip: VideoClipAbility = field(
        default_factory=VideoClipAbility, metadata=keyword("videoClip")
    )
    cloud_storage: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("cloudStorage")
    )
    schedule_version: VersionAbility = field(
        default_factory=VersionAbility, metadata=keyword("scheduleVersion")
    )
    custom_audio: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("customAudio")
    )
    wifi_test: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("wifiTest")
    )
    sim: BoolAbility = field(default_factory=BoolAbility, metadata=keyword("simModule"))
    date_format: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("dateFormat")
    )
    email_interval: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("emailInterval")
    )
    show_qr_code: BoolAbility = field(
        default_factory=BoolAbility, metadata=keyword("showQrCode")
    )
    ftp: FtpAbilities = field(default_factory=FtpAbilities, metadata=flatten())
    record: RecordAbilities = field(default_factory=RecordAbilities, metadata=flatten())
