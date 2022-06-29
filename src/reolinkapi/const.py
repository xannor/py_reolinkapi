""" Constants """

from enum import IntEnum
from typing import Literal

try:
    from enum import StrEnum #pylint: disable=ungrouped-imports
except ImportError:
    from backports.strenum import StrEnum

DEFAULT_TIMEOUT = 30
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = ""

STREAM_TYPES = Literal["main", "sub", "ext"]


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
