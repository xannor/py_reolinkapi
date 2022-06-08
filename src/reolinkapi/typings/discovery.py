"""Discovery typings"""

from typing import TypedDict
from typing_extensions import NotRequired


class Device(TypedDict):
    """Discovered Device"""

    ip: str
    mac: str
    name: NotRequired[str]
    ident: NotRequired[str]
    uuid: NotRequired[str]
