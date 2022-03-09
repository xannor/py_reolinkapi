""" System Mixin """
from __future__ import annotations

from typing import Iterable, TypedDict

from .typings.commands import (
    CommandRequest,
    CommandRequestTypes,
    CommandResponse,
    filter_command_responses,
)

from .typings.abilities import Abilities
from .typings.system import DeviceInfo, UserInfo

from . import connection


class GetAbilityResponseValue(TypedDict):
    """Get Abilities Resposne Value"""

    Ability: Abilities


def _cast_ability_response_value(responses: Iterable[CommandResponse]):
    def _cast(response: CommandResponse):
        value: GetAbilityResponseValue = response["value"]
        return value["Ability"]

    return map(_cast, responses)


class UserInfoRequestParameter(TypedDict):
    """User Info Request Parameter"""

    User: UserInfo


GET_ABILITY_COMMAND = "GetAbility"


class GetDeviceInfoResponseValue(TypedDict):
    """Get Device Info Response Value"""

    DevInfo: DeviceInfo


def _cast_device_info_response_value(responses: Iterable[CommandResponse]):
    def _cast(response: CommandResponse):
        value: GetDeviceInfoResponseValue = response["value"]
        return value["DevInfo"]

    return map(_cast, responses)


DEVICE_INFO_COMMAND = "GetDevInfo"


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
        return CommandRequest(
            cmd=GET_ABILITY_COMMAND,
            action=_type,
            param=UserInfoRequestParameter(User=UserInfo(userName=username or "null")),
        )

    @staticmethod
    def get_ability_responses(responses: Iterable[CommandResponse]):
        """Get GetAbility Responses"""

        return _cast_ability_response_value(
            filter_command_responses(GET_ABILITY_COMMAND, responses)
        )

    async def get_ability(self, username: str | None = None):
        """Get User Permisions"""

        abilities = next(
            _cast_ability_response_value(
                filter_command_responses(
                    GET_ABILITY_COMMAND,
                    await self._execute(System.create_get_ability(username)),
                )
            ),
            None,
        )
        return abilities

    @staticmethod
    def create_get_device_info(
        _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    ):
        """Create DeviceInfo Request"""
        return CommandRequest(cmd=DEVICE_INFO_COMMAND, action=_type)

    @staticmethod
    def get_device_info_responses(responses: Iterable[CommandResponse]):
        """Get DeviceInfo Responses"""

        return _cast_device_info_response_value(
            filter_command_responses(DEVICE_INFO_COMMAND, responses)
        )

    async def get_device_info(self):
        """Get Device Information"""

        devinfo = next(
            _cast_device_info_response_value(
                filter_command_responses(
                    DEVICE_INFO_COMMAND,
                    await self._execute(System.create_get_device_info()),
                )
            ),
            None,
        )
        return devinfo
