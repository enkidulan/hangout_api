import os.path
import unittest
from testfixtures import compare, LogCapture
from hangout_api import Hangouts
from hangout_api import LoginError
from testfixtures import ShouldRaise
from yaml import load
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
from time import sleep
from contextlib import contextmanager


credentials = load(open('credentials.yaml', 'r'))


@contextmanager
def hangouts_connection_manager(users_credentials, hangout_id):
    connections = []
    try:
        for credentials in users_credentials:
            hangout = Hangouts()
            hangout.browser.timeout = 15
            hangout.login(credentials[0], credentials[1])
            hangout.connect(hangout_id)
            connections.append(hangout)
        yield connections
    finally:
        # TODO: won't work sometimes
        for connection in connections:
            del connection


class TestDevicesSettings(unittest.TestCase):

    @classmethod
    def setup_class(self):
        self.hangout = Hangouts()
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
        mics = self.hangout.get_microphone_devices()
        self.assertTrue(len(mics) > 0)

    def test_set_microphone_devices(self):
        mic_device = random.choice(self.hangout.get_microphone_devices())
        self.hangout.set_microphone_devices(mic_device)
        self.hangout.navigate_to_devices_settings()
        current_device = \
            self.hangout.browser.xpath(
                '//span[text()="Microphone"]').parent.get_attribute(
                'innerText').strip()
        compare(mic_device, current_device)

    def test_set_bandwidth(self):
        current_bandwidth = self.hangout.get_bandwidth()
        desired_bandwidth = random.choice(
            [i for i in range(4) if i != current_bandwidth])
        self.hangout.set_bandwidth(desired_bandwidth)
        compare(desired_bandwidth, self.hangout.get_bandwidth())

    def test_get_bandwidth(self):
        current_bandwidth = self.hangout.get_bandwidth()
        compare(current_bandwidth in [0, 1, 2, 3, 4], True)

    def test_get_audio_devices(self):
        audio_devices = self.hangout.get_audio_devices()
        self.assertTrue(len(audio_devices) > 0)

    def test_set_audio_devices(self):
        audio_device = random.choice(self.hangout.get_audio_devices())
        self.hangout.set_audio_devices(audio_device)
        self.hangout.navigate_to_devices_settings()
        current_audio_device = \
            self.hangout.browser.xpath(
                '//div[text()="Play test sound"]').parent.parent.get_attribute(
                'innerText').split('\n')[0].strip()
        compare(audio_device, current_audio_device)

    def test_audio_mute_unmute(self):
        # set up in case if video was muted by previous test
        self.hangout.unmute_audio()

        compare(self.hangout.mute_audio(), True)
        compare(self.hangout.mute_audio(), False)
        compare(self.hangout.unmute_audio(), True)
        compare(self.hangout.unmute_audio(), False)

    def test_video_mute_unmute(self):
        # set up in case if video was muted by previous test
        self.hangout.unmute_video()

        compare(self.hangout.mute_video(), True)
        compare(self.hangout.mute_video(), False)
        compare(self.hangout.unmute_video(), True)
        compare(self.hangout.unmute_video(), False)

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

    # def test_get_video_devices(self):
    #     raise
    #     cams = self.hangout.get_video_devices()
    #     self.assertTrue(len(cams) > 0)

    # def test_set_video_devices(self):
    #     raise
    #     video_device = random.choice(self.hangout.get_video_devices())
    #     self.hangout.set_video_devices(video_device)
    #     self.hangout.navigate_to_devices_settings()
    #     xpath = '//div[contains(@id, ".yt")]//span[@role="option"]'
    #     current_device = \
    #         self.hangout.browser.xpath(xpath).get_attribute('innerText')
    #     compare(video_device, current_device)

# class TestLogIn(unittest.TestCase):

#     def test_valid_credentials(self):
#         hangout = Hangouts()
#         if not hangout.is_logged_in:
#             hangout.login(
#                 credentials['name'],
#                 credentials['password'],
#                 otp=credentials['otp'])
#         hangout.start()

#     def test_invalid_credentials(self):
#         msg = 'Wasn\'t able to login. Check if credentials are correct.'
#         hangout = Hangouts()
#         with ShouldRaise(LoginError(msg)):
#             hangout.login(
#                 'DoeJohnBot@gmail.com',
#                 'qwerty')
