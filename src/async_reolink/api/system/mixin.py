"""System"""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from ..connection.typing import WithConnection
from ..errors import ReolinkResponseError
from .typing import WithSystem
from .capabilities import Capabilities
from .command import CommandFactory
from .models import NO_CAPABILITY, NO_DEVICEINFO
from .typing import DeviceInfo


class System(WithConnection[CommandFactory], WithSystem):
    """System Commands Mixin"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__abilities = None
        self.__time = None
        self.__timezone = None

        self._disconnect_callbacks.append(self.__clear)

    def __clear(self):
        self.__abilities = None
        self.__timezone = None
        self.__time = None

    async def get_capabilities(self, username: str | None = None) -> Capabilities:
        """Get User Permisions"""

        if username is None:
            self.__abilities = None

        async for response in self._execute(
            self.commands.create_get_capabilities_request(username)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_get_capabilities_response(response):
                return response.capabilities

            if self.commands.is_error(response):
                response.throw("Get capabilities failed")

        return NO_CAPABILITY

    async def _ensure_capabilities(self):
        if self.__abilities:
            return self.__abilities
        return await self.get_capabilities()

    async def get_device_info(self) -> DeviceInfo:
        """Get Device Information"""

        async for response in self._execute(
            self.commands.create_get_device_info_request()
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_get_device_info_response(response):
                return response.info

            if self.commands.is_error(response):
                response.throw("Get device info failed")

        return NO_DEVICEINFO

    async def get_time(self):
        """Get Device Time Information"""

        self.__timezone = None
        self.__time = None

        async for response in self._execute(self.commands.create_get_time_request()):
            if not self.commands.is_response(response):
                break

            if self.commands.is_get_time_response(response):
                self.__time = response.to_datetime()
                self.__timezone = response.to_timezone()

                return self.__time

            if self.commands.is_error(response):
                response.throw("Get time failed")

        if TYPE_CHECKING:
            _time = datetime.now()
            self.__time = _time
        return self.__time

    async def _ensure_time(self):
        if self.__time:
            return self.__time
        return await self.get_time()

    async def get_time_info(self):
        """Get DST Info"""
        await self._ensure_time()
        if TYPE_CHECKING:
            _tz = datetime.now().tzinfo
            if _tz is None:
                raise TypeError()
            self.__timezone = _tz
        return self.__timezone

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

        async for response in self._execute(
            self.commands.create_get_hdd_info_request()
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_get_hdd_info_response(response):
                return response.info

            if self.commands.is_error(response):
                response.throw("Get storage Info failed")

        raise ReolinkResponseError("Get storage Info failed")
