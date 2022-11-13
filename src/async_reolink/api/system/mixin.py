"""System"""
from __future__ import annotations
from abc import ABC, abstractmethod

from typing import TypeGuard

from ..connection.model import Response, ErrorResponse
from ..connection.part import Connection as ConnectionPart
from ..security.part import Security as SecurityPart
from ..errors import ReolinkResponseError
from .part import System as SystemPart
from .capabilities import Capabilities
from .model import NO_CAPABILITY, NO_DEVICEINFO
from .typing import DeviceInfo

from . import command


class System(ConnectionPart, SystemPart, SecurityPart, ABC):
    """System Commands Mixin"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @abstractmethod
    def _create_get_capabilities(self, username: str | None) -> command.GetAbilitiesRequest:
        ...

    @abstractmethod
    def _is_get_capabilities_response(
        self, response: Response
    ) -> TypeGuard[command.GetAbilitiesResponse]:
        ...

    async def get_capabilities(self, username: str | None = None) -> Capabilities:
        """Get User Permisions"""

        async for response in self._execute(self._create_get_capabilities(username)):
            if not isinstance(response, Response):
                break

            if self._is_get_capabilities_response(response):
                return response.capabilities

            if isinstance(response, ErrorResponse):
                response.throw("Get capabilities failed")

        return NO_CAPABILITY

    @abstractmethod
    def _create_get_device_info(self) -> command.GetDeviceInfoRequest:
        ...

    @abstractmethod
    def _is_get_device_info_response(
        self, response: Response
    ) -> TypeGuard[command.GetDeviceInfoResponse]:
        ...

    async def get_device_info(self) -> DeviceInfo:
        """Get Device Information"""

        async for response in self._execute(self._create_get_device_info()):
            if not isinstance(response, Response):
                break

            if self._is_get_device_info_response(response):
                return response.info

            if isinstance(response, ErrorResponse):
                response.throw("Get device info failed")

        return NO_DEVICEINFO

    @abstractmethod
    def _create_get_time(self) -> command.GetTimeRequest:
        ...

    @abstractmethod
    def _is_get_time_response(self, response: Response) -> TypeGuard[command.GetTimeResponse]:
        ...

    async def _get_time(self):
        async for response in self._execute(self._create_get_time()):
            if not isinstance(response, Response):
                break

            if self._is_get_time_response(response):
                return response

            if isinstance(response, ErrorResponse):
                response.throw("Get time failed")

        raise ReolinkResponseError("Get Time failed")

    async def get_time(self):
        """Get Device Time Information"""

        return (await self._get_time()).to_datetime()

    async def get_time_info(self):
        """Get DST Info"""

        return (await self._get_time()).to_timezone()

    @abstractmethod
    def _create_reboot(self) -> command.RebootRequest:
        ...

    async def reboot(self):
        """Reboot device"""

        async for response in self._execute(self._create_reboot()):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Reboot failed")

            if self._is_success_response(response):
                return

        raise ReolinkResponseError("Reboot failed")

    @abstractmethod
    def _create_get_hdd_info(self) -> command.GetHddInfoRequest:
        ...

    @abstractmethod
    def _is_get_hdd_info_response(
        self, response: Response
    ) -> TypeGuard[command.GetHddInfoResponse]:
        ...

    async def get_storage_info(self):
        """Get Device Recording Capabilities"""

        async for response in self._execute(self._create_get_hdd_info()):
            if not isinstance(response, Response):
                break

            if self._is_get_hdd_info_response(response):
                return response.info

            if isinstance(response, ErrorResponse):
                response.throw("Get storage Info failed")

        raise ReolinkResponseError("Get storage Info failed")
