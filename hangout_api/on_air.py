"""
Module provides OnAir functionality for HangoutAPI
"""

from zope.component import provideUtility
from .interfaces import IOnAirModule
from .utils import tries_n_time_until_true


class Broadcast:

    def __init__(self, base):
        self.base = base

    def start(self):
        self.base.browser.by_text('Start broadcast').click(0.5)
        self.base.browser.by_text('OK').click(0.5)
        tries_n_time_until_true(self.on, try_num=60)

    def on(self):
        return self.base.browser.by_text('LIVE', timeout=2).is_displayed()

    def embed_url(self):
        self.base.browser.by_text('Links').click(0.5)
        return self.base.browser.xpath(
            '//div[@class="c-N-K"]/input').get_attribute('value')

    def stop(self):
        self.base.browser.by_text('Stop broadcast').click(0.5)
        tries_n_time_until_true(lambda: not self.on(), try_num=60)

provideUtility(Broadcast, IOnAirModule, 'broadcast')
