""" Constants """

from enum import IntEnum
from typing import Final, Literal
from backports.strenum import StrEnum

DEFAULT_TIMEOUT: Final = 30
DEFAULT_USERNAME: Final = "admin"
DEFAULT_PASSWORD: Final = ""

STREAM_TYPES: Final = Literal["main", "sub", "ext"]


class IntStreamTypes(IntEnum):
    """Stream Types"""

    MAIN = 0
    SUB = 1
    EXT = 2


class StreamTypes(StrEnum):
    """Stream Types"""

    MAIN = "main"
    SUB = "sub"
    EXT = "ext"


class LightTypes(IntEnum):
    """Light Types"""

    IR = 0
    POWER = 1
    WHITE = 2
