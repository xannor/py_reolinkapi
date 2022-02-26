""" Rest API client """

from .connection import Connection
from .auth import Authentication
from .system import System


class Client(Connection, Authentication, System):
    """Rest API Client"""

    def __init__(self) -> None:
        """not usless"""
        super().__init__()
