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


parret_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMEDRIVER_PATH = join(parret_dir_path, 'CHROMEDRIVER')


class LoginError(BaseException):
    pass


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

        self.browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)
        self.wait = WebDriverWait(self.browser, 10)
        self.browser.get('https://plus.google.com/hangouts/active')
        element = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'opd')))
        element.click()

        sleep(4)  # XXX: add waiting for second window to open
        self.browser.close()  # closing old window

        # 'Google+' title
        self.browser.switch_to_window(self.browser.window_handles[-1])

        # Log in - input name pass and press Log in
        element = self.wait.until(EC.element_to_be_clickable((By.ID, 'Email')))
        element.send_keys(username)
        element = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'Passwd')))
        element.send_keys(password)
        element = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'signIn')))
        element.click()

        # filling up opt
        if otp:
            element = self.wait.until(
                EC.element_to_be_clickable((By.ID, 'smsUserPin')))
            element.send_keys(otp)
            element = self.wait.until(
                EC.element_to_be_clickable((By.ID, 'smsVerifyPin')))
            element.click()

        # checking if log in was successful
        try:
            element = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//title[text()="Google+ Hangouts"]')))
        except TimeoutException:
            raise LoginError(
                'Wasn\'t able to login. Check if credentials are correct.')

    def __del__(self):
        self.browser.quit()
        if self.display is not None:
            self.display.stop()
