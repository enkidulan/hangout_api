"""
Base classes and utilities for working with hangouts settings
"""

from hangout_api.exceptions import NoSuchDeviceFound
from hangout_api.utils import silence_contextmanager, names_cleaner, TIMEOUTS


class BaseSettings(object):  # pylint: disable=R0903
    """
    Base class that handling device setting
    """
    device_class = NotImplementedError

    def __init__(self, base):
        self.base = base

    def get_devices(self, with_nodes=False):
        """
        Return devices list
        """
        raise NotImplementedError()

    def _devices_getter(
            self, device_xpath, devices_list_xpath, with_nodes):
        """
        Returns list of the devices based on device_xpath and
        devices_list_xpath arguments. Because HG is build all DOM dynamically
        there is need to make some actions before list of devices appear in
        DOM, this method handles it and also parses list values.
        """
        self.base.navigate_to_devices_settings()
        # click on MC list to make it load list of all devices
        device_box = self.base.browser.xpath(device_xpath).parent
        with silence_contextmanager(device_box):
            if device_box.by_class('c-h-i-b-o', timeout=TIMEOUTS.immediately):
                # if this class present that means that there is no devices
                # available to change
                device_name = device_box.get_attribute(
                    'innerText').split('\n')[0].strip()
                # in case if there is no devices at all return empty list
                if ' found' in device_name:
                    return []
                return [self.device_class(names_cleaner(device_name))]
        device_box.click(timeout=TIMEOUTS.fast)
        # get list of devices
        devices = {
            names_cleaner(n.get_attribute('innerText')): n
            for n in self.base.browser.xpath(devices_list_xpath, eager=True)}
        if with_nodes:
            return devices
        # pylint: disable=bad-builtin
        return list(map(self.device_class, devices.keys()))

    def _device_setter(self, device_name):
        """
        Devices setter that can handle special cases when only 1 device is
        available or no devices at all. In case if device can not be set raise
        NoSuchDeviceFound exception
        """
        if isinstance(device_name, self.device_class):
            device_name = device_name.name
        devices = self.get_devices(with_nodes=True)
        if len(devices) == 1:
            # there is no sense to set devise
            # if no devices or only one device are available
            return
        # pylint: disable=bad-builtin
        if device_name not in devices:
            raise NoSuchDeviceFound(
                "Can't find device with name '%s'" % device_name)
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
        device_name = names_cleaner(
            base_element.get_attribute('innerText').split('\n')[0])
        return self.device_class(device_name)


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
        with silence_contextmanager(self.base.browser):
            mute_button = self.base.browser.xpath(self.xpath)
        if mute_button is None:
            with silence_contextmanager(self.base.browser):
                no_device = self.base.browser.xpath(
                    self.no_device_xpath, timeout=TIMEOUTS.fast)
            if no_device:
                raise NoSuchDeviceFound('No device found')
            # raising original exception
            self.base.browser.xpath(self.xpath, timeout=TIMEOUTS.fast)
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
