from hangout_api.settings.utils import BaseSettings


class AudioSettings(BaseSettings):
    """
    Controlling call audio settings.
    ==================================
    """

    def get_devices(self, with_nodes=False):
        """
        Returns list of available audio devices:

        .. code::

            >>> hangout.audio.get_devices()
            ['Default', 'Built-in Audio Analog Stereo']

        """
        device_xpath = '//*[contains(@class, "iph_s_ao")]'
        devices_list_xpath = \
            '//div[@class="c-i c-i-Ed Iz"]/div/div[@class="c-k-t"]'
        return self._devices_getter(
            device_xpath, devices_list_xpath, with_nodes)

    def set_device(self, device_name):
        """
        Set device by its name:

        .. code::

            >>> hangout.audio.get_devices()
            ['Default', 'Built-in Audio Analog Stereo']
            >>> hangout.audio.set_device('Default')

        """
        return self._device_setter(device_name)

    @property
    def current_device(self):
        """
        Returns current device:

        .. code::

            >>> hangout.audio.current_device()
            'Default'

        """
        return self._current_device_getter('Play test sound')
