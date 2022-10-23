"""Command Factory"""

from typing import Protocol

from .ai.command import CommandFactory as AI
from .alarm.command import CommandFactory as Alarm
from .connection.typing import CommandFactory as WithCommandFactory
from .encoding.command import CommandFactory as Encoding
from .led.command import CommandFactory as LED
from .network.command import CommandFactory as Network
from .ptz.command import CommandFactory as PTZ
from .record.command import CommandFactory as Record
from .security.command import CommandFactory as Security
from .system.command import CommandFactory as System


class CommandFactory(
    AI,
    Alarm,
    Encoding,
    LED,
    Network,
    PTZ,
    Record,
    Security,
    System,
    WithCommandFactory,
    Protocol,
):
    """Command Factory"""
