"""Led Typings"""


from enum import Enum
from typing import TypedDict


class LightStates(str, Enum):
    """Light States"""

    AUTO = "Auto"
    ON = "On"
    OFF = "Off"


class LightState(TypedDict, total=False):
    """Light State"""

    channel: int
    state: str


class LightingSchedule(TypedDict, total=False):
    """Lighting Schedule"""

    StartHour: int
    StartMin: int
    EndHour: int
    EndMin: int


class AiDetectType(TypedDict, total=False):
    """AI Detect Types"""

    dog_cat: int
    face: int
    people: int
    vehicle: int


class WhiteLedInfo(TypedDict, total=False):
    """White Led Info"""

    channel: int
    bright: int
    mode: int
    state: int
    LightingSchedule: LightingSchedule
    wlAiDetectType: AiDetectType
