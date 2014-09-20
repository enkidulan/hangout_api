"""
Setting tab controllers.
========================
"""


class BaseSettings():

    def __init__(self, base):
        self.base = base

    def _devices_getter(self, device_xpath, devices_list_xpath, with_nodes):
        self.base.navigate_to_devices_settings()
        # click on MC list to make it load list of all devices
        device_box = self.base.browser.xpath(device_xpath).parent
        device_box.silent = True
        if device_box.by_class('c-h-i-b-o', timeout=0.2):
            # if this class present that means that there is no devices
            # available to change, so lets return current text
            return device_box.get_attribute('innerText').strip()
        device_box.silent = False
        device_box.click(timeout=0.5)
        # get list of devices
        devices = {
            n.get_attribute('innerText'): n
            for n in self.base.browser.xpath(devices_list_xpath, eager=True)}
        if with_nodes:
            return devices
        return list(devices.keys())


class BandwidthSettings(BaseSettings):
    """
    Bandwidth settings
    """

    def _get_bandwidth_controooller(self):
        limit_bandwidth_xpath = '//div[text()="Limit Bandwidth"]'
        if not self.base.browser.xpath(limit_bandwidth_xpath).is_displayed():
            # no need to open bandwidth settings tab if it's opened already
            self.base.click_menu_element(
                '//div[@aria-label="Adjust bandwidth usage"]')
        return self.base.browser.xpath(
            '//div[@aria-label="Adjust the quality of your video"]')

    def set(self, bandwidth):
        """
        Set bandwidth setting for hangout:
            * 0 - Audio only
            * 1 - Very Low
            * 2 - Low
            * 3 - Medium
            * 4 - Auto HD
        """
        controller = self._get_bandwidth_controooller()
        levels = controller.by_class('Sa-IU-HT', eager=True)
        # setting levels
        levels[bandwidth].click(timeout=0.5)

    def get(self):
        """
        Get bandwidth setting for hangout
        """
        controller = self._get_bandwidth_controooller()
        return int(controller.get_attribute('aria-valuenow'))


class VideoSettings(BaseSettings):
    """
    Video settings
    """

    def mute(self):
        """
        Mute video device. Returns:
            * True - Video went from un-muted to muted
            * False - Video was already muted
        """
        self.base.click_cancel_button_if_there_is_one()
        xpath = '//div[contains(@aria-label, "Turn camera")]'
        mute_button = self.base.browser.xpath(xpath)
        if mute_button.get_attribute('aria-label') == 'Turn camera on':
            return False
        self.base.click_menu_element(xpath)
        return True

    def unmute(self):
        """
        Un-mute video device. Returns:
            * True - Video went from muted to un-muted
            * False - Video was already un-muted
        """
        self.base.click_cancel_button_if_there_is_one()
        xpath = '//div[contains(@aria-label, "Turn camera")]'
        mute_button = self.base.browser.xpath(xpath)
        if mute_button.get_attribute('aria-label') == 'Turn camera off':
            return False
        self.base.click_menu_element(xpath)
        return True

    def get_devices(self, with_nodes=False):
        device_xpath = '//*[text()="Video and Camera"]'
        devices_list_xpath = \
            '//div[@class="c-i c-i-Ed Kz"]/div/div[@class="c-k-t"]'
        return self._devices_getter(
            device_xpath, devices_list_xpath, with_nodes)

    def set_device(self, device_name):
        self.get_devices(with_nodes=True)[device_name].click()
        self.base.click_on_devices_save_button()


class MicrophoneSettings(BaseSettings):
    """
    Microphone settings
    """

    def get_devices(self, with_nodes=False):
        device_xpath = '//*[text()="Microphone"]'
        devices_list_xpath = \
            '//div[@class="c-i c-i-Ed Hz"]/div/div[@class="c-k-t"]'
        return self._devices_getter(
            device_xpath, devices_list_xpath, with_nodes)

    def set_device(self, name):
        # TODO: make sure that browser is on needed context
        self.get_devices(with_nodes=True)[name].click()
        # click save button
        self.base.click_on_devices_save_button()


class AudioSettings(BaseSettings):
    """
    Audio settings
    """

    def unmute(self):
        """
        Un-mute audio device. Returns:
            * True - Audio went from muted to un-muted
            * False - Audio was already un-muted
        """
        self.base.click_cancel_button_if_there_is_one()
        xpath = '//div[contains(@aria-label, "ute microphone")]'
        mute_button = self.base.browser.xpath(xpath)
        if mute_button.get_attribute('aria-label') == 'Mute microphone':
            return False
        self.base.click_menu_element(xpath)
        return True

    def mute(self):
        """
        Mute audio device. Returns:
            * True - Audio went from un-muted to muted
            * False - Audio was already muted
        """
        self.base.click_cancel_button_if_there_is_one()
        xpath = '//div[contains(@aria-label, "ute microphone")]'
        mute_button = self.base.browser.xpath(xpath)
        if mute_button.get_attribute('aria-label') == 'Unmute microphone':
            return False
        self.base.click_menu_element(xpath)
        return True

    def get_devices(self, with_nodes=False):
        device_xpath = '//*[contains(@class, "iph_s_ao")]'
        devices_list_xpath = \
            '//div[@class="c-i c-i-Ed Iz"]/div/div[@class="c-k-t"]'
        return self._devices_getter(
            device_xpath, devices_list_xpath, with_nodes)

    def set_device(self, device_name):
        # TODO: make sure that browser is on needed context
        self.get_devices(with_nodes=True)[device_name].click()
        # click save button
        self.base.click_on_devices_save_button()
