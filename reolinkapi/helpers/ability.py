"""Ability helpers"""

from typing import Final

from ..typings.abilities import Abilities
from ..typings.abilities.base import Ability
from ..typings.abilities.channel import ChannelAbilities

NO_ABILITY: Final = Ability(ver=0, permit=0)
NO_CHANNEL_ABILITIES: Final = ChannelAbilities()
NO_ABILITIES: Final = Abilities()


def has_value(abilities: dict[str, Ability], key: str):
    return (
        key in abilities
        and isinstance(abilities[key], dict)
        and "ver" in abilities[key]
        and abilities[key]["ver"] != 0
    )


def is_value(abilities: dict[str, Ability], key: str, value: int):
    return (
        key in abilities
        and isinstance(abilities[key], dict)
        and "ver" in abilities[key]
        and abilities[key]["ver"] == value
    )
