"""
Hangout API for bandwidth
"""

from enum import Enum
from hangout_api.settings.utils import BaseSettings

BANDWIDTH_LEVELS = Enum(
    'Bandwidth', {
        'Audio only': 0,
        'Very Low': 1,
        'Low': 2,
        'Medium': 3,
        'Auto HD': 4})


class BandwidthSettings(BaseSettings):
    # pylint: disable=duplicate-code
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
