""" System Mixin """
from __future__ import annotations
from datetime import datetime

from reolinkapi.typings.system import TimeValueInfo

from . import connection

from ..helpers import system as systemHelpers


class System:
    """System Commands Mixin"""

    def __init__(self) -> None:
        self.__timeinfo: TimeValueInfo | None = None
        self.__time: datetime | None = None

        if isinstance(self, connection.Connection):
            self._disconnect_callbacks.append(self.__clear)

    def __clear(self):
        self.__timeinfo = None
        self.__time = None

    async def get_ability(self, username: str | None = None):
        """Get User Permisions"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(systemHelpers.create_get_ability(username))
        else:
            return None

        return next(systemHelpers.get_ability_responses(responses), None)

    async def get_device_info(self):
        """Get Device Information"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(systemHelpers.create_get_device_info())
        else:
            return None

        return next(systemHelpers.get_devinfo_responses(responses), None)

    async def get_time(self):
        """Get Device Time Information"""

        self.__clear()
        if isinstance(self, connection.Connection):
            responses = await self._execute(systemHelpers.create_get_time())
        else:
            return None
        time = next(systemHelpers.get_time_responses(responses), None)
        if time is not None:
            self.__timeinfo = time["Time"]
            self.__time = systemHelpers.as_dateime(
                time["Time"], tzinfo=systemHelpers.get_tzinfo(time)
            )

        return self.__time

    async def _ensure_time(self):
        if self.__time is None:
            return await self.get_time()
        return self.__time

    async def get_time_info(self):
        """Get DST Info"""
        await self.get_time()
        return self.__timeinfo
