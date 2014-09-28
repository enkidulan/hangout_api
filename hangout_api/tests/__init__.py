from .utils import hangout_factory, credentials

HANGOUT = None


def setup_package():
    global HANGOUT
    HANGOUT = hangout_factory()
    HANGOUT.browser.timeout = 15
    HANGOUT.login(
        credentials['name'],
        credentials['password'],
        otp=credentials['otp'])
    HANGOUT.start()


def teardown_package():
    HANGOUT.__del__()
