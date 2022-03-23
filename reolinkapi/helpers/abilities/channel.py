"""Channel helpers"""

from typing import Literal, overload

from ...typings.abilities.channel import (
    ChannelAbilities,
    EncodingTypeAbilityVers,
    PTZAbilities,
    PTZTypeAbilityVers,
)


@overload
def get_value(abilities: PTZAbilities, key: Literal["ptzType"]) -> int:
    ...


@overload
def has_value(abilities: PTZAbilities, key: Literal["ptzType"]) -> bool:
    ...


@overload
def is_value(
    abilities: PTZAbilities, key: Literal["ptzType"], value: PTZTypeAbilityVers
) -> bool:
    ...


@overload
def get_value(abilities: ChannelAbilities, key: Literal["mainEncType"]) -> int:
    ...


@overload
def has_value(
    abilities: ChannelAbilities,
    key: Literal["mainEncType"],
) -> bool:
    ...


@overload
def is_value(
    abilities: ChannelAbilities,
    key: Literal["mainEncType"],
    value: EncodingTypeAbilityVers,
) -> bool:
    ...


from .ability import get_value, has_value, is_value
