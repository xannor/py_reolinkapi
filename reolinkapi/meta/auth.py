""" Authentication Metaclasses """


class AuthenticationMeta(type):
    """Authentication Metaclass"""

    def __subclasscheck__(cls, subcls: type) -> bool:
        return hasattr(subcls, "_get_auth_token") and callable(subcls._get_auth_token)

    def __instancecheck__(cls, inst: any) -> bool:
        return cls.__subclasscheck__(type(inst))


class AuthenticationInterface(metaclass=AuthenticationMeta):
    """Authentication Interface"""

    def _get_auth_token(self) -> any:
        """get token"""
