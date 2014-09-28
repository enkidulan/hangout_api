from hangout_api import Hangouts
from yaml import load
import random
from contextlib import contextmanager


def hangout_factory():
    return Hangouts()

credentials = load(open('credentials.yaml', 'r'))


def device_seter(dev_getter, dev_setter):
    device = dev_getter()
    if isinstance(device, list):
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
            hangout.browser.timeout = 15
            hangout.login(credentials[0], credentials[1])
            hangout.connect(hangout_id)
            connections.append(hangout)
        yield connections
    finally:
        for connection in connections:
            try:
                connection.__del__()
            except:
                pass
