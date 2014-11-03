"""
API for Cameraman Hangout PlugIn
"""
from hangout_api.gadgets.utils import gadget_context_handler
from hangout_api.utils import TIMEOUTS


class Cameraman(object):
    """
    Cameraman plugin for OnAir

    .. testsetup:: Cameraman

        from hangout_api.gadgets.cameraman import (Cameraman)
        from hangout_api.tests.doctests_utils import (
            DummyHangout, DummySelenium)

        from hangout_api.gadgets import utils
        utils.open_app = lambda *args: None


        global call_num
        call_num = 0

        def get_attribute(*args):
            global call_num
            if call_num == 6:
                call_num = 0
            call_num += 1
            val = [False, True, True, True, False, False][call_num - 1]
            return val and 'Yes' or 'No'
        DummySelenium.get_attribute = get_attribute

        hangout = DummyHangout(
            name='cameraman',
            klass=Cameraman)

    """

    def __init__(self, base):
        self.base = base

    def _status_getter_setter(self, class_name, value):
        """
        Helper function that handles turning on and off Cameraman properties
        """
        status_xpath = \
            '//*[contains(@class, "%s")]/div[@aria-checked="true"]' \
            % class_name
        value_xpath = '//*[contains(@class, "%s")]//div[text()="%s"]' % (
            class_name, 'Yes' if value else 'No')
        status = self.base.browser.xpath(status_xpath).get_attribute(
            'innerText').strip() == 'Yes'
        if value is None:
            return status
        if status != value:
            self.base.browser.xpath(value_xpath).click(TIMEOUTS.fast)
            # waiting for a change
            self.base.browser.xpath(
                status_xpath + '//div[text()="%s"]' % (
                    'Yes' if value else 'No'))
            return True
        return False

    @gadget_context_handler("Cameraman")
    def mute_new_guests(self, value=None):
        """
        New guests in my large (3+) broadcast are muted when they join?

        As argument takes True or False and returns:
            * True - went to opposite state
                (from 'on' to 'off', or from 'off' to 'on')
            * False -desired state was already chosen

        In case if no argument was provided returns current state

        .. doctest:: Cameraman

            >>> hangout.cameraman.mute_new_guests(True)
            True
            >>> hangout.cameraman.mute_new_guests()
            True
            >>> hangout.cameraman.mute_new_guests(True)
            False
            >>> hangout.cameraman.mute_new_guests(False)
            True
            >>> hangout.cameraman.mute_new_guests()
            False
            >>> hangout.cameraman.mute_new_guests(False)
            False

        """
        return self._status_getter_setter('u-Xc-Ox-ra', value)

    @gadget_context_handler("Cameraman")
    def video_only(self, value=None):
        """
        Broadcast the large video that I see to my audience and
        hide the other video feeds?

        As argument takes True or False and returns:
            * True - went to opposite state
                (from 'on' to 'off', or from 'off' to 'on')
            * False -desired state was already chosen

        In case if no argument was provided returns current state

        .. doctest:: Cameraman

            >>> hangout.cameraman.video_only(True)
            True
            >>> hangout.cameraman.video_only()
            True
            >>> hangout.cameraman.video_only(True)
            False
            >>> hangout.cameraman.video_only(False)
            True
            >>> hangout.cameraman.video_only()
            False
            >>> hangout.cameraman.video_only(False)
            False
        """
        return self._status_getter_setter('u-Xc-Wt-ra', value)

    @gadget_context_handler("Cameraman")
    def hide_new_guests(self, value=None):
        """
        As guests join, hide their audio and video from my broadcast?

        As argument takes True or False and returns:
            * True - went to opposite state
                (from 'on' to 'off', or from 'off' to 'on')
            * False -desired state was already chosen

        In case if no argument was provided returns current state.

        .. doctest:: Cameraman

            >>> hangout.cameraman.hide_new_guests(True)
            True
            >>> hangout.cameraman.hide_new_guests()
            True
            >>> hangout.cameraman.hide_new_guests(True)
            False
            >>> hangout.cameraman.hide_new_guests(False)
            True
            >>> hangout.cameraman.hide_new_guests()
            False
            >>> hangout.cameraman.hide_new_guests(False)
            False
        """
        return self._status_getter_setter('u-Xc-ra', value)
