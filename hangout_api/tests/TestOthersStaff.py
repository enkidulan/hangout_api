from hangout_api.exceptions import LoginError
from testfixtures import ShouldRaise
from hangout_api.tests.utils import (
    credentials,
    hangouts_connection_manager,
    hangout_factory
)


def test_dummy_otp():
    hangout = hangout_factory()
    with ShouldRaise(LoginError):
        hangout.login(
            credentials['name_4'], credentials['password_4'], otp='000000')
