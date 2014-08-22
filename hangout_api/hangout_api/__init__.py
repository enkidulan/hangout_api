"""
Python API for controlling Google+ Hangouts
===========================================
"""
import os.path
from os.path import join
from time import sleep
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyvirtualdisplay.smartdisplay import SmartDisplay
import seleniumwrapper as selwrap


parret_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMEDRIVER_PATH = join(parret_dir_path, 'CHROMEDRIVER')


class LoginError(BaseException):
    pass



class Hangouts():
    """
    Base class that provide all bunch of options.
    """

    cookies_dump_path = "cookies.pkl"  # XXX: bad path should be in user conf path

    def __init__(self):
        """
        On initialization new browser session are created.
        """
        # lets start display in case if no is available
        self.display = None
        if not os.environ.get('DISPLAY'):
            self.display = SmartDisplay()
            self.display.start()

        self.browser = selwrap.create(
            "chrome", executable_path=CHROMEDRIVER_PATH)
        self.browser.timeout = 5

        # # XXX: Loading browser cookies:
        # # TODO: it's probably better to have custom persistent FF data patch
        # if os.path.isfile(self.cookies_dump_path):
        #     self.browser.get('https://accounts.google.com/ServiceLogin')
        #     cookies = pickle.load(open(self.cookies_dump_path, "rb"))
        #     for cookie in cookies:
        #         self.browser.add_cookie(cookie)
        #     self.browser.get('https://plus.google.com/hangouts/active')

    def start(self, onair=False):
        if not self.browser.current_url.startswith('https://plus.google.com/hangouts/active'):
            self.browser.get('https://plus.google.com/hangouts/active')
        self.browser.by_class('opd').click()
        # G+ opens new window for new hangout, so we need to switch selenium to
        # it

        # waiting until new window appears
        while len(self.browser.window_handles) <= 1:
            sleep(0.2)  # XXX: add waiting for second window to open
        self.browser.close()  # closing old window
        # 'Google+' title
        self.browser.switch_to_window(self.browser.window_handles[0])
        # XXX: Saving cookies
        # with open(self.cookies_dump_path, "wb") as cookies_dump:
        #     pickle.dump(self.browser.get_cookies(), cookies_dump)
        # and close dialog window
        # close the inviting popup
        self.browser.xpath('//div[@id=":sd.Qf" or @id=":se.Qf"]').click()

    @property
    def is_logged_in(self):
        # XXX: slow and ugly
        status = self.browser.current_url.startswith('https://plus.google.com/')
        status = status or self.browser.current_url.startswith('https://www.google.com/settings/personalinfo')
        # import pdb; pdb.set_trace()
        return status

    def login(self, username=None, password=None, otp=None):
        self.browser.get('https://accounts.google.com/ServiceLogin')

        # Log in - input name pass and press Log in
        self.browser.by_id('Email').send_keys(username)
        self.browser.by_id('Passwd').send_keys(password)
        self.browser.by_id('signIn').click()

        # filling up opt
        if otp:
            self.browser.by_id('smsUserPin').send_keys(otp)
            self.browser.by_id('smsVerifyPin').click()

        # XXX: checking if log in was successful
        if not self.is_logged_in:
            raise LoginError('Wasn\'t able to login. Check if credentials are correct.')

        # # Saving cookies
        # with open(self.cookies_dump_path, "wb") as cookies_dump:
        #     pickle.dump(self.browser.get_cookies(), cookies_dump)

    def regex_xpat(self, xpath, sufix, attr='id'):
        # XXX
        self.browser.silent = True
        try:
            nodes = self.browser.xpath(xpath, timeout=0.01, eager=True) or ()
        finally:
            self.browser.silent = False
        targets = [i for i in nodes if i.attr(attr).endswith(sufix)]
        if targets:
                return targets[0]

    def click_cancel_button_if_there_is_one(self):
        # this function close all menus and return browser to staring state
        # xpath = '//div[matches(@id, "^.*?\.Jt.*$"]'  # TODO: xpath
        cancel_button = self.regex_xpat(
            '//div[@class="d-w-R"]/div/div[@id]', sufix=".Jt")
        if cancel_button is not None:
            cancel_button.click()

    def navigate_to_devices_settings(self):
        self.click_cancel_button_if_there_is_one()
        # making nav link visible
        # webdriver.ActionChains(self.browser).move_to_element(self.browser.by_id(':tc.ct')).perform()
        try:
            self.browser.by_class('MQ', timeout=0.3).click()
        except:  # XXX
            self.browser.by_class('Za-Ja-m').click()
            # click on it
            self.browser.by_class('MQ').click()

    def open_mics_devices_list(self):
        self.navigate_to_devices_settings()
        # click on MC list to make it load list of all devices
        self.browser.by_class('qd-pc-kg').click()

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
        self.mics_list = mics.keys()
        if with_nodes:
            return mics
        return self.mics_list

    def set_microphone_devices(self, name):
        # TODO: make sure that browser is on needed context
        self.get_microphone_devices(with_nodes=True)[name].click()
        # click save button
        self.regex_xpat('//div[@class="d-w-R"]/div/div[@id]', sufix=".Ut").click()

    def __del__(self):
        try:
            self.browser.quit()
        finally:
            if self.display is not None:
                self.display.stop()
