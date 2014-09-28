import unittest
from testfixtures import compare


class TestToolboxApp(unittest.TestCase):

    @classmethod
    def setup_class(self):
        from hangout_api.tests import HANGOUT
        self.hangout = HANGOUT

    def test_lower_third_settings(self):
        self.hangout.toolbox.lower_third(
            name="J.R. Dou",
            tags="hangout api bot",
            logo='file.png',
            color="#55bbgg")
        raise

    def test_lower_third_active(self):
        self.hangout.toolbox.lower_third_active(True)
        compare(self.hangout.toolbox.lower_third_active(), True)

        self.hangout.toolbox.lower_third_active(False)
        compare(self.hangout.toolbox.lower_third_active(), False)
        self.hangout.toolbox.lower_third_active(False)
        compare(self.hangout.toolbox.lower_third_active(), False)
        self.hangout.toolbox.lower_third_active(True)
        compare(self.hangout.toolbox.lower_third_active(), True)
        self.hangout.toolbox.lower_third_active(True)
        compare(self.hangout.toolbox.lower_third_active(), True)

    def test_custom_overlay(self):
        self.hangout.toolbox.custom_overlay(file="overlay.png")
        raise

    def test_video_mirror_active(self):
        self.hangout.toolbox.video_mirror_active(True)
        compare(self.hangout.toolbox.video_mirror_active(), True)

        self.hangout.toolbox.video_mirror_active(False)
        compare(self.hangout.toolbox.video_mirror_active(), False)
        self.hangout.toolbox.video_mirror_active(True)
        compare(self.hangout.toolbox.video_mirror_active(), True)
