"""System"""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from ..connection.typing import WithConnection
from ..security.typing import WithSecurity
from ..errors import ReolinkResponseError
from .typing import WithSystem
from .capabilities import Capabilities
from .command import CommandFactory
from .models import NO_CAPABILITY, NO_DEVICEINFO
from .typing import DeviceInfo


class System(WithConnection[CommandFactory], WithSystem, WithSecurity):
    """System Commands Mixin"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def get_capabilities(self, username: str | None = None) -> Capabilities:
        """Get User Permisions"""

        if username is not None:
            auth_id = self._create_authentication_id(username)
        else:
            auth_id = self.authentication_id
        if auth_id.weak == self.authentication_id.weak:
            self.__capabilities = None

        async for response in self._execute(
            self.commands.create_get_capabilities_request(username)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_get_capabilities_response(response):
                if auth_id.weak == self.authentication_id.weak:
                    self.__capabilities = response.capabilities

                return response.capabilities

            if self.commands.is_error(response):
                response.throw("Get capabilities failed")

        return NO_CAPABILITY

    async def get_device_info(self) -> DeviceInfo:
        """Get Device Information"""

        async for response in self._execute(self.commands.create_get_device_info_request()):
            if not self.commands.is_response(response):
                break

            if self.commands.is_get_device_info_response(response):
                return response.info

            if self.commands.is_error(response):
                response.throw("Get device info failed")

        return NO_DEVICEINFO

    async def _get_time(self):
        async for response in self._execute(self.commands.create_get_time_request()):
            if not self.commands.is_response(response):
                break

            if self.commands.is_get_time_response(response):
                return response

            if self.commands.is_error(response):
                response.throw("Get time failed")

        raise ReolinkResponseError("Get Time failed")

    async def get_time(self):
        """Get Device Time Information"""

        return (await self._get_time()).to_datetime()

    async def get_time_info(self):
        """Get DST Info"""

        return (await self._get_time()).to_timezone()

    async def reboot(self):
        """Reboot device"""

        async for response in self._execute(self.commands.create_reboot_request()):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Reboot failed")

            if self.commands.is_success(response):
                return

        raise ReolinkResponseError("Reboot failed")

    async def get_storage_info(self):
        """Get Device Recording Capabilities"""

        async for response in self._execute(self.commands.create_get_hdd_info_request()):
            if not self.commands.is_response(response):
                break

            if self.commands.is_get_hdd_info_response(response):
                return response.info

            if self.commands.is_error(response):
                response.throw("Get storage Info failed")

        raise ReolinkResponseError("Get storage Info failed")
