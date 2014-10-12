import unittest
from testfixtures import compare, ShouldRaise
from hangout_api.exceptions import LoginError
from hangout_api.base import _create_hangout_event
from hangout_api.tests.utils import (
    credentials,
    hangout_factory
)


def test_dummy_otp():
    hangout = hangout_factory()
    with ShouldRaise(LoginError):
        hangout.login(
            credentials['name_4'], credentials['password_4'], otp='000000')


class TestHangoutsStart(unittest.TestCase):

    @classmethod
    def setup_class(self):
        self.hangout = hangout_factory()
        self.hangout.login(credentials['name'], credentials['password'])

    @classmethod
    def teardown_class(self):
        del self.hangout

    def teardown(self):
        self.hangout.disconnect()

    def test_regular_hangout(self):
        self.hangout.start()
        compare(self.hangout.hangout_id is None, False)
        compare(self.hangout.on_air is None, True)
        self.hangout.disconnect()

    def test_hangout_onair(self):
        on_air = {'name': 'On Air creation test',
                  'attendees': ['Friends', 'optgilgameshbot@gmail.com']}
        self.hangout.start(on_air=on_air)
        compare(self.hangout.hangout_id is None, False)
        compare(self.hangout.on_air, on_air)
        self.hangout.disconnect()

    def test_hangout_onair_existing_event(self):
        url = _create_hangout_event(
            self.hangout.browser, 'Start OnAir from event URL', ['Friends', ])
        self.hangout.browser.get('http://google.com')
        self.hangout.start(on_air=url)
        compare(self.hangout.hangout_id is None, False)
        compare(self.hangout.on_air, url)
        self.hangout.disconnect()
