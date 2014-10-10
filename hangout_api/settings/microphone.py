"""
Hangout API for Microphone
"""

from hangout_api.settings.utils import BaseSettings, MutingHandler


class MicrophoneSettings(BaseSettings):
    # pylint: disable=duplicate-code
    """
    Controlling call microphone settings.
    ======================================
    """

    def __init__(self, base):
        super(MicrophoneSettings, self).__init__(base)
        self.muting_handler = MutingHandler(
            base=base,
            base_text='ute microphone',
            mute_label='Mute microphone',
            unmute_label='Unmute microphone',
            no_device='Microphone not detected')

    @property
    def is_muted(self):
        """
        Returns True if microphone is muted, otherwise returns False

        .. code::

            >>> hangout.microphone.is_mutes()
            False
            >>> hangout.microphone.mute()
            >>> hangout.microphone.is_mutes()
            True
        """
        return self.muting_handler.is_muted()

    def unmute(self):
        """
        Un-mute microphone device. Returns:
            * True - microphone went from muted to un-muted
            * False - microphone was already un-muted

        .. code::

            >>> hangout.microphone.mute()

            >>> hangout.microphone.unmute()
            True
            >>> hangout.microphone.unmute()
            False

        """
        return self.muting_handler.unmute()

    def mute(self):
        """
        Mute microphone device. Returns:
            * True - microphone went from un-muted to muted
            * False - microphone was already muted

        .. code::

            >>> hangout.microphone.unmute()

            >>> hangout.microphone.mute()
            True
            >>> hangout.microphone.mute()
            False

        """
        return self.muting_handler.mute()

    def get_devices(self, with_nodes=False):
        """
        Returns list of available microphone devices:

        .. code::

            >>> hangout.microphone.get_devices()
            ['Default', 'Built-in Audio Analog Stereo']
        """
        device_xpath = '//*[text()="Microphone"]'
        devices_list_xpath = \
            '//div[@class="c-i c-i-Ed Hz"]/div/div[@class="c-k-t"]'
        return self._devices_getter(
            device_xpath, devices_list_xpath, with_nodes)

    def set_device(self, device_name):
        """
        Set device by its name:

        .. code::

            >>> hangout.microphone.get_devices()
            ['Default', 'Built-in Audio Analog Stereo']
            >>> hangout.microphone.set_device('Default')

        """
        return self._device_setter(device_name)

    @property
    def current_device(self):
        """
        Returns current device:

        .. code::

            >>> hangout.microphone.current_device()
            'Built-in Audio Analog Stereo'

        """
        return self._current_device_getter('Microphone', parrenty=1)
