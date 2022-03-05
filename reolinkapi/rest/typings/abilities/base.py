"""System Abilities Typings"""

from enum import IntEnum, IntFlag
from typing import TypedDict


class Permissions(IntFlag):
    """Ability permissions (Permit)"""

    NONE = 0
    OPTION = 1
    WRITE = 2
    READ = 4


class BooleanAbilityVers(IntEnum):
    """Boolean Ability Values"""

    NOT_SUPPORTED = 0
    SUPPORTED = 1


class VideoClipAbilityVers(IntEnum):
    """Video Clip Ability Values"""

    NONE = 0
    FIXED = 1
    MOD = 2


class Ability(TypedDict):
    """Ability"""

    ver: int
    """value 'supported'
    hint: eg BooleanAbilityVers"""
    permit: int
    """hint: Permissions"""
