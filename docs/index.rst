.. Python Hangout Api documentation master file, created by
   sphinx-quickstart on Wed Jul 30 00:16:29 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Python Hangout Api's documentation
==============================================

Hangout API is python API for google hangouts build on top of selenium library.
It provides ability to create new hangouts, connect to existing calls,
invite people to call and manage call settings.

Hangout structure:

  - `hangout`_ it is a base allows you to log in, create new hangouts, etc..
  - `hangout.audio`_ - that allows you to set or get audio device, etc...
  - `hangout.video`_ - that allows you to mute/un-mute video, set video device, etc...
  - `hangout.microphone`_ - that allows you to mute/un-mute microphone, set microphone device, etc...
  - `hangout.bandwidth`_ - that allows you to get or set bandwidth.
  - `hangout.toolbox`_ - API to Hangouts ToolBox PlugIn

There is also some extension that are availably for OnAir Hangouts only:

  - `hangout.broadcast`_ - allows you manage your broadcasting: start, stop, get its youtube url, etc...
  - `hangout.cameraman`_ - API to Hangouts Cameraman PlugIn
  - `hangout.controlroom`_ - API to Hangouts Control Room PlugIn

Also you can read `developers notes`_


How to use Hangout API
============================================

.. testsetup:: base_api

    from hangout_api.tests.utils import credentials
    from hangout_api.tests.utils import hangout_factory as Hangouts
    email = credentials['name']
    password = credentials['password']

.. testcleanup:: base_api

    del hangout


First of all you need to log in:

    .. doctest:: base_api

        >>> hangout = Hangouts()
        >>> hangout.login(email, password)

Now you can start new or connect to existing hangouts and invite people:

    .. doctest:: base_api

        >>> hangout.start()
        >>> hangout.invite(['maxybot@gmail.com', 'Friends'])

Or get (or change) call setting, like bandwidth, audio, etc:

    .. doctest:: base_api

        >>> hangout.microphone.get_devices()
        [...]
        >>> hangout.video.get_devices()
        [...]

And leave the call when you done:

    .. doctest:: base_api

        >>> hangout.disconnect()


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _hangout:  api/Hangouts.html#hangout_api.base.Hangouts
.. _hangout.audio: api/Audio.html#hangout_api.settings.audio.AudioSettings
.. _hangout.video: api/Video.html#hangout_api.settings.video.VideoSettings
.. _hangout.microphone: api/Microphone.html#hangout_api.settings.microphone.MicrophoneSettings
.. _hangout.bandwidth: api/Bandwidth.html#hangout_api.settings.bandwidth.BandwidthSettings
.. _hangout.toolbox: api/Toolbox.html#hangout_api.gadgets.toolbox.ToolBox
.. _hangout.broadcast: api/Broadcast.html#hangout_api.settings.broadcast.Broadcast
.. _hangout.cameraman: api/Cameraman.html#hangout_api.gadgets.cameraman.Cameraman
.. _hangout.controlroom: api/ControlRoom.html#hangout_api.gadgets.control_room.ControlRoom
.. _developers notes: DevelopersNotes.html
