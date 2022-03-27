""" Rest API client """

from ..base.led import LED
from ..base.network import Network
from .connection import Connection, SessionFactory
from .security import Security
from .encrypt import Encrypt
from ..base.system import System
from ..base.video import Video
from ..base.encoding import Encoding
from .record import Record
from ..base.alarm import Alarm
from ..base.ai import AI


class Client(
    Connection,
    Security,
    Encrypt,
    System,
    Network,
    Video,
    Encoding,
    Record,
    Alarm,
    AI,
    LED,
):
    """Rest API Client"""

    def __init__(self, session_factory: SessionFactory = None) -> None:
        super().__init__(session_factory=session_factory)
