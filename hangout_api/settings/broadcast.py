"""
Hangout API for OnAir Broadcast
"""
# pylint: disable=R0801

from hangout_api.utils import tries_n_time_until_true


class Broadcast(object):
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
