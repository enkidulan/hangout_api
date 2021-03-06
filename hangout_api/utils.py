"""
Usefull code pices for HG API, like list if important URLs and
navigation helpers.
"""
# pylint can't handle EasyDict properly
# pylint: disable=E1101

from easydict import EasyDict
from time import sleep
from collections import namedtuple
from contextlib import contextmanager
from retrying import retry


Participant = namedtuple('Participant', ['name', 'profile_id'])


URLS = EasyDict(
    hangout_session_base='https://plus.google.com/hangouts/_/',
    hangouts_active_list='https://plus.google.com/hangouts/active',
    onair='https://plus.google.com/hangouts/onair',
    plus_main='https://plus.google.com/',
    personalinfo='https://www.google.com/settings/personalinfo',
    service_login='https://accounts.google.com/ServiceLogin',
    my_account_page='https://myaccount.google.com/',
)


class Timeouts(object):
    # pylint: disable=too-few-public-methods, no-init
    """
    Timeouts helper, contain set of used timeouts for easier management
    """
    immediately = 1
    fast = 5
    average = 30
    long = 90
    extralong = 240

TIMEOUTS = Timeouts()


def names_cleaner(name):
    """
    Helper function to clean up string from 'thml' symbols
    """
    # pylint: disable=W1402
    return name.replace('\u202a', '').replace('\u202c', '').strip()


@contextmanager
def silence_contextmanager(node):
    """
    Context manager to preform operations 'silently'
    """
    origin = node.silent
    node.silent = True
    try:
        yield
    finally:
        node.silent = origin


def tries_n_time_until_true(func, try_num=10):
    """
    Helper that repeats some action unlit its returns something
    different from  False or None. Returns Function result
    """
    while try_num:
        val = func()
        if val:
            return val
        sleep(0.1)
        try_num -= 1
    return False


@retry(stop_max_attempt_number=3)
def click_on_app_icon(browser, xpath, func='xpath'):
    """
    Clicks on app icon on menu panel
    """
    gadget_icon = getattr(browser, func)(xpath)
    if gadget_icon.location['x'] < 0 or not gadget_icon.is_displayed():
        browser.by_class('Za-Ja-m').click(timeout=TIMEOUTS.fast)
    gadget_icon.click(timeout=TIMEOUTS.fast)


class Utils(object):
    """
    Batch of function to navigate through G+ Hangout to keep main API
    class cleaner
    """
    browser = None
    """
    Instance of the `seleniumwrapper`_ library

    .. _seleniumwrapper: https://pypi.python.org/pypi/seleniumwrapper/

    """

    def __init__(self, browser):
        self.browser = browser

    def set_text(self, node, text):
        """
        Helper to remove text from input and then set text to it.
        Takes xpath or selenium node and text.
        """
        if isinstance(node, str):
            node = self.browser.xpath(node)
        node.clear()
        node.send_keys(text)

    @retry(stop_max_attempt_number=3)
    def click_menu_element(self, xpath, func='xpath'):
        """
        Make items menu to show out if it is hidden and click on its element
        provided by 'xpath' argumet
        """
        self.click_cancel_button_if_there_is_one()
        click_on_app_icon(self.browser, xpath, func)

    # pylint: disable=C0103
    @retry(stop_max_attempt_number=3)
    def click_cancel_button_if_there_is_one(self, timeout=1):
        """
        If somewhere on page is visible "cancel" or "close" button, this
        method will click on it
        """
        self.browser.switch_to_default_content()
        # this function close all menus and return browser to staring state
        xpath = '//*[text()="Cancel" or text()="Close" or text()="Skip"]'
        with silence_contextmanager(self.browser):
            # We're looking for text because are id's are hangable
            # and something weird is going on about css selectors
            cancel_buttons = self.browser.xpath(
                xpath, timeout=timeout, eager=True)
        if cancel_buttons is not None:
            for cancel_button in cancel_buttons:
                if cancel_button.is_displayed():
                    cancel_button.click(timeout=timeout)

    @property
    @retry(stop_max_attempt_number=3)
    def is_logged_in(self):
        """
        Returns True if user is loged in, otherwise returns False.
        Be careful this function analyzing current URL to determinate
        if user loged in or not.
        """
        def _is_logged_in():
            """
            simple function wrapper to check in user is logged in
            """
            return \
                self.browser.current_url.startswith(URLS.plus_main) or \
                self.browser.current_url.startswith(URLS.personalinfo) or \
                self.browser.current_url.startswith(URLS.my_account_page)
        return tries_n_time_until_true(_is_logged_in)

    @retry(stop_max_attempt_number=3)
    def navigate_to_devices_settings(self):
        """
        Opens dialog box for device setting in HG call.
        """
        self.click_menu_element('MQ', func='by_class')

    def click_on_devices_save_button(self):
        """
        Clicks on button with text "Save"
        """
        xpath = '//div[text()="Save"]'
        self.browser.xpath(xpath).click(timeout=TIMEOUTS.fast)
