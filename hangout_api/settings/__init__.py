"""
Hangout Call Setting Handlers
=============================
"""
from zope.component import provideUtility
from hangout_api.interfaces import IModule
from .bandwidth import BandwidthSettings
from .video import VideoSettings
from .microphone import MicrophoneSettings
from .audio import AudioSettings

provideUtility(BandwidthSettings, IModule, 'bandwidth')
provideUtility(VideoSettings, IModule, 'video')
provideUtility(MicrophoneSettings, IModule, 'microphone')
provideUtility(AudioSettings, IModule, 'audio')
