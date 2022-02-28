"""Record command"""

from dataclasses import dataclass, field
import random
import string
from typing import ClassVar

from reolinkapi.utils.dataclasses import keyword

from .command import CommandRequest, CommandRequestChannelParam, CommandStreamResponse
from ..meta.connection import ConnectionInterface

_rnd = random.SystemRandom()
_rnd_set = string.printable


@dataclass
class SnapshotRequestParam(CommandRequestChannelParam):
    """Snapshot Request Param"""

    _seed: str = field(init=False, metadata=keyword("rs"))

    def __post_init__(self):
        self._seed = "".join(_rnd.choice(_rnd_set) for _ in range(16))


@dataclass
class SnapshotRequest(CommandRequest):
    """Snapshot Request"""

    COMMAND: ClassVar = "Snap"
    param: SnapshotRequestParam = field(default_factory=SnapshotRequestParam)

    def __post_init__(self):
        self.command = type(self).COMMAND


class Record:
    """Record Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self, ConnectionInterface) and not hasattr(self, "_execute"):
            # type "interface"
            self._execute = self._execute

    async def get_snap(self, channel: int = 0):
        """get snapshot"""
        results = await self._execute(
            SnapshotRequest(SnapshotRequestParam(channel)), get=True
        )
        if len(results) != 1 or not isinstance(results[0], CommandStreamResponse):
            return None

        return (results[0].stream, results[0].attributes)
