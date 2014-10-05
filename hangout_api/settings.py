"""
Hangout Call Setting Handlers
=============================
"""
from zope.component import provideUtility
from .interfaces import IModule
from enum import Enum
from .exceptions import NoSuchDeviceFound

BANDWIDTH_LEVELS = Enum(
    'Bandwidth', {
        'Audio only': 0,
        'Very Low': 1,
        'Low': 2,
        'Medium': 3,
        'Auto HD': 4})


def names_cleaner(name):
    """
    Helper function to clean up string from 'thml' symbols
    """
    # pylint: disable=W1402
    return name.strip().replace('\u202a', '').replace('\u202c', '')


class BaseSettings(object):  # pylint: disable=R0903
    """
    Base class that handling device setting
    """

    def __init__(self, base):
        self.base = base

    def get_devices(self, with_nodes=False):
        """
        Return devices list
        """
        raise NotImplementedError()

    def _devices_getter(self, device_xpath, devices_list_xpath, with_nodes):
        """
        Returns list of the devices based on device_xpath and
        devices_list_xpath arguments. Because HG is build all DOM dynamically
        there is need to make some actions before list of devices appear in
        DOM, this method handles it and also parses list values.
        """
        self.base.navigate_to_devices_settings()
        # click on MC list to make it load list of all devices
        device_box = self.base.browser.xpath(device_xpath).parent
        device_box.silent = True
        if device_box.by_class('c-h-i-b-o', timeout=0.2):
            # if this class present that means that there is no devices
            # available to change
            device_name = device_box.get_attribute(
                'innerText').split('\n')[0].strip()
            # in case if there is no devices at all return empty list
            if ' found' in device_name:
                return []
            return [names_cleaner(device_name)]
        device_box.silent = False
        device_box.click(timeout=0.5)
        # get list of devices
        devices = {
            names_cleaner(n.get_attribute('innerText')): n
            for n in self.base.browser.xpath(devices_list_xpath, eager=True)}
        if with_nodes:
            return devices
        return list(devices.keys())

    def _device_setter(self, device_name):
        """
        Devices setter that can handle special cases when only 1 device is
        available or no devices at all. In case if device can not be set raise
        NoSuchDeviceFound exception
        """
        devices = self.get_devices(with_nodes=True)
        if device_name not in devices:
            raise NoSuchDeviceFound(
                "Can't find device with name '%s'" % device_name)
        if len(devices) == 1:
            # there is no sense to set devise
            # if no devices or only one device are available
            return
        self.get_devices(with_nodes=True)[device_name].click()
        self.base.click_on_devices_save_button()

    def _current_device_getter(self, text_selector, parrenty=2):
        """
        Returns currently used device
        """
        self.base.navigate_to_devices_settings()
        base_element = self.base.browser.by_text(text_selector)
        for _ in range(parrenty):
            base_element = base_element.parent
        return names_cleaner(
            base_element.get_attribute('innerText').split('\n')[0])


class MutingHandler(object):
    """
    Handler to interact with mute buttons, like "Mute Video".
    """
    # pylint: disable=R0913
    def __init__(self, base, base_text, mute_label, unmute_label, no_device):
        self.base = base
        self.base_text = base_text
        self.mute_label = mute_label
        self.unmute_label = unmute_label
        self.xpath = '//div[contains(@aria-label, "%s")]' % self.base_text
        self.no_device_xpath = '//div[contains(@aria-label, "%s")]' % no_device

    def get_mute_button_label(self):
        """
        Returns current text of 'mute' button. In case if muting is not
        available (no device found) raises NoSuchDeviceFound
        """
        self.base.click_cancel_button_if_there_is_one()
        self.base.browser.silent = True
        try:
            mute_button = self.base.browser.xpath(self.xpath)
        finally:
            self.base.browser.silent = False
        if mute_button is None:
            self.base.browser.silent = True
            try:
                no_device = self.base.browser.xpath(
                    self.no_device_xpath, timeout=0.5)
            finally:
                self.base.browser.silent = False
            if no_device:
                raise NoSuchDeviceFound('No device found')
            # raising original exception
            self.base.browser.xpath(self.xpath, timeout=0.5)
        return mute_button.get_attribute('aria-label')

    def is_muted(self):
        """
        Returns True if muted otherwise False
        """
        return self.get_mute_button_label() == self.unmute_label

    def mute(self):
        """
        Mutes device
        """
        if self.get_mute_button_label() == self.unmute_label:
            return False
        self.base.click_menu_element(self.xpath)
        return True

    def unmute(self):
        """
        Un-mutes device
        """
        if self.get_mute_button_label() == self.mute_label:
            return False
        self.base.click_menu_element(self.xpath)
        return True


class BandwidthSettings(BaseSettings):
    """

    Controlling bandwidth settings.

    Available bandwidth levels are:
        * 0 - Audio only
        * 1 - Very Low
        * 2 - Low
        * 3 - Medium
        * 4 - Auto HD
    """
    # pylint: disable=W0223
    def _get_bandwidth_controller(self):
        """
        Returns selenium wrapper object for "Bandwidth" bar
        """
        limit_bandwidth_xpath = '//div[text()="Limit Bandwidth"]'
        if not self.base.browser.xpath(limit_bandwidth_xpath).is_displayed():
            # no need to open bandwidth settings tab if it's opened already
            self.base.click_menu_element(
                '//div[@aria-label="Adjust bandwidth usage"]')
        return self.base.browser.xpath(
            '//div[@aria-label="Adjust the quality of your video"]')

    def set(self, bandwidth):
        """
        Set bandwidth setting for hangout

        .. code::

            >>> hangout.bandwidth.set(2)

        """
        controller = self._get_bandwidth_controller()
        levels = controller.by_class('Sa-IU-HT', eager=True)
        # setting levels
        levels[bandwidth].click(timeout=0.5)

    def get(self):
        """
        Get bandwidth setting for hangout.

        .. code::

            >>> hangout.bandwidth.get()
            <Bandwidth.Very Low: 1>

        """
        controller = self._get_bandwidth_controller()
        # pylint: disable=E1102
        return BANDWIDTH_LEVELS(int(controller.get_attribute('aria-valuenow')))

provideUtility(BandwidthSettings, IModule, 'bandwidth')


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

provideUtility(VideoSettings, IModule, 'video')


class MicrophoneSettings(BaseSettings):
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

provideUtility(MicrophoneSettings, IModule, 'microphone')


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

provideUtility(AudioSettings, IModule, 'audio')
