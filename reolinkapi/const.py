""" Constants """

from enum import IntEnum


DEFAULT_TIMEOUT = 30
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = ""


class LightTypes(IntEnum):
    """Light Types"""

    IR = 0
    POWER = 1
    WHITE = 1
