import json
from typing import Generic, TypeVar

from reolinkapi.meta.command import CommandRequestInterface, CommandResponseInterface
from reolinkapi.rest.command import get_response_type
from reolinkapi.utils.dataclasses import DataclassesJSONEncoder, fromdict

jsonEnc = DataclassesJSONEncoder()

_T = TypeVar("_T", bound=dict[type, str])


class MockConnection(Generic[_T]):
    """Mocked Connection"""

    JSON: _T

    def __init__(self) -> None:
        self._disconnect_callbacks = []
        super().__init__()

    def _get_disconnect_callbacks(self):
        """mocked callbacks"""
        return self._disconnect_callbacks

    def _ensure_connection(self) -> bool:
        """mocked ensure connect"""
        return True

    async def _execute(
        self, *args: CommandRequestInterface
    ) -> list[CommandResponseInterface]:
        """mocked _execue"""
        _json = jsonEnc.encode(args)
        assert _json == type(self).JSON[type(args[0])], (
            "unexpected json of `%s`" % _json
        )
        _type = get_response_type(type(args[0]))

        data = json.loads(type(self).JSON[_type])
        return [fromdict(data[0], _type)]
