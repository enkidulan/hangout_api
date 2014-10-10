from hangout_api.gadgets.utils import gadget_context_handler


class Cameraman(object):
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
