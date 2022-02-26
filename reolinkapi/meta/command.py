""" Command Metaclassed """


class CommandMeta(type):
    """Command Metaclass"""

    def __subclasscheck__(cls, __subclass: type) -> bool:
        return hasattr(__subclass, "command")

    def __instancecheck__(cls, __instance) -> bool:
        return cls.__subclasscheck__(type(__instance))


class CommandInterface(metaclass=CommandMeta):
    """Command Interface"""

    command: str


class CommandRequestInterface(metaclass=CommandMeta):
    """Command Request Interface"""


class CommandResponseInterface(metaclass=CommandMeta):
    """Command Response Interface"""
