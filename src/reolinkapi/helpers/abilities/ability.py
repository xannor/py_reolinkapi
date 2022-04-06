"""Ability helpers"""
from __future__ import annotations

from typing import Final, overload

from ...typings.abilities import Abilities
from ...typings.abilities.base import (
    Ability,
    Permissions,
    ABILITY_VALUE,
    ABILITY_PERMISSION,
)
from ...typings.abilities.channel import ChannelAbilities

NO_ABILITY: Final = Ability(ver=0, permit=0)
NO_CHANNEL_ABILITIES: Final = ChannelAbilities()
NO_ABILITIES: Final = Abilities()


def get_permissions(ability: Ability):
    """Get typed ability permissions"""

    return Permissions(ability.get(ABILITY_PERMISSION, Permissions.NONE))


def has_permission(ability: Ability, permission: Permissions):
    """Verify ability has the given permission"""
    return get_permissions(ability) & permission == permission


@overload
def get_value(ability: Ability) -> int:
    ...


@overload
def get_value(abilities: dict[str, Ability], key: str) -> int:
    ...


def get_value(ability: dict, key: str | None = None) -> int:
    """Get ability value"""
    if key is not None:
        ability = ability.get(key, NO_ABILITY)
    return ability.get(ABILITY_VALUE, 0)


def has_value(abilities: dict[str, Ability], key: str):
    """Returns true of ability is present and non-zero false otherwise"""

    return get_value(abilities, key) != 0


def is_value(abilities: dict[str, Ability], key: str, value: int):
    """Returns true if ability matches the value provided"""

    return get_value(abilities, key) == value
