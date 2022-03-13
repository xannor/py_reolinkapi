""" Constants """

from enum import IntEnum


DEFAULT_TIMEOUT = 30
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = ""


class DetectionTypes(IntEnum):
    """AI Detection Types"""

    NONE = 0
    PEOPLE = 1
    VEHICLE = 2
    ANIMAL = 3
    PET = 4
    FACE = 5


class LightTypes(IntEnum):
    """Light Types"""

    IR = 0
    POWER = 1
    WHITE = 1
