from easydict import EasyDict


URLS = EasyDict(
    hangout_session_base='https://plus.google.com/hangouts/_/',
    hangouts_active_list='https://plus.google.com/hangouts/active',
    plus_main='https://plus.google.com/',
    personalinfo='https://www.google.com/settings/personalinfo',
    service_login='https://accounts.google.com/ServiceLogin',
)


class NavigationHelpers():
    """
    Batch of function to navigate through G+ Hangout to keep main API
    class cleaner
    """

    def click_menu_element(self, xpath, func='xpath'):
        self.click_cancel_button_if_there_is_one()
        menu_button = getattr(self.browser, func)(xpath)
        if not menu_button.is_displayed():
            # if menu buttons is hidden make them displayed
            self.browser.by_class('Za-Ja-m').click(timeout=0.5)
        menu_button.click(0.5)

    def click_cancel_button_if_there_is_one(self, timeout=0.5):
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
        Returns True if loged in, otherwise returns False.
        Be careful this function analyzing current URL to determinate
        if user loged in or not.
        """
        return self.browser.current_url.startswith(URLS.plus_main) or \
            self.browser.current_url.startswith(URLS.personalinfo)

    def navigate_to_devices_settings(self):
        self.click_menu_element('MQ', func='by_class')

    def open_mics_devices_list(self):
        self.navigate_to_devices_settings()
        # click on MC list to make it load list of all devices
        self.browser.by_text('Microphone').parent.click(timeout=0.5)

    def click_on_devices_save_button(self):
        xpath = '//div[text()="Save"]'
        self.browser.xpath(xpath).click(timeout=0.5)

    def get_microphone_devices(self, with_nodes=False):
        self.open_mics_devices_list()
        # TODO: add caching
        # if self.mics_list is not None:
            # return self.mics_list.keys()
        # get list of devices
        xpath = '//div[@class="c-i c-i-Ed Hz"]/div/div[@class="c-k-t"]'
        mics = {
            node.get_attribute('innerText'): node
            for node in self.browser.find_elements_by_xpath(xpath)}
        self.mics_list = list(mics.keys())
        if with_nodes:
            return mics
        return self.mics_list
