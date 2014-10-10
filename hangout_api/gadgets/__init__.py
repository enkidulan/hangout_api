"""
This part contain helpers for woring wiht Hangout Plug-In's
and API to some of this Plug-In's
"""
from zope.component import provideUtility
from hangout_api.interfaces import IModule, IOnAirModule
from .cameraman import Cameraman
from .toolbox import ToolBox

provideUtility(Cameraman, IOnAirModule, 'cameraman')
provideUtility(ToolBox, IModule, 'toolbox')
