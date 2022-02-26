""" Base """

from typing import ClassVar, Mapping

from .command import CommandResponse
from ..abc.base import Base as _Base


class Base(_Base):
    """Base Mixin"""

    __command_response_types: ClassVar[Mapping[str, type[CommandResponse]]] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for _type in cls.__bases__:


    def __init__(self):
        self._command_response_types = type(self)
