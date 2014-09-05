*******************************
User stories for Hangout API
*******************************

This stories is actual tests.

.. testsetup:: base_api

    from yaml import load
    credentials = load(open('credentials.yaml', 'r'))

    from hangout_api.hangout_api import Hangouts
    hangout = Hangouts()
    hangout.browser.timeout = 15
    hangout.login(credentials['name'], credentials['password'], otp=credentials['otp'])
    hangout.start()

.. doctest:: base_api

   >>> hangout.get_bandwidth() in [0, 1, 2, 3, 4]
   True

.. doctest:: base_api

    >>> len(hangout.get_audio_devices()) > 0
    True

.. testcleanup:: base_api

    del hangout
