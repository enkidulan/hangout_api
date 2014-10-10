import unittest
from testfixtures import compare
import random
from hangout_api.settings.bandwidth import BANDWIDTH_LEVELS
from ..utils import (
    hangout_factory,
    credentials,
)


class TestBandwidthSettings(unittest.TestCase):

    @classmethod
    def setup_class(self):
        from hangout_api.tests import HANGOUT
        self.hangout = HANGOUT

    def test_set_bandwidth(self):
        current_bandwidth = self.hangout.bandwidth.get()
        desired_bandwidth = random.choice(
            [i for i in range(2, 4) if i != current_bandwidth])
        self.hangout.bandwidth.set(desired_bandwidth)
        compare(
            BANDWIDTH_LEVELS(desired_bandwidth), self.hangout.bandwidth.get())

    def test_get_bandwidth(self):
        current_bandwidth = self.hangout.bandwidth.get()
        compare(current_bandwidth in BANDWIDTH_LEVELS, True)
