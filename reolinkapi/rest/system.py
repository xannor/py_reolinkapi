""" System Mixin """
from __future__ import annotations

from typing import Iterable, TypedDict

from ..typings.commands import (
    CommandRequestWithParam,
    CommandRequestTypes,
    CommandResponse,
)

from ..typings.abilities import Abilities
from ..typings.system import DeviceInfo, UserInfo

from . import connection
from ..helpers import commands as commandHelpers


class GetAbilityResponseValue(TypedDict):
    """Get Abilities Resposne Value"""

    Ability: Abilities


class UserInfoRequestParameter(TypedDict):
    """User Info Request Parameter"""

    User: UserInfo


GET_ABILITY_COMMAND = "GetAbility"

_isAbilities = commandHelpers.create_value_has_key("Ability", GetAbilityResponseValue)


def _get_ability_responses(responses: Iterable[CommandResponse]):

    return map(
        lambda response: response["value"]["Ability"],
        filter(
            _isAbilities,
            filter(
                commandHelpers.isvalue,
                filter(
                    lambda response: response["cmd"] == GET_ABILITY_COMMAND, responses
                ),
            ),
        ),
    )


class GetDeviceInfoResponseValue(TypedDict):
    """Get Device Info Response Value"""

    DevInfo: DeviceInfo


DEVICE_INFO_COMMAND = "GetDevInfo"

_isDevInfo = commandHelpers.create_value_has_key("DevInfo", GetDeviceInfoResponseValue)


def _get_devinfo_responses(responses: Iterable[CommandResponse]):

    return map(
        lambda response: response["value"]["DevInfo"],
        filter(
            _isDevInfo,
            filter(
                commandHelpers.isvalue,
                filter(
                    lambda response: response["cmd"] == DEVICE_INFO_COMMAND, responses
                ),
            ),
        ),
    )


class System:
    """System Commands Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        other: any = self
        if isinstance(other, connection.Connection) and not hasattr(self, "_execute"):
            # type "interface"
            self._execute = other._execute

    @staticmethod
    def create_get_ability(
        username: str | None = None,
        _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    ):
        """Create GetAbility Request"""
        return CommandRequestWithParam(
            cmd=GET_ABILITY_COMMAND,
            action=_type,
            param=UserInfoRequestParameter(User=UserInfo(userName=username or "null")),
        )

    @staticmethod
    def get_ability_responses(responses: Iterable[CommandResponse]):
        """Get GetAbility Responses"""

        return _get_ability_responses(responses)

    async def get_ability(self, username: str | None = None):
        """Get User Permisions"""

        value = next(
            _get_ability_responses(
                await self._execute(System.create_get_ability(username)),
            ),
            None,
        )
        return value

    @staticmethod
    def create_get_device_info(
        _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    ):
        """Create DeviceInfo Request"""
        return CommandRequestWithParam(cmd=DEVICE_INFO_COMMAND, action=_type)

    @staticmethod
    def get_device_info_responses(responses: Iterable[CommandResponse]):
        """Get DeviceInfo Responses"""

        return _get_devinfo_responses(responses)

    async def get_device_info(self):
        """Get Device Information"""

        devinfo = next(
            _get_devinfo_responses(
                await self._execute(System.create_get_device_info()),
            ),
            None,
        )
        return devinfo
