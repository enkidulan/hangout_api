"""
Hangout API for audio
"""

from hangout_api.settings.utils import BaseSettings
from retrying import retry


class AudioDevice(object):
    """
    Class that represents audio devise. More like marker than actual class.

    .. testsetup:: AudioDevice

        from hangout_api.settings.audio import AudioDevice

    .. doctest:: AudioDevice

        >>> device_1 = AudioDevice('audio 1')
        >>> device_1.name
        'audio 1'
        >>> device_1
        <AudioDevice: 'audio 1'>
        >>> device_1 == AudioDevice('audio 2')
        False
        >>> device_1 == AudioDevice('audio 1')
        True

    """
    # pylint: disable=too-few-public-methods
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return "<AudioDevice: %r>" % self.name


class AudioSettings(BaseSettings):
    # pylint: disable=duplicate-code
    """
    Controlling call audio settings.
    ==================================

    .. testsetup:: AudioSettings

        from hangout_api.settings.audio import AudioSettings, AudioDevice
        from hangout_api.tests.doctests_utils import DummyHangout

        hangout = DummyHangout(
            name='audio',
            klass=AudioSettings,
            getter=[
                AudioDevice('Default'),
                AudioDevice('Built-in Audio Analog Stereo')],
            setter=None,
            current=AudioDevice('Default'))

    """
    device_class = AudioDevice

    @retry(stop_max_attempt_number=3)
    def get_devices(self, with_nodes=False):
        """
        Returns list of available audio devices:

        .. doctest:: AudioSettings

            >>> hangout.audio.get_devices()
            [<AudioDevice: 'Default'>, ...]

        """
        device_xpath = '//*[contains(@class, "iph_s_ao")]'
        devices_list_xpath = \
            '//div[@class="c-i c-i-Ed Iz"]/div/div[@class="c-k-t"]'
        return self._devices_getter(
            device_xpath, devices_list_xpath, with_nodes)

    @retry(stop_max_attempt_number=3)
    def set_device(self, device_name):
        """
        Set device by its name:

        .. doctest:: AudioSettings

            >>> hangout.audio.get_devices()
            [<AudioDevice: 'Default'>, ...]
            >>> hangout.audio.set_device('Default')

        """
        return self._device_setter(device_name)

    @property
    @retry(stop_max_attempt_number=3)
    def current_device(self):
        """
        Returns current device:

        .. doctest:: AudioSettings

            >>> hangout.audio.current_device
            <AudioDevice: 'Default'>

        """
        return self._current_device_getter('Play test sound')
