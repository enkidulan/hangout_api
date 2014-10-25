********************************
Developers Notes for Hangout API
********************************

Hangout API Architecture Overview
=================================

Hangout API has modular structure. Base Hangout class provides only
`few methods`_ to control call. All other functionality are dynamically
extends base class by using utility from zope.component (part of ZCA
implementation). It has a bunch of build-in extensions:
    * Regular Hangout PlugIn's:
        * :doc:`api/Audio`
        * :doc:`api/Microphone`
        * :doc:`api/Video`
        * :doc:`api/Bandwidth`
    * OnAir PlugIn's:
        * :doc:`api/Broadcast`
        * :doc:`api/Cameraman`
        * :doc:`api/Toolbox`
        * :doc:`api/ControlRoom`

.. _few methods: api/Hangouts.html#hangout_api.base.Hangouts


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

As you can see from interfaces your class in initialization step should
take *base* argument, which is instance of `hangout_api.utils.Utils`_ class.

.. _hangout_api.utils.Utils: api/BaseUtils.html#hangout_api.utils.Utils

PlugIn's development
=====================

The PlugIn's actually are a case Hangouts Extensions, but here you need to
handle the browser frames context. To make that easier there is
**hangout_api.gadgets.utils.gadget_context_handle**:

.. code:: python

    from hangout_api.gadgets.utils import gadget_context_handler

    class Cameraman(object):

        def __init__(self, base):
            self.base = base

        @gadget_context_handler("Cameraman")
        def mute_new_guests(self, value=None):
            pass

For more examples take a look at *hangout_api.gadgets*.


Testing
=======

.. _few methods: api/Hangouts
