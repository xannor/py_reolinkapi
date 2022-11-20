"""LED Typings"""

from enum import Enum, auto
from typing import Mapping, Protocol

from ..ai import typing as ai
from ..typing import PercentValue, SimpleTime


class LightStates(Enum):
    """Light States"""

    AUTO = auto()
    ON = auto()
    OFF = auto()


class LightingSchedule(Protocol):
    """Lighting Schedule"""

    start: SimpleTime
    end: SimpleTime


class WhiteLedInfo(Protocol):
    """White Led Info"""

    brightness: PercentValue
    auto_mode: bool
    brightness_state: int
    """according to API 0 given as example"""
    state: bool
    """according to API 0 given as example"""
    lighting_schedule: LightingSchedule
    ai_detection_type: Mapping[ai.AITypes, bool]
