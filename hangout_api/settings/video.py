"""
Hangout API for Video
"""

from hangout_api.settings.utils import BaseSettings, MutingHandler


class VideoDevice(object):
    """
    Class that represents video devise. More like marker than actual class.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return "<VideoDevice: %r>" % self.name


class VideoSettings(BaseSettings):
    """
    Controlling call video settings.
    =================================

    .. testsetup:: VideoSettings

        from hangout_api.settings.video import VideoSettings, VideoDevice
        from hangout_api.tests.doctests_utils import DummyHangout

        hangout = DummyHangout(
            name='video',
            klass=VideoSettings,
            getter=[VideoDevice('USB2.0 PC CAMERA'),
                    VideoDevice('HP Truevision HD')],
            setter=None,
            current=VideoDevice('USB2.0 PC CAMERA'))
        global was_called
        was_called = False
        def get_mute_button_label(*args):
            global was_called
            val = was_called and 'Turn camera on' or 'Turn camera off'
            was_called = not was_called
            return val
        hangout.video.muting_handler.get_mute_button_label = \
            get_mute_button_label

    """
    device_class = VideoDevice

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

        .. doctest:: VideoSettings

            >>> hangout.video.is_muted in (True, False)
            True
        """
        return self.muting_handler.is_muted()

    def mute(self):
        """
        Mute video device. Returns:
            * True - Video went from un-muted to muted
            * False - Video was already muted

        .. doctest:: VideoSettings

            >>> hangout.video.unmute()
            True
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

        .. doctest:: VideoSettings

            >>> hangout.video.mute()
            True
            >>> hangout.video.unmute()
            True
            >>> hangout.video.unmute()
            False

        """
        return self.muting_handler.unmute()

    def get_devices(self, with_nodes=False):
        """
        Returns list of available video devices:

        .. doctest:: VideoSettings

            >>> hangout.video.get_devices()
            [<VideoDevice: 'USB2.0 PC CAMERA'>, ...]

        """
        device_xpath = '//*[text()="Video and Camera"]'
        devices_list_xpath = \
            '//div[@class="c-i c-i-Ed Kz"]/div/div[@class="c-k-t"]'
        return self._devices_getter(
            device_xpath, devices_list_xpath, with_nodes)

    def set_device(self, device_name):
        """
        Set device by its name:

        .. doctest:: VideoSettings

            >>> hangout.video.get_devices()
            [<VideoDevice: 'USB2.0 PC CAMERA'>, ...]
            >>> hangout.video.set_device('HP Truevision HD')

        """
        return self._device_setter(device_name)

    @property
    def current_device(self):
        """
        Returns current device:

        .. doctest:: VideoSettings

            >>> hangout.video.current_device
            <VideoDevice: 'USB2.0 PC CAMERA'>

        """
        return self._current_device_getter('Video and Camera')
