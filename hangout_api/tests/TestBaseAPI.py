import unittest
from testfixtures import compare
from hangout_api import Hangouts
# from hangout_api.exceptions import LoginError
# from testfixtures import ShouldRaise
from yaml import load
import random
from time import sleep
from contextlib import contextmanager


def hangout_factory():
    return Hangouts()

credentials = load(open('credentials.yaml', 'r'))


def device_seter(dev_getter, dev_setter):
    device = dev_getter()
    if isinstance(device, list):
        # we can't set device if there is no devices to choose
        # TODO: maybe it would be better to skip this test if no devices
        device = random.choice(device)
        dev_setter(device)
    return device


@contextmanager
def hangouts_connection_manager(users_credentials, hangout_id):
    connections = []
    try:
        for credentials in users_credentials:
            hangout = hangout_factory()
            hangout.browser.timeout = 15
            hangout.login(credentials[0], credentials[1])
            hangout.connect(hangout_id)
            connections.append(hangout)
        yield connections
    finally:
        for connection in connections:
            try:
                connection.__del__()
            except:
                pass


class TestBaseAPI(unittest.TestCase):

    @classmethod
    def setup_class(self):
        self.hangout = hangout_factory()
        self.hangout.browser.timeout = 15
        self.hangout.login(
            credentials['name'],
            credentials['password'],
            otp=credentials['otp'])
        self.hangout.start()

    @classmethod
    def teardown_class(self):
        self.hangout.__del__()

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

    def test_get_microphone_devices(self):
        mics = self.hangout.microphone.get_devices()
        self.assertTrue(len(mics) > 0)

    def test_set_microphone_devices(self):
        mic_device = device_seter(
            self.hangout.microphone.get_devices,
            self.hangout.microphone.set_device)
        self.hangout.utils.navigate_to_devices_settings()
        current_device = \
            self.hangout.browser.xpath(
                '//span[text()="Microphone"]').parent.get_attribute(
                'innerText').strip()
        compare(mic_device, current_device)

    def test_set_bandwidth(self):
        current_bandwidth = self.hangout.bandwidth.get()
        desired_bandwidth = random.choice(
            [i for i in range(4) if i != current_bandwidth])
        self.hangout.bandwidth.set(desired_bandwidth)
        compare(desired_bandwidth, self.hangout.bandwidth.get())

    def test_get_bandwidth(self):
        current_bandwidth = self.hangout.bandwidth.get()
        compare(current_bandwidth in [0, 1, 2, 3, 4], True)

    def test_get_audio_devices(self):
        audio_devices = self.hangout.audio.get_devices()
        self.assertTrue(len(audio_devices) > 0)

    def test_set_audio_devices(self):
        audio_device = device_seter(
            self.hangout.audio.get_devices, self.hangout.audio.set_device)
        self.hangout.utils.navigate_to_devices_settings()
        current_audio_device = \
            self.hangout.browser.xpath(
                '//div[text()="Play test sound"]').parent.parent.get_attribute(
                'innerText').split('\n')[0].strip()
        compare(audio_device, current_audio_device)

    def test_audio_mute_unmute(self):
        # set up in case if video was muted by previous test
        self.hangout.audio.unmute()

        compare(self.hangout.audio.mute(), True)
        compare(self.hangout.audio.mute(), False)
        compare(self.hangout.audio.unmute(), True)
        compare(self.hangout.audio.unmute(), False)

    def test_video_mute_unmute(self):
        # set up in case if video was muted by previous test
        self.hangout.video.unmute()

        compare(self.hangout.video.mute(), True)
        compare(self.hangout.video.mute(), False)
        compare(self.hangout.video.unmute(), True)
        compare(self.hangout.video.unmute(), False)

    def test_invite(self):
        self.hangout.invite(['maxybot@gmail.com', 'test circle for call'])
        waiting_message = self.hangout.browser.by_text(
            'Waiting for people to join this video call...')
        compare(waiting_message.is_displayed(), True)

    def test_participants(self):
        # raise NotImplementedError()
        self.hangout.invite(['maxybot@gmail.com'])

        users = [[credentials['name_2'], credentials['password_2']],
                 [credentials['name_3'], credentials['password_3']]]
        with hangouts_connection_manager(users, self.hangout.hangout_id):
            sleep(3)  # lets give some time to make sure that google add all
            # participants to hangout
            participants = self.hangout.participants()
        compare(participants, ['Gilgamesh Bot', 'Lorem Impus', 'John Doe'])

    def test_get_video_devices(self):
        cams = self.hangout.video.get_devices()
        self.assertTrue(isinstance(cams, list) or isinstance(cams, str))

    def test_set_video_devices(self):
        video_device = device_seter(
            self.hangout.video.get_devices, self.hangout.video.set_device)
        self.hangout.utils.navigate_to_devices_settings()
        current_device = \
            self.hangout.browser.by_text(
                'Video and Camera').parent.parent.get_attribute(
                'innerText').split('\n')[0].strip()
        compare(video_device, current_device)
