import unittest
from testfixtures import compare
from hangout_api.utils import Participant
from time import sleep
from .utils import (
    credentials,
    hangouts_connection_manager,
    hangout_factory
)
from hangout_api import Hangouts


class TestBroadcast(unittest.TestCase):

    @classmethod
    def setup_class(self):
        self.on_air = {
            'name': 'test',
            'attendees': 'Friends',
        }
        self.hangout = hangout_factory()
        self.hangout.start(on_air=self.on_air)

    @classmethod
    def teardown_class(self):
        del self.hangout

    def test_all(self):
        compare(self.hangout.broadcast.is_on(), False)
        self.hangout.broadcast.start()
        compare(self.hangout.broadcast.is_on(), True)
        self.hangout.broadcast.stop()
        compare(self.hangout.broadcast.is_on(), False)
        compare(len(self.hangout.broadcast.embed_url()) > 20, True)
        self.hangout.disconnect()
        compare(getattr(self.hangout, 'broadcast', None), None)


class TestCameraman(unittest.TestCase):

    @classmethod
    def setup_class(self):
        self.on_air = {
            'name': 'test',
            'attendees': 'Friends',
        }
        self.hangout = Hangouts()
        self.hangout.login(
            credentials['name'],
            credentials['password'],
            otp=credentials['otp'])
        self.hangout.start(on_air=self.on_air)

    @classmethod
    def teardown_class(self):
        del self.hangout

    def test_mute_new_guests(self):
        self.hangout.cameraman.mute_new_guests(False)

        compare(self.hangout.cameraman.mute_new_guests(True), True)
        compare(self.hangout.cameraman.mute_new_guests(True), False)
        compare(self.hangout.cameraman.mute_new_guests(), True)

        compare(self.hangout.cameraman.mute_new_guests(False), True)
        compare(self.hangout.cameraman.mute_new_guests(False), False)
        compare(self.hangout.cameraman.mute_new_guests(), False)

    def test_video_only(self):
        self.hangout.cameraman.video_only(False)

        compare(self.hangout.cameraman.video_only(True), True)
        compare(self.hangout.cameraman.video_only(True), False)
        compare(self.hangout.cameraman.video_only(), True)

        compare(self.hangout.cameraman.video_only(False), True)
        compare(self.hangout.cameraman.video_only(False), False)
        compare(self.hangout.cameraman.video_only(), False)

    def test_hide_new_guests(self):
        self.hangout.cameraman.hide_new_guests(False)

        compare(self.hangout.cameraman.hide_new_guests(True), True)
        compare(self.hangout.cameraman.hide_new_guests(True), False)
        compare(self.hangout.cameraman.hide_new_guests(), True)

        compare(self.hangout.cameraman.hide_new_guests(False), True)
        compare(self.hangout.cameraman.hide_new_guests(False), False)
        compare(self.hangout.cameraman.hide_new_guests(), False)
