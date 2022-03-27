""" Constants """

from enum import IntEnum
from typing import Literal


DEFAULT_TIMEOUT = 30
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = ""

STREAM_TYPES = Literal["main", "sub", "ext"]


class StreamTypes(IntEnum):
    """Stream Types"""

    MAIN = 0
    SUB = 1
    EXT = 2


class LightTypes(IntEnum):
    """Light Types"""

    IR = 0
    POWER = 1
    WHITE = 1
