.. Python Hangout Api documentation master file, created by
   sphinx-quickstart on Wed Jul 30 00:16:29 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Python Hangout Api's documentation
==============================================

Hangout API is python API for for controlling `Google Hangouts video calls`_ built
on top of selenium library. It provides ability to create new hangouts, connect
to existing calls, invite people to call and manage call settings.

Hangout structure:

  - `hangout`_ - Base Hangouts functionality. Allows you to log in, create new hangouts, etc..
  - `hangout.audio`_ - Allows control over the hangout's audio output settings.
  - `hangout.video`_ - Allows control over the hangout's video settings.
  - `hangout.microphone`_ - Allows control over the hangout's microphone settings.
  - `hangout.bandwidth`_ - Allows control over the hangout's bandwidth and quality.
  - `hangout.toolbox`_ - API to Hangouts `ToolBox PlugIn`_

Some extensions are only available in `Hangouts On Air`_. These are:

  - `hangout.broadcast`_ - Allows to manage `On Air broadcasting`_
  - `hangout.cameraman`_ - API to Hangouts `Cameraman PlugIn`_
  - `hangout.controlroom`_ - API to Hangouts `Control Room PlugIn`_

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


First you need to log in:

    .. doctest:: base_api

        >>> hangout = Hangouts()
        >>> hangout.login(email, password)

Then you can start a new hangout or connected to an existing one.

    .. doctest:: base_api

        >>> hangout.start()


Once in a hangout you can invite (via an email address or using a circle name)
other people to the hangout.

    .. doctest:: base_api

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

.. toctree::
   :glob:
   :hidden:

   api/*
   DevelopersNotes.rst

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

.. _ToolBox PlugIn: http://hangouttoolbox.com/
.. _Hangouts On Air: https://support.google.com/plus/answer/2553119?hl=en&ref_topic=2553242&rd=1
.. _On Air broadcasting: https://support.google.com/plus/answer/2660854?hl=en
.. _Cameraman PlugIn: https://support.google.com/plus/answer/2660854?hl=en
.. _Control Room PlugIn: https://support.google.com/plus/answer/2660854?hl=en
.. _Google Hangouts video calls: https://support.google.com/hangouts/answer/3110347?hl=en&ref_topic=2944918
