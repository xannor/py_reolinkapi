""" Common Abilities """

from dataclasses import dataclass
from enum import IntEnum
from .base import Ability


class BooleanAbility(Ability[bool]):
    """Yes/No"""


class VideoClipAbilitySupport(IntEnum):
    """Support"""

    NONE = 0
    FIXED = 1
    MOD = 2


@dataclass
class VideoClipAbility(Ability[VideoClipAbilitySupport]):
    """VideoClip Ability"""
