""" Connection Metaclasses """

from typing import Callable, Optional

import aiohttp

from .command import CommandRequestInterface, CommandResponseInterface


class ConnectionMeta(type):
    """Connection Metaclass"""

    def __subclasscheck__(cls, subcls) -> bool:
        return (
            hasattr(subcls, "_get_disconnect_callbacks")
            and callable(subcls._get_disconnect_callbacks)
            and hasattr(subcls, "_ensure_connection")
            and callable(subcls._ensure_connection)
            and hasattr(subcls, "_execute")
            and callable(subcls._execute)
        )

    def __instancecheck__(cls, inst) -> bool:
        return cls.__subclasscheck__(type(inst))


class ConnectionInterface(metaclass=ConnectionMeta):
    """Connection Interface"""

    def _get_disconnect_callbacks(self) -> list[Callable[[], None]]:
        """callbacks"""

    def _ensure_connection(self) -> bool:
        """Ensure Connection"""

    async def _execute(
        self, *args: CommandRequestInterface, **kwargs
    ) -> list[CommandResponseInterface]:
        """Execute Command"""
