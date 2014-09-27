"""
Exceptions for Hangout API
"""


class LoginError(BaseException):
    """
    Hangout Exception which rises in case of any problems with user log in
    procedure
    """
    pass


class NoSuchDeviceFound(BaseException):
    """
    Hangout Exception which rises in case if user tries to set not available
    device
    """
    pass
