import unittest
from testfixtures import compare, ShouldRaise
from hangout_api.utils import Participant
from hangout_api.exceptions import LoginError
from time import sleep
from .utils import (
    credentials,
    hangouts_connection_manager,
    hangout_factory
)


def test_dummy_otp():
    hangout = hangout_factory()
    with ShouldRaise(LoginError):
        hangout.login(
            credentials['name_4'], credentials['password_4'], otp='000000')


class TestBaseAPI(unittest.TestCase):

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
            sleep(5)  # lets give some time to make sure that google add all
            # participants to hangout
            participants = self.hangout.participants()
        compare(
            participants,
            [Participant(name='John Doe',
                         profile_id='108775712935793912532'),
             Participant(name='Lorem Impus',
                         profile_id='115041713348329690244'),
             Participant(name='Gilgamesh Bot',
                         profile_id='108572696173264293426')])
