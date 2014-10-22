"""
Helpers for handling Hangout PlugIns (gadgets)
"""
from functools import wraps
from hangout_api.utils import tries_n_time_until_true, silence_contextmanager


def guess_gadget_name(browser):
    """
    function that tries to guess gadget name by analyzing its text
    """
    text = browser.xpath('//body').get_attribute('innerText')[:50]
    return text.strip().split('\n', 1)[0].strip()


def get_loaded_gadgets_list(browser, desire_gadget_name=None):
    """
    Returns list of currently loaded gadgets.
    """
    browser.switch_to_default_content()
    with silence_contextmanager(browser):
        gadgets = browser.xpath(
            '//iframe[contains(@id, "__gadget_")]', eager=True, timeout=1)
    if not gadgets:
        return
    gadget_name_to_iframe_id = {}
    for gadget in gadgets:
        gadget_id = gadget.get_attribute('id')
        browser.switch_to_frame(gadget_id)
        try:
            gadget_name = guess_gadget_name(browser)
        finally:
            browser.switch_to_default_content()
        if not gadget_name:
            continue
        gadget_name_to_iframe_id[gadget_id] = gadget_name
        # There is no sufficient way to get PlugIn name, but usually
        # plugins innerText starts with PlugIn name, so
        # we cat try to guess...
        if gadget_name.startswith(desire_gadget_name):
            return gadget_id
    return None if desire_gadget_name else gadget_name_to_iframe_id


def open_app(self, gadget_name):
    """
    Opens Hangout PlugIn by provided name.
    """
    if guess_gadget_name(self.base.browser).startswith(gadget_name):
        return
    self.base.click_cancel_button_if_there_is_one()
    gadget_id = get_loaded_gadgets_list(self.base.browser, gadget_name)
    if not gadget_id or not self.base.browser.by_id(gadget_id).is_displayed():
        gadget_icon = self.base.browser.xpath(
            '//div[@aria-label="%s"]' % gadget_name)
        if gadget_icon.location['x'] < 0:
            self.base.browser.by_class('Za-Ja-m').click(timeout=0.5)
        gadget_icon.click(timeout=1)
        gadget_id = tries_n_time_until_true(
            lambda: get_loaded_gadgets_list(self.base.browser, gadget_name))
    self.base.browser.switch_to_frame(gadget_id)


def gadget_context_handler(gadget_name):
    """
    Decorator context handler for gadgets.
    Make sure that current browser context is set to work with provided PlugIn
    """
    def decorator(function):  # pylint: disable=C0111
        @wraps(function)
        def wrapper(self, *args, **kwargs):  # pylint: disable=C0111
            open_app(self, gadget_name)
            return function(self, *args, **kwargs)
        return wrapper
    return decorator
