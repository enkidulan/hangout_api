"""
Hangout API for Video
"""

from hangout_api.settings.utils import BaseSettings, MutingHandler


class VideoSettings(BaseSettings):
    """
    Controlling call video settings.
    =================================
    """

    def __init__(self, base):
        super(VideoSettings, self).__init__(base)
        self.muting_handler = MutingHandler(
            base=base,
            base_text='Turn camera',
            mute_label='Turn camera off',
            unmute_label='Turn camera on',
            no_device='Camera not detected')

    @property
    def is_muted(self):
        """
        Returns True if video is muted, otherwise returns True

        .. code::

            >>> hangout.video.is_mutes()
            False
            >>> hangout.video.mute()
            >>> hangout.video.is_mutes()
            True
        """
        return self.muting_handler.is_muted()

    def mute(self):
        """
        Mute video device. Returns:
            * True - Video went from un-muted to muted
            * False - Video was already muted

        .. code::

            >>> hangout.video.unmute()

            >>> hangout.video.mute()
            True
            >>> hangout.video.mute()
            False

        """
        return self.muting_handler.mute()

    def unmute(self):
        """
        Un-mute video device. Returns:
            * True - Video went from muted to un-muted
            * False - Video was already un-muted

        .. code::

            >>> hangout.video.mute()

            >>> hangout.video.unmute()
            True
            >>> hangout.video.unmute()
            False
        """
        return self.muting_handler.unmute()

    def get_devices(self, with_nodes=False):
        """
        Returns list of available video devices:

        .. code::

            >>> hangout.video.get_devices()
            ['USB2.0 PC CAMERA', 'HP Truevision HD']

        """
        device_xpath = '//*[text()="Video and Camera"]'
        devices_list_xpath = \
            '//div[@class="c-i c-i-Ed Kz"]/div/div[@class="c-k-t"]'
        return self._devices_getter(
            device_xpath, devices_list_xpath, with_nodes)

    def set_device(self, device_name):
        """
        Set device by its name:

        .. code::

            >>> hangout.video.get_devices()
            ['USB2.0 PC CAMERA', 'HP Truevision HD']
            >>> hangout.video.set_device('HP Truevision HD')

        """
        return self._device_setter(device_name)

    @property
    def current_device(self):
        """
        Returns current device:

        .. code::

            >>> hangout.video.current_device()
            'HP Truevision HD'

        """
        return self._current_device_getter('Video and Camera')
