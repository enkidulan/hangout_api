import operator
import unittest
from testfixtures import compare, ShouldRaise
from hangout_api.utils import Participant
from time import sleep
from .utils import (
    credentials,
    hangouts_connection_manager,
    hangout_factory
)


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
        xpath = '//*[text()="Invitation posted"'\
                'or text()="Waiting for people to join this video call..."]'
        waiting_message = self.hangout.browser.xpath(xpath)
        compare(waiting_message.is_displayed(), True)

    def test_participants(self):
        # raise NotImplementedError()
        self.hangout.invite(['maxybot@gmail.com'])

        users = [[credentials['name_2'], credentials['password_2']],
                 [credentials['name_3'], credentials['password_3']]]
        with hangouts_connection_manager(users, self.hangout.hangout_id):
            sleep(10)  # lets give some time to make sure that google add all
            # participants to hangout
            participants = self.hangout.participants()
        participants.sort(key=operator.attrgetter('profile_id'))
        compare(
            participants,
            [Participant(profile_id='108572696173264293426',
                         name='Gilgamesh Bot'),
             Participant(profile_id='108775712935793912532',
                         name='John Doe'),
             Participant(profile_id='115041713348329690244',
                         name='Lorem Impus')])
