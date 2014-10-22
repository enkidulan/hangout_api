.. Python Hangout Api documentation master file, created by
   sphinx-quickstart on Wed Jul 30 00:16:29 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Python Hangout Api's documentation
==============================================

Hangout API is python API for google hangouts build on top of selenium library.
It provides ability to create new hangouts, connect to existing calls,
invite people to call and manage call settings.

Settings API:
  * :doc:`api/Hangouts`
  * :doc:`api/Audio`
  * :doc:`api/Microphone`
  * :doc:`api/Video`
  * :doc:`api/Bandwidth`

On Air API:
  * :doc:`api/Broadcast`

PlugIns API:
  * :doc:`api/Cameraman`
  * :doc:`api/Toolbox`
  * :doc:`api/ControlRoom`

Contents:

.. toctree::
   :maxdepth: 2

   api_documentation


How to use Hangout API
============================================

.. testsetup:: base_api

    from hangout_api.tests.utils import credentials
    from hangout_api.tests.utils import hangout_factory as Hangouts
    email = credentials['name']
    password = credentials['password']

.. testcleanup:: base_api

    del hangout


First of all you need to log in to start new or connect to existing hangout:

    .. doctest:: base_api

        >>> hangout = Hangouts()
        >>> hangout.login(email, password)

Now you can start new or connect and invite people:

    .. doctest:: base_api

        >>> hangout.start()
        >>> hangout.invite(['maxybot@gmail.com', 'test circle for call'])

Or change call setting, like bandwidth, audio, etc:

    .. .. doctest:: base_api

    ..     >>> hangout.bandwidth.get()
    ..     5
    ..     >>> hangout.bandwidth.set(3)
    ..     >>> hangout.microphone.mute()
..     ..     >>> hangout.video.set('USB2.0 PC CAMERA')

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
