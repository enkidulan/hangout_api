import os
import unittest
from testfixtures import compare


class TestControlRoom(unittest.TestCase):

    @classmethod
    def setup_class(self):
        from hangout_api.tests import HANGOUT
        self.hangout = HANGOUT

    def test_audio(self):
        if 'TRAVIS' in os.environ:
            self.skipTest('Skip this test on travis')

        self.hangout.controlroom.audio('John Doe', False)

        compare(self.hangout.controlroom.audio('John Doe', True), True)
        compare(self.hangout.controlroom.audio('John Doe', True), False)
        compare(self.hangout.controlroom.audio('John Doe', ), True)

        compare(self.hangout.controlroom.audio('John Doe', False), True)
        compare(self.hangout.controlroom.audio('John Doe', False), False)
        compare(self.hangout.controlroom.audio('John Doe', ), False)

    def test_video(self):
        if 'TRAVIS' in os.environ:
            self.skipTest('Skip this test on travis')

        self.hangout.controlroom.video('John Doe', False)

        compare(self.hangout.controlroom.video('John Doe', True), True)
        compare(self.hangout.controlroom.video('John Doe', True), False)
        compare(self.hangout.controlroom.video('John Doe', ), True)

        compare(self.hangout.controlroom.video('John Doe', False), True)
        compare(self.hangout.controlroom.video('John Doe', False), False)
        compare(self.hangout.controlroom.video('John Doe', ), False)
