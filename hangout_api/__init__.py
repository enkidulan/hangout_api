"""
Python API for controlling Google+ Hangouts
===========================================
"""

# Mocking retry for tests
#


def retry_mock(**_):
    """
    Decorator context handler for gadgets.
    It makes sure that current browser context is set to work with
    provided PlugIn.
    """
    def decorator(function):  # pylint: disable=C0111
        def wrapper(self, *args, **kwargs):  # pylint: disable=C0111
            return function(self, *args, **kwargs)
        return wrapper
    return decorator

# from testfixtures import Replacer
# r = Replacer()
# r.replace('retrying.retry', retry_mock)

from .base import Hangouts
from hangout_api import settings
from hangout_api import gadgets
