import unittest
from testfixtures import compare


class TestBroadcast(unittest.TestCase):

    @classmethod
    def setup_class(self):
        from ..utils import hangout_factory, credentials
        on_air = {
            'name': 'test',
            'attendees': 'Friends'}
        self.hangout = hangout_factory()
        self.hangout.login(
            credentials['name'],
            credentials['password'],
            otp=credentials['otp'])
        self.hangout.start(on_air=on_air)

    @classmethod
    def teardown_class(self):
        del self.hangout

    def test_all(self):
        compare(self.hangout.broadcast.is_on(), False)
        self.hangout.broadcast.start()
        compare(self.hangout.broadcast.is_on(), True)
        compare(len(self.hangout.broadcast.embed_url()) > 20, True)
        self.hangout.broadcast.stop()
        compare(self.hangout.broadcast.is_on(), False)
        self.hangout.disconnect()
        compare(getattr(self.hangout, 'broadcast', None), None)
