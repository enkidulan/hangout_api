from hangout_api import Hangouts
from yaml import load
import random
from contextlib import contextmanager
import os
from selenium.webdriver.chrome.options import Options


def hangout_factory():
    # if os.environ.get('DISPLAY'):
    #     del os.environ['DISPLAY']
    chrome_options = Options()
    if 'TRAVIS' in os.environ:
        chrome_options.add_argument('--no-sandbox')
    hangout = Hangouts(chrome_options=chrome_options)
    # hangout.browser.timeout = 60
    return hangout


credentials = load(open(
    os.path.join(os.path.dirname(__file__), 'resources', 'credentials.yaml'),
    'r'))


def device_seter(dev_getter, dev_setter):
    device = dev_getter()
    if not device:
        return
    if isinstance(device, list) or isinstance(device, tuple):
        # we can't set device if there is no devices to choose
        # TODO: maybe it would be better to skip this test if no devices
        device = random.choice(device)
        dev_setter(device)
    return device


@contextmanager
def hangouts_connection_manager(users_credentials, hangout_id):
    connections = []
    try:
        for credentials in users_credentials:
            hangout = hangout_factory()
            hangout.login(credentials[0], credentials[1])
            hangout.connect(hangout_id)
            connections.append(hangout)
        yield connections
    finally:
        for connection in connections:
            del connection
