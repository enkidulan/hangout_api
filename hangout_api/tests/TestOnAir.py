import unittest
from testfixtures import compare
from hangout_api.utils import Participant
from time import sleep
from .utils import (
    credentials,
    hangouts_connection_manager,
)
from hangout_api import Hangouts


class TestBroadcast(unittest.TestCase):

    @classmethod
    def setup_class(self):
        self.on_air = {
            'name': 'test',
            'attendies': 'Friends',
        }
        self.hangout = Hangouts()
        self.hangout.login(
            credentials['name'],
            credentials['password'],
            otp=credentials['otp'])
        self.hangout.start(on_air=self.on_air)

    @classmethod
    def teardown_class(self):
        if self.hangout.broadcast.on():
            self.hangout.broadcast.stop()
        del self.hangout

    def test_all(self):
        self.hangout.broadcast.start()
        compare(self.hangout.broadcast.on(), True)
        self.hangout.broadcast.stop()
        compare(self.hangout.broadcast.on(), False)
        compare(len(self.hangout.broadcast.embed_url()) > 20, True)
