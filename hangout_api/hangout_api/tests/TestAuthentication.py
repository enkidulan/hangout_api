import os.path
import unittest
from testfixtures import compare, LogCapture
from hangout_api.hangout_api import Hangouts
from hangout_api.hangout_api import LoginError
from testfixtures import ShouldRaise
from yaml import load
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random


credentials = load(open('credentials.yaml', 'r'))


class TestMicrophoneDevices(unittest.TestCase):

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

    def test_get_microphone_devices(self):
        mics = self.hangout.get_microphone_devices()
        self.assertTrue(len(mics) > 0)

    def test_set_microphone_devices(self):
        mic_device = random.choice(self.hangout.get_microphone_devices())
        self.hangout.set_microphone_devices(mic_device)
        self.hangout.navigate_to_devices_settings()
        xpath = '//div[contains(@id, ".yt")]//span[@role="option"]'
        current_device = \
            self.hangout.browser.xpath(xpath).get_attribute('innerText')
        compare(mic_device, current_device)

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
