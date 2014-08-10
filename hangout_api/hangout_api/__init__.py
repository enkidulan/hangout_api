"""
Python API for controlling Google+ Hangouts
===========================================
"""
import os.path
from os.path import join
from time import sleep
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


def switch_window_to_new_session(browser):
    while len(browser.window_handles) <= 1:
        sleep(0.2)  # XXX: add waiting for second window to open
    browser.close()  # closing old window
    # 'Google+' title
    browser.switch_to_window(browser.window_handles[-1])


class Hangouts():
    """
    Base class that provide all bunch of options.
    """
    def __init__(self, username=None, password=None, otp=None):
        """
        On initialization new browser session are created and user logs in
        by providing its credential to class or by entering them manually
        in browser log in page.
        """
        # lets start display in case if no is available
        self.display = None
        if not os.environ.get('DISPLAY'):
            self.display = SmartDisplay(visible=0, bgcolor='black')
            self.display.start()

        self.browser = selwrap.create(
            "chrome", executable_path=CHROMEDRIVER_PATH)
        self.browser.get('https://plus.google.com/hangouts/active')
        self.browser.by_class('opd').click()

        switch_window_to_new_session(self.browser)

        # Log in - input name pass and press Log in
        self.browser.by_id('Email').send_keys(username)
        self.browser.by_id('Passwd').send_keys(password)
        self.browser.by_id('signIn').click()

        # filling up opt
        if otp:
            self.browser.by_id('smsUserPin').send_keys(otp)
            self.browser.by_id('smsVerifyPin').click()

        # checking if log in was successful
        try:
            self.browser.xpath('//title[text()="Google+ Hangouts"]')
        except TimeoutException:
            raise LoginError(
                'Wasn\'t able to login. Check if credentials are correct.')

    def __del__(self):
        self.browser.quit()
        if self.display is not None:
            self.display.stop()
