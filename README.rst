Hangout Api
============

.. DANGER::
   This package is under heavy development


Python API for controlling Google+ Hangouts


********************
Install requirements
********************

**xvfb:**

.. code:: bash

    $ sudo apt-get install git python3-dev xvfb python-imaging scrot -y

**Google Talk Pluggin**

.. code:: bash

    $ wget https://dl.google.com/linux/direct/google-talkplugin_current_amd64.deb
    $ sudo dpkg -i google-talkplugin_current_amd64.deb

**Chrome:**

.. code:: bash

    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
    sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
    sudo apt-get update
    sudo apt-get install google-chrome-stable -y


*****************
API Specification
*****************

.. code:: python

    >>> hangout = Hangouts()

    >>> hangout.get_microphone_devices()
    >>> hangout.set_microphone_device(????) # Input audio device
    ["Default Device", "Internal Microphone"]

    >>> hangout.set_microphone_mode("studio")
    >>> hangout.set_microphone_mode("voice")

    >>> hangout.get_video_devices()
    ["Webcam A", "Webcam B"]
    >>> hangout.set_video_device(????) # Input video "webcam"

    >>> hangout.set_audio_device(????) # Audio output device
    ["Default Device", "Analog Stereo", "Digital Output"]


    >>> hangout.mute_audio()
    True # Audio went from un-muted to muted
    >>> hangout.unmute_audio()
    True # Audio went from muted to un-muted
    False # Audio was already un-muted

    # Same as the API above
    >>> hangout.mute_video()
    >>> hangout.unmute_video()

    >>> hangout.set_bandwidth(0) # 0 == audio only, 1, 2, 3

    # Two login methods,
    # * takes a username and password (plus optionally otp)
    # * takes no arguments, pops up a browser window which lets a user login using the normal Google flow, the system then saves the cookies needed.
    >>> hangout.login(username=xxx, password=xxx, otp=xxxx)
    >>> hangout.login()

    # Start a new hangout
    >>> hangout.start(onair=False)

    # Connect to an existing hangout
    >>> hangout.connect(hangoutid)

    # Invite people into the hangout
    >>> hangout.invite("persona@gmail.com")
    >>> hangout.invite(["personb@gmail.com", "Circle Name A")

    >>> hangout.participants()
    {participantid: {details}}

    >>> def f(level):
    ...   print level
    >>> hangout.audio_level_callback(f)

    # On Air extra API
    #######################################
    >>> hangout.broadcast.start()
    >>> hangout.broadcast.on()
    False
    >>> hangout.broadcast.stop()
    >>> hangout.broadcast.embed_url()

    # Hangout Toolbox API
    #######################################
    >>> hangout.toolbox.lower_third(
           line1="Tim Ansell", line2="",
           color="#55bbgg",
           logo="file.png",
           country="Australia")
    >>> hangout.toolbox.lower_third_active()
    False
    >>> hangout.toolbox.lower_third_active(True)
    >>> hangout.toolbox.lower_third_active()
    True

    >>> hangout.toolbox.display_clock_active()
    False
    >>> hangout.toolbox.display_clock_active(True)

    >>> hangout.toolbox.custom_overlay(file="overlay.png")

    >>> hangout.toolbox.video_mirror_active()
    False
    >>> hangout.video_mirror_active(True)

    # Cameraman API
    #######################################
    >>> hangout.cameraman.settings(
       video_only=True,
       hide_new_guests=True,
       mute_new_guests=True)

    # Same as the above personal mute/unmute API...
    >>> hangout.cameraman.mute_audio(participantid)
    >>> hangout.cameraman.unmute_audio(participantid)
    >>> hangout.cameraman.mute_video(participantid)
    >>> hangout.cameraman.unmute_video(participantid)
