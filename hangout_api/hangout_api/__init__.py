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
            self.display = SmartDisplay(visible=0, bgcolor='black')
            self.display.start()

        self.browser = selwrap.create(
            "chrome", executable_path=CHROMEDRIVER_PATH)

        # # XXX: Loading browser cookies:
        # # TODO: it's probably better to have custom persistent FF data patch
        # if os.path.isfile(self.cookies_dump_path):
        #     self.browser.get('https://accounts.google.com/ServiceLogin')
        #     cookies = pickle.load(open(self.cookies_dump_path, "rb"))
        #     for cookie in cookies:
        #         self.browser.add_cookie(cookie)
        #     self.browser.get('https://plus.google.com/hangouts/active')

    def switch_window_to_new_session(self):
        while len(self.browser.window_handles) <= 1:
            sleep(0.2)  # XXX: add waiting for second window to open
        self.browser.close()  # closing old window
        # 'Google+' title
        self.browser.switch_to_window(self.browser.window_handles[-1])
        # XXX: Saving cookies
        # with open(self.cookies_dump_path, "wb") as cookies_dump:
        #     pickle.dump(self.browser.get_cookies(), cookies_dump)

    def start(self, onair=False):
        if not self.browser.current_url.startswith('https://plus.google.com/hangouts/active'):
            self.browser.get('https://plus.google.com/hangouts/active')
        self.browser.by_class('opd').click()
        self.switch_window_to_new_session()

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

    def __del__(self):
        try:
            self.browser.quit()
        finally:
            if self.display is not None:
                self.display.stop()
