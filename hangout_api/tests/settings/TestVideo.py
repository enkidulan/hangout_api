import unittest
from testfixtures import compare
from ..utils import (
    hangout_factory,
    credentials,
    hangouts_connection_manager,
    device_seter
)


class TestVideoSetting(unittest.TestCase):

    @classmethod
    def setup_class(self):
        from hangout_api.tests import HANGOUT
        self.hangout = HANGOUT

    def test_connect(self):
        user = [[credentials['name_2'], credentials['password_2']]]
        with hangouts_connection_manager(user, self.hangout.hangout_id) as nhg:
            new_connection = nhg[0]
            new_connection.browser.xpath(
                '//div[@aria-label="Open menu for John Doe"]', timeout=30)
            # the John Doe is connected
            user_icon = new_connection.browser.xpath(
                '//div[@aria-label="Open menu for John Doe"]')
            compare(user_icon.is_displayed(), True)

    def test_video_mute_unmute_ismuted(self):
        # set up in case if video was muted by previous test
        self.hangout.video.unmute()

        compare(self.hangout.video.is_muted, False)

        compare(self.hangout.video.mute(), True)
        compare(self.hangout.video.mute(), False)

        compare(self.hangout.video.is_muted, True)

        compare(self.hangout.video.unmute(), True)
        compare(self.hangout.video.unmute(), False)

    def test_get_video_devices(self):
        cams = self.hangout.video.get_devices()
        self.assertTrue(isinstance(cams, list))

    def test_set_video_devices(self):
        video_device = device_seter(
            self.hangout.video.get_devices, self.hangout.video.set_device)
        compare(video_device, self.hangout.video.current_device)
