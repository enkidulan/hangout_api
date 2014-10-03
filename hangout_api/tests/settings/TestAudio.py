import unittest
from testfixtures import compare
from ..utils import (
    hangout_factory,
    credentials,
    device_seter
)


class TestAudioSettings(unittest.TestCase):

    @classmethod
    def setup_class(self):
        from hangout_api.tests import HANGOUT
        self.hangout = HANGOUT

    def test_get_audio_devices(self):
        audio_devices = self.hangout.audio.get_devices()
        self.assertTrue(
            isinstance(audio_devices, list))

    def test_set_audio_devices(self):
        audio_device = device_seter(
            self.hangout.audio.get_devices, self.hangout.audio.set_device)
        if audio_device is None:
            self.skipTest('No devices to set')
        compare(audio_device, self.hangout.audio.current_device)
