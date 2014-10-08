"""
Module provides OnAir functionality for HangoutAPI
"""

from zope.component import provideUtility
from .interfaces import IOnAirModule
from .utils import tries_n_time_until_true
from hangout_api.gadgets.utils import gadget_context_handler


class Broadcast:
    """
    Broadcast plugin for OnAir
    """

    def __init__(self, base):
        self.base = base

    def start(self):
        """
        Start broadcasting
        """
        self.base.browser.by_text('Start broadcast').click(0.5)
        self.base.browser.by_text('OK').click(0.5)
        tries_n_time_until_true(self.is_on, try_num=60)

    def is_on(self):
        """
        Returns True if broadcasting otherwise returns False
        """
        return self.base.browser.by_text('LIVE', timeout=2).is_displayed()

    def embed_url(self):
        """
        Returns url for embedding video
        """
        self.base.browser.by_text('Links').click(0.5)
        return self.base.browser.xpath(
            '//div[@class="c-N-K"]/input').get_attribute('value')

    def stop(self):
        """
        Stop broadcasting
        """
        self.base.browser.by_text('Stop broadcast').click(0.5)
        tries_n_time_until_true(lambda: not self.is_on(), try_num=60)
        self.base.click_cancel_button_if_there_is_one(timeout=10)

provideUtility(Broadcast, IOnAirModule, 'broadcast')


class Cameraman:
    """
    Cameraman plugin for OnAir
    """

    def __init__(self, base):
        self.base = base

    def _status_getter_setter(self, class_name, value):
        """
        Helper function that handles to on or off Cameraman properties
        """
        status_xpath = '//*[contains(@class, "%s")]/div[@aria-checked="true"]'
        status = self.base.browser.xpath(
            status_xpath % class_name).get_attribute(
                'innerText').strip() == 'Yes'
        if value is None:
            return status
        if status != value:
            value_xpath = '//*[contains(@class, "%s")]//div[text()="%s"]' % (
                class_name, 'Yes' if value else 'No')
            self.base.browser.xpath(value_xpath).click(0.5)
            return True
        return False

    @gadget_context_handler("Cameraman")
    def mute_new_guests(self, value=None):
        """
        New guests in my large (3+) broadcast are muted when they join?
        """
        return self._status_getter_setter('u-Xc-Ox-ra', value)

    @gadget_context_handler("Cameraman")
    def video_only(self, value=None):
        """
        Broadcast the large video that I see to my audience and
        hide the other video feeds?
        """
        return self._status_getter_setter('u-Xc-Wt-ra', value)

    @gadget_context_handler("Cameraman")
    def hide_new_guests(self, value=None):
        """
        As guests join, hide their audio and video from my broadcast?
        """
        return self._status_getter_setter('u-Xc-ra', value)

provideUtility(Cameraman, IOnAirModule, 'cameraman')
