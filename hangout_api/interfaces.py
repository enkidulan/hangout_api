"""
Interfaces for Hangout API
"""
# pylint not working well with zope and don't get the Interface conception
# pylint: disable=E0611,F0401,R0903,W0232

from zope.interface import Interface


class IModule(Interface):
    """
    Interface to register utils for hangout instance. Resisted class instance
    will be reachable as Hangouts class property under the name you registered
    it.
    """
    # def __init__(self, base):
    #     pass

    pass


class IOnAirModule(Interface):
    """
    Interface to register utils for hangout instance. Resisted class instance
    will be reachable as Hangouts class property under the name you registered
    it.
    """
    # def __init__(self, base):
    #     pass

    pass
