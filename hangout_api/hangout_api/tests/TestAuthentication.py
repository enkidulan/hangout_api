import os.path
import unittest
from testfixtures import compare, LogCapture
from hangout_api.hangout_api import Hangouts
from hangout_api.hangout_api import LoginError
from testfixtures import ShouldRaise
from yaml import load

credentials = load(open('credentials.yaml', 'r'))


class TestLogIn(unittest.TestCase):

    def test_valid_credentials(self):
        Hangouts(
            credentials['name'],
            credentials['password'],
            otp=credentials['otp'])

    def test_invalid_credentials(self):
        msg = 'Wasn\'t able to login. Check if credentials are correct.'
        with ShouldRaise(LoginError(msg)):
            Hangouts(
                'DoeJohnBot@gmail.com',
                'qwerty')
