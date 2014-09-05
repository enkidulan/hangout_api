*******************************
User stories for Hangout API
*******************************

This stories is actual tests.


How to create new hangout and invite people?
============================================

.. testsetup:: base_api

    from yaml import load
    credentials = load(open('credentials.yaml', 'r'))

    from hangout_api import Hangouts


.. testcleanup:: base_api

    del hangout


First of all you need to login in:

    .. doctest:: base_api

        >>> hangout = Hangouts()
        >>> hangout.login(credentials['name'], credentials['password'], otp=credentials['otp'])

Now you can start new hangout:

    .. doctest:: base_api

        >>> hangout.start()

and invite people:

    .. doctest:: base_api

        >>> hangout.invite(['maxybot@gmail.com', 'test circle for call'])
