"""AI Typings"""

from enum import Enum, auto
from typing import Protocol


class AITypes(Enum):
    """AI Types"""

    ANIMAL = auto()
    PET = auto()
    FACE = auto()
    PEOPLE = auto()
    VEHICLE = auto()


class AlarmState(Protocol):
    """Alarm State"""

    state: bool
    supported: bool
