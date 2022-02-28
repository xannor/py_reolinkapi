""" Rest API client """

from .network import Network
from .connection import Connection
from .security import Security
from .system import System
from .video import Video
from .encoding import Encoding
from .record import Record


class Client(Connection, Security, System, Network, Video, Encoding, Record):
    """Rest API Client"""

    def __init__(self) -> None:
        """not usless"""
        super().__init__()
