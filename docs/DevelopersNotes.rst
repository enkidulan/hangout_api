********************************
Developers Notes for Hangout API
********************************

Hangout API Architecture Overview
=================================

Hangout API has modular structure. Base Hangout class provides only
`few methods`_ to control a call. All other functionality are dynamically
added to base class by using `named utilities`_ from zope.component (part of ZCA
implementation).

Hangout API package has a bunch of build-in extensions:

    * Regular Hangout PlugIn's:

        * :doc:`api/Audio`
        * :doc:`api/Microphone`
        * :doc:`api/Video`
        * :doc:`api/Bandwidth`
        * :doc:`api/Toolbox`

    * OnAir PlugIn's:

        * :doc:`api/Broadcast`
        * :doc:`api/Cameraman`
        * :doc:`api/ControlRoom`

.. _few methods: api/Hangouts.html#hangout_api.base.Hangouts
.. _named utilities: http://docs.zope.org/zope.component/api/utility.html

Writing Hangouts Extensions
===========================

You can easily extend Hangout functionality by registering zope.component
utility (just make sure that this code executes on package initialization):

.. code:: python

    provideUtility(MyNewExtension, IModule, 'my_new_extension')

After you do it your new extension will be accessible from Hangout instance:

.. code:: python

    hangout = Hangouts()
    hangout.my_new_extension.do_some_thing()

List of available interfaces you can find at hangout_api.interfaces:

.. literalinclude:: ../hangout_api/interfaces.py
    :language: python


For more examples look at hangout_api.setting and hangout_api.gadgets.

As you can see from interfaces your class on initialization step should
take *base* argument, which is instance of `hangout_api.utils.Utils`_ class.

.. _hangout_api.utils.Utils: api/BaseUtils.html#hangout_api.utils.Utils

PlugIns development
=====================

The PlugIn's actually are a case Hangouts Extensions, but here you need to
handle the browser frames context. To make that easier there is
*gadget_context_handler*:

.. code:: python

    from hangout_api.gadgets.utils import gadget_context_handler

    class Cameraman(object):

        def __init__(self, base):
            self.base = base

        @gadget_context_handler("Cameraman")
        def mute_new_guests(self, value=None):
            self.base.browser.execute_script(
                'gapi.hangout.av.setLocalParticipantVideoMirrored(%s);' % value)

Now you can be sure that *mute_new_guests* function will be called only when
*self.base.browser* would be set to right iframe.

For more examples take a look at *hangout_api.gadgets*.


Testing
=======

What are tested:

    * pep8 && pylint
    * doctest to make sure that documentation code examples are correct
    * integration tests to make sure that library works with Hangouts well
      (that is nose based tests inside *hangout_api/tests directory*)

To run tests:

.. code:: bash

    $ bin/test

