""" System Mixin """
from __future__ import annotations

from typing import TypedDict

from reolinkapi.rest.typings.commands import CommandRequest, CommandRequestTypes

from .typings.abilities import Abilities
from .typings.system import DeviceInfo, UserInfo

from .connection import Connection


class GetAbilityResponseValue(TypedDict):
    """Get Abilities Resposne Value"""

    Ability: Abilities


class UserInfoRequestParameter(TypedDict):
    """User Info Request Parameter"""

    User: UserInfo


GET_ABILITY_COMMAND = "GetAbility"


class GetDeviceInfoResponseValue(TypedDict):
    """Get Device Info Response Value"""

    DevInfo: DeviceInfo


DEVICE_INFO_COMMAND = "GetDevInfo"


class System:
    """System Commands Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self, Connection) and not hasattr(self, "_execute"):
            # type "interface"
            self._execute = self._execute

    async def get_ability(self, username: str | None = None):
        """Get User Permisions"""

        results = await self._execute(
            CommandRequest(
                cmd=GET_ABILITY_COMMAND,
                action=CommandRequestTypes.VALUE_ONLY,
                param=UserInfoRequestParameter(
                    User=UserInfo(userName=username or "null")
                ),
            )
        )
        if (
            len(results) != 1
            or not isinstance(results[0], dict)
            or results[0]["cmd"] != GET_ABILITY_COMMAND
        ):
            return None

        value: GetAbilityResponseValue = results[0]["value"]
        return value["Ability"]

    async def get_device_info(self):
        """Get Device Information"""

        results = await self._execute(
            CommandRequest(
                cmd=DEVICE_INFO_COMMAND, action=CommandRequestTypes.VALUE_ONLY
            )
        )
        if (
            len(results) != 1
            or not isinstance(results[0], dict)
            or results[0]["cmd"] != DEVICE_INFO_COMMAND
        ):
            return None

        value: GetDeviceInfoResponseValue = results[0]["value"]
        return value["DevInfo"]
