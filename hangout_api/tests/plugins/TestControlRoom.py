import os.environ
import unittest
from testfixtures import compare
from hangout_api.tests.utils import (
    credentials,
    hangout_factory
)


class TestControlRoom(unittest.TestCase):

    @classmethod
    def setup_class(self):
        from hangout_api.tests import HANGOUT
        self.hangout = HANGOUT
        self.participant = hangout_factory()
        self.participant.login(
            credentials['name_2'], credentials['password_2'])
        self.participant.connect(self.hangout.hangout_id)

    @classmethod
    def teardown_class(self):
        del self.participant

    def test_audio(self):
        if 'TRAVIS' in os.environ:
            self.skipTest('Skip this test on travis')

        self.hangout.controlroom.audio('Lorem Impus', False)

        compare(self.hangout.controlroom.audio('Lorem Impus', True), True)
        compare(self.hangout.controlroom.audio('Lorem Impus', True), False)
        compare(self.hangout.controlroom.audio('Lorem Impus', ), True)

        compare(self.hangout.controlroom.audio('Lorem Impus', False), True)
        compare(self.hangout.controlroom.audio('Lorem Impus', False), False)
        compare(self.hangout.controlroom.audio('Lorem Impus', ), False)

    def test_video(self):
        if 'TRAVIS' in os.environ:
            self.skipTest('Skip this test on travis')

        self.hangout.controlroom.video('Lorem Impus', False)

        compare(self.hangout.controlroom.video('Lorem Impus', True), True)
        compare(self.hangout.controlroom.video('Lorem Impus', True), False)
        compare(self.hangout.controlroom.video('Lorem Impus', ), True)

        compare(self.hangout.controlroom.video('Lorem Impus', False), True)
        compare(self.hangout.controlroom.video('Lorem Impus', False), False)
        compare(self.hangout.controlroom.video('Lorem Impus', ), False)
