import os.path
from time import sleep
from pyvirtualdisplay.smartdisplay import SmartDisplay
import seleniumwrapper as selwrap
from chromedriver import CHROMEDRV_PATH
from .utils import NavigationHelpers, URLS
from .exceptions import LoginError
from .settings import BaseSettings


class Hangouts(NavigationHelpers, BaseSettings):
    """
    Base class that provide all bunch of options.

    """

    # TODO: how to show self.display, self.browser and self.hangout_id in
    #       docs?

    def __init__(self, browser="chrome", executable_path=None):
        """
        Initialization does two things:
            1. Makes sure that there is active X session.
            2. Starts browser.

        On initialization it stats X session if can't find 'DISPLAY' in
        os.environ. For this purposes used *pyvirtualdisplay* package.

        For handling browser used seleniumwrapper library.

        """
        # lets start display in case if no is available
        self.hangout_id = None

        self.display = None
        if not os.environ.get('DISPLAY'):
            self.display = SmartDisplay()
            self.display.start()

        kwargs = {}
        if browser == "chrome":
            kwargs['executable_path'] = executable_path or CHROMEDRV_PATH
        self.browser = selwrap.create(browser, **kwargs)

    def start(self, onair=False):
        """
        Start new hangout.
        """
        if not self.browser.current_url.startswith(URLS.hangouts_active_list):
            self.browser.get(URLS.hangouts_active_list)

        self.browser.by_class('opd').click(timeout=0.5)
        # G+ opens new window for new hangout, so we need to switch selenium to
        # it

        # waiting until new window appears
        while len(self.browser.window_handles) <= 1:
            sleep(0.2)  # XXX: add waiting for second window to open
        self.browser.close()  # closing old window
        # TODO: 'Google+' title
        self.browser.switch_to_window(self.browser.window_handles[0])

        self.click_cancel_button_if_there_is_one(timeout=30)

        # setting hangout id property
        self.hangout_id = self.browser.current_url.replace(
            URLS.hangout_session_base, '', 1).split('?', 1)[0]

    def connect(self, hangout_id):
        """
        Connect to an existing hangout.
        Takes id of targeted hangout as argument
        """
        self.hangout_id = hangout_id
        self.browser.get(URLS.hangout_session_base + hangout_id)
        # there may be a big delay before 'Join' button appears, so we need
        # to add longer timeout for this
        self.browser.by_text('Join', timeout=60).click(timeout=0.5)

    def login(self, username=None, password=None, otp=None):
        """
        Log into google plus account.

        *opt* argument is one time password and is optional,
        set it only if you're 2-factor authorization

        """

        # Open login form and sing in with credentials
        self.browser.get(URLS.service_login)
        self.browser.by_id('Email').send_keys(username)
        self.browser.by_id('Passwd').send_keys(password)
        self.browser.by_id('signIn').click(timeout=0.5)

        # filling up one time password if provides
        if otp:
            self.browser.by_id('smsUserPin').send_keys(otp)
            self.browser.by_id('smsVerifyPin').click(timeout=0.5)

        # checking if log in was successful
        if not self.is_logged_in:
            raise LoginError(
                'Wasn\'t able to login. Check if credentials are correct'
                'and make sure that you have G+ account activated')

    def invite(self, participants):
        """
        Invite person or circle to hangout
            >>> hangout.invite("persona@gmail.com")
            >>> hangout.invite(["personb@gmail.com", "Circle Name A"])
        """
        self.click_cancel_button_if_there_is_one()
        if not any(isinstance(participants, i) for i in (list, tuple)):
            participants = [participants, ]
        # click on Invite People button
        self.click_menu_element('//div[@aria-label="Invite People"]')
        input = self.browser.xpath(
            '//input[@placeholder="+ Add names, circles, or email addresses"]')
        input.send_keys("\n".join(participants) + "\n\n")
        self.browser.by_text('Invite').click(timeout=0.5)

    def participants(self):
        """
        Returns list of current participants
            >>> hangout.participants()
            ['John Doe', ...]
        """
        xpath = '//div[@aria-label="Video call participants"]/div'
        participants = self.browser.xpath(xpath, eager=True)
        return [p.get_attribute('aria-label').split('Open menu for ')[1]
                for p in participants]

    def leave_call(self):
        """
        Leave hangout. EQ to click on "Leave call" button.
        """
        self.click_menu_element('//div[@aria-label="Leave call"]')

    def __del__(self):
        # leaving the call first
        self.browser.silent = True
        try:
            self.leave_call()
        except:
            pass
        try:
            self.browser.quit()
        finally:
            if self.display is not None:
                self.display.stop()
