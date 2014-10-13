"""
Hangout API for OnAir Broadcast
"""
# pylint: disable=R0801

from hangout_api.utils import tries_n_time_until_true


class Broadcast(object):
    """
    Broadcast plugin for OnAir

    .. testsetup:: Broadcast

        from hangout_api.settings.broadcast import Broadcast
        from hangout_api.tests.doctests_utils import  (
            DummyHangout, DummySelenium)

        DummySelenium.get_attribute = lambda *args: '<iframe width="560" height="315" src="//www.youtube.com/embed/bVEV9ODxbYs" frameborder="0" allowfullscreen></iframe>'

        hangout = DummyHangout(
            name='broadcast',
            klass=Broadcast)

    """

    def __init__(self, base):
        self.base = base

    def start(self):
        """
        Start broadcasting

        .. doctest:: Broadcast

            >>> hangout.broadcast.start()

        """
        self.base.browser.by_text('Start broadcast').click(0.5)
        self.base.browser.by_text('OK').click(0.5)
        tries_n_time_until_true(self.is_on, try_num=60)

    def is_on(self):
        """
        Returns True if broadcasting otherwise returns False

        .. doctest:: Broadcast

            >>> hangout.broadcast.is_on() in (True, False)
            True

        """
        return self.base.browser.by_text('LIVE', timeout=2).is_displayed()

    def embed_url(self):
        """
        Returns url for embedding video

        .. doctest:: Broadcast

            >>> hangout.broadcast.embed_url()
            '<iframe width="560" height="315" src="//www.youtube.com/embed/bVEV9ODxbYs" frameborder="0" allowfullscreen></iframe>'

        """
        self.base.browser.by_text('Links').click(0.5)
        return self.base.browser.xpath(
            '//div[@class="c-N-K"]/input').get_attribute('value')

    def stop(self):
        """
        Stop broadcasting

        .. doctest:: Broadcast

            >>> hangout.broadcast.stop()

        """
        self.base.browser.by_text('Stop broadcast').click(0.5)
        tries_n_time_until_true(lambda: not self.is_on(), try_num=60)
        self.base.click_cancel_button_if_there_is_one(timeout=10)
