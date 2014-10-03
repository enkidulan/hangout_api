import unittest
from testfixtures import compare
from ..utils import (
    hangout_factory,
    credentials,
    hangouts_connection_manager,
    device_seter
)


class TestMicrophoneSettings(unittest.TestCase):

    @classmethod
    def setup_class(self):
        from hangout_api.tests import HANGOUT
        self.hangout = HANGOUT

    def test_get_microphone_devices(self):
        mics = self.hangout.microphone.get_devices()
        self.assertTrue(isinstance(mics, list))

    def test_set_microphone_devices(self):
        mic_device = device_seter(
            self.hangout.microphone.get_devices,
            self.hangout.microphone.set_device)
        if mic_device is None:
            self.skipTest('No devices to set')
        compare(mic_device, self.hangout.microphone.current_device)

    def test_microphone_mute_unmute_ismuted(self):
        # set up in case if microphone was muted by previous test
        self.hangout.microphone.unmute()

        compare(self.hangout.microphone.is_muted, False)

        compare(self.hangout.microphone.mute(), True)
        compare(self.hangout.microphone.mute(), False)

        compare(self.hangout.microphone.is_muted, True)

        compare(self.hangout.microphone.unmute(), True)
        compare(self.hangout.microphone.unmute(), False)
