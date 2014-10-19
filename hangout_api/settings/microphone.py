"""
Hangout API for Microphone
"""

from hangout_api.settings.utils import BaseSettings, MutingHandler


class MicrophoneDevice(object):
    """
    Class that represents microphone devise. More like marker than actual class
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return "<MicrophoneDevice: %r>" % self.name


class MicrophoneSettings(BaseSettings):
    # pylint: disable=duplicate-code
    """
    Controlling call microphone settings.
    ======================================

    .. testsetup:: MicrophoneSettings

        from hangout_api.settings.microphone import (
            MicrophoneSettings, MicrophoneDevice)
        from hangout_api.tests.doctests_utils import DummyHangout

        hangout = DummyHangout(
            name='microphone',
            klass=MicrophoneSettings,
            getter=[
                MicrophoneDevice('Default'),
                MicrophoneDevice('usb001: microphone device')],
            setter=None,
            current=MicrophoneDevice('Default'))
        global was_called
        was_called = False
        def get_mute_button_label(*args):
            global was_called
            val = was_called and 'Unmute microphone' or 'Mute microphone'
            was_called = not was_called
            return val
        hangout.microphone.muting_handler.get_mute_button_label = \
            get_mute_button_label


    """
    device_class = MicrophoneDevice

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

        .. doctest:: MicrophoneSettings

            >>> hangout.microphone.is_muted in (True, False)
            True

        """
        return self.muting_handler.is_muted()

    def unmute(self):
        """
        Un-mute microphone device. Returns:
            * True - microphone went from muted to un-muted
            * False - microphone was already un-muted

        .. doctest:: MicrophoneSettings

            >>> hangout.microphone.mute()
            True
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

        .. doctest:: MicrophoneSettings

            >>> hangout.microphone.unmute()
            True
            >>> hangout.microphone.mute()
            True
            >>> hangout.microphone.mute()
            False

        """
        return self.muting_handler.mute()

    def get_devices(self, with_nodes=False):
        """
        Returns list of available microphone devices:

        .. doctest:: MicrophoneSettings

            >>> hangout.microphone.get_devices()
            [<MicrophoneDevice: 'Default'>, ...]
        """
        device_xpath = '//*[text()="Microphone"]'
        devices_list_xpath = \
            '//div[@class="c-i c-i-Ed Hz"]/div/div[@class="c-k-t"]'
        return self._devices_getter(
            device_xpath, devices_list_xpath, with_nodes)

    def set_device(self, device_name):
        """
        Set device by its name:

        .. doctest:: MicrophoneSettings

            >>> hangout.microphone.get_devices()
            [<MicrophoneDevice: 'Default'>, ...]
            >>> hangout.microphone.set_device('Default')

        """
        return self._device_setter(device_name)

    @property
    def current_device(self):
        """
        Returns current device:

        .. doctest:: MicrophoneSettings

            >>> hangout.microphone.current_device
            <MicrophoneDevice: 'Default'>

        """
        return self._current_device_getter('Microphone', parrenty=1)
