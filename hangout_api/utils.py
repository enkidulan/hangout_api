"""
Usefull code pices for HG API, like list if important URLs and
navigation helpers.
"""
# pylint can't handle EasyDict properly
# pylint: disable=E1101

from easydict import EasyDict
from time import sleep
from collections import namedtuple


Participant = namedtuple('Participant', ['name', 'profile_id'])


URLS = EasyDict(
    hangout_session_base='https://plus.google.com/hangouts/_/',
    hangouts_active_list='https://plus.google.com/hangouts/active',
    plus_main='https://plus.google.com/',
    personalinfo='https://www.google.com/settings/personalinfo',
    service_login='https://accounts.google.com/ServiceLogin',
)


class Utils(object):
    """
    Batch of function to navigate through G+ Hangout to keep main API
    class cleaner
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

    def click_menu_element(self, xpath, func='xpath'):
        """
        Make items menu to show out if it is hidden and click on its element
        provided by 'xpath' argumet
        """
        self.click_cancel_button_if_there_is_one()
        menu_button = getattr(self.browser, func)(xpath)
        if not menu_button.is_displayed():
            # if menu buttons is hidden make them displayed
            self.browser.by_class('Za-Ja-m').click(timeout=0.5)
        menu_button.click(0.5)

    # pylint: disable=C0103
    def click_cancel_button_if_there_is_one(self, timeout=0.5):
        """
        If somewhere on page is visible "cancel" or "close" button, this
        method will click on it
        """
        self.browser.switch_to_default_content()
        # this function close all menus and return browser to staring state
        origin_state = self.browser.silent
        self.browser.silent = True
        xpath = '//*[text()="Cancel" or text()="Close"]'
        try:
            # We're looking for text because are id's are hangable
            # and something weird is going on about css selectors
            cancel_buttons = self.browser.xpath(
                xpath, timeout=timeout, eager=True)
        finally:
            self.browser.silent = origin_state
        if cancel_buttons is not None:
            for cancel_button in cancel_buttons:
                if cancel_button.is_displayed():
                    cancel_button.click(timeout=timeout)

    @property
    def is_logged_in(self):
        """
        Returns True if user is loged in, otherwise returns False.
        Be careful this function analyzing current URL to determinate
        if user loged in or not.
        """
        is_logged_in = lambda: \
            self.browser.current_url.startswith(URLS.plus_main) or \
            self.browser.current_url.startswith(URLS.personalinfo)
        try_num = 0
        while try_num < 10:
            if is_logged_in():
                return True
            sleep(0.1)
            try_num += 1
        return False

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
        self.browser.xpath(xpath).click(timeout=0.5)
