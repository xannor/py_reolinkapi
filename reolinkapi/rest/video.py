""" Video Commands """

from typing import TypedDict
from .connection import Connection


class Video:
    """Video Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self, Connection) and not hasattr(self, "_execute"):
            # type "interface"
            self._execute = self._execute
