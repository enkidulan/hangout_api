import unittest
from testfixtures import compare


class TestCameraman(unittest.TestCase):

    @classmethod
    def setup_class(self):
        from hangout_api.tests import HANGOUT
        self.hangout = HANGOUT

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
