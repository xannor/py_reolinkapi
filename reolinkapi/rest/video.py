""" Video Commands """

from dataclasses import dataclass, field
from email.policy import default
from typing import ClassVar

from ..utils.dataclasses import keyword

from .command import (
    CommandRequest,
    CommandRequestParameter,
    CommandValueResponse,
    CommandValueResponseValue,
    response_type,
)
from ..meta.connection import ConnectionInterface


class Video:
    """Video Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self, ConnectionInterface) and not hasattr(self, "_execute"):
            # type "interface"
            self._execute = self._execute
