"""
Hangout API
===========

Main module of Hangout that provide base HG management and call settings
management.

"""
# pylint can't handle EasyDict properly
# pylint: disable=E1101
import os.path
from pyvirtualdisplay.smartdisplay import SmartDisplay
import seleniumwrapper as selwrap
from chromedriver import CHROMEDRV_PATH
from zope.component import getUtilitiesFor

from .utils import (
    Utils,
    URLS,
    Participant,
    tries_n_time_until_true,
    names_cleaner,
)
from .exceptions import LoginError
from .interfaces import IModule, IOnAirModule


def _create_hangout_event(browser, name, attendees):
    """
    Creates hangout event on google plus. As arguments takes event name and
    attendees list, also should be provided with 'browser' object where
    visitor is logged in
    """
    browser.get(URLS.onair)
    browser.by_text('Start a Hangout On Air').click(0.5)
    # Setting name
    browser.xpath(
        '//input[@aria-label="Give it a name"]').send_keys(name)
    # cleaning 'share' field and send attendees list there
    browser.xpath(
        '//input[@aria-label="Add more people"]').send_keys(
            '\b\b\b' + ','.join(attendees) + ',')
    browser.xpath(
        '//*[@guidedhelpid="shareboxcontrols"]//*[text()="Share"]').click(0.5)
    # waiting for redirecting to OnAir event page to be complete
    browser.xpath('//div[@data-tooltip="Start the Hangout On Air"]', timeout=60)
    return browser.current_url


class Hangouts(object):
    """
    Main class for controlling hangout calls.

    """

    def __init__(self, executable_path=None, chrome_options=None):
        """
        Initialization does two things:
            1. Makes sure that there is active X session.
            2. Starts the browser.

        If 'DISPLAY' can't be found in os.environ than new X session starts.
        Starting new session handels `PyVirtualDisplay`_.

        .. _PyVirtualDisplay: http://ponty.github.io/PyVirtualDisplay/

        For handling browser used seleniumwrapper library.

        """
        self.hangout_id = None
        self.on_air = None

        # lets start display in case if no is available
        self.display = None
        if not os.environ.get('DISPLAY'):
            self.display = SmartDisplay()
            self.display.start()

        kwargs = {'executable_path': executable_path or CHROMEDRV_PATH}
        if chrome_options is not None:
            kwargs['chrome_options'] = chrome_options
        # pylint: disable=W0142
        self.browser = selwrap.create('chrome', **kwargs)

        self.utils = Utils(self.browser)
        for name, instance in getUtilitiesFor(IModule):
            setattr(self, name, instance(self.utils))

    def start(self, on_air=None):
        """
        Start a new hangout.
        After new hangout is created its id is stored in 'hangout_id' attribure

        .. code::

            >>> hangout.hangout_id
            None
            >>> hangout.start()
            >>> hangout.hangout_id
            'gs4pp6g62w65moctfqsvihzq2qa'

        """

        # onair
        if on_air is not None:
            self.on_air = on_air
            if isinstance(on_air, dict):
                # in case if on_air is a dict create new hangout event
                _create_hangout_event(
                    self.browser, on_air['name'], on_air['attendees'])
            else:
                # otherwise (hangout is a string) go to event page
                self.browser.get(on_air)
            # on event page, redirecting can take some time
            self.browser.xpath(
                '//div[@data-tooltip="Start the Hangout On Air"]',
                timeout=60).click(0.5)
            for name, instance in getUtilitiesFor(IOnAirModule):
                setattr(self, name, instance(self.utils))

        else:
            if not self.browser.current_url.startswith(
                    URLS.hangouts_active_list):
                self.browser.get(URLS.hangouts_active_list)
            # G+ opens new window for new hangout, so we need to
            # switch selenium to it
            self.browser.by_class('opd').click(timeout=0.5)

        # waiting until new window appears
        tries_n_time_until_true(
            lambda: len(self.browser.window_handles) <= 1, try_num=100)

        # self.browser.close()  # closing old window
        self.browser.switch_to_window(self.browser.window_handles[-1])

        self.utils.click_cancel_button_if_there_is_one(timeout=30)

        if self.on_air:
            #  waiting for broadcasting to be ready
            broadcast_button = self.browser.by_text(
                'Start broadcast', timeout=60)
            tries_n_time_until_true(broadcast_button.is_displayed, try_num=600)

        # setting hangout id property
        self.hangout_id = self.browser.current_url.replace(
            URLS.hangout_session_base, '', 1).split('?', 1)[0]

    def connect(self, hangout_id):
        """
        Connect to an existing hangout.
        Takes id of targeted hangout as argument.
        Also it sets hangout_id property:

        .. code::

            >>> hangout.hangout_id
            None
            >>> hangout.connect('gs4pp6g62w65moctfqsvihzq2qa')
            >>> hangout.hangout_id
            'gs4pp6g62w65moctfqsvihzq2qa'


        """
        self.hangout_id = hangout_id
        self.browser.get(URLS.hangout_session_base + hangout_id)
        # there may be a big delay before 'Join' button appears, so there is a
        #  need wait longer than usual
        join_button = self.browser.xpath(
            '//*[text()="Join" or text()="Okay, got it!"]', timeout=40)
        button_text = names_cleaner(join_button.get_attribute('innerText'))
        if button_text == 'Okay, got it!':
            # to join hangout we need to set agreement checkbox
            self.browser.xpath('//*[@role="presentation"]').click(timeout=0.5)
            join_button.click(timeout=5)
        self.browser.by_text('Join', timeout=40).click(timeout=0.5)

    def login(self, username=None, password=None, otp=None):
        """
        Log in to google plus.

        *otp* argument is one time password and it's optional,
        set it only if you're using 2-factor authorization.

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
        if not self.utils.is_logged_in:
            raise LoginError(
                'Wasn\'t able to login. Check if credentials are correct'
                'and make sure that you have G+ account activated')

    def invite(self, participants):
        """
        Invite person or circle to hangout:

        .. code::

            >>> hangout.invite("persona@gmail.com")
            >>> hangout.invite(["personb@gmail.com", "Public", "Friends"])

        """
        self.utils.click_cancel_button_if_there_is_one()
        if not any(isinstance(participants, i) for i in (list, tuple)):
            participants = [participants, ]
        # click on Invite People button
        self.utils.click_menu_element('//div[@aria-label="Invite People"]')
        input_field = self.browser.xpath(
            '//input[@placeholder="+ Add names, circles, or email addresses"]')
        input_field.send_keys("\n".join(participants) + "\n\n")
        self.browser.by_text('Invite').click(timeout=0.5)

    def participants(self):
        """
        Returns list of namedtuples of current participants:

        .. code::

            >>> hangout.participants()
            [Participant(name='John Doe',
                         profile_id='108775712935793912532'),
             Participant(name='Lorem Impus',
                         profile_id='115041713348329690244')]
        """
        xpath = '//div[@data-userid]'
        participants = self.browser.xpath(xpath, eager=True)
        return [Participant(p.get_attribute('aria-label')[5:-11],
                            p.get_attribute('data-userid'))
                for p in participants]

    def disconnect(self):
        """
        Leave hangout (equal on clicking on "Leave call" button). After
        leaving the call you can create a new one or connect to existing.
        """
        self.utils.click_cancel_button_if_there_is_one()
        self.utils.click_menu_element('//div[@aria-label="Leave call"]')
        self.hangout_id = None
        if self.on_air is not None:
            # removing properties that is available only for OnAir
            for name, _ in getUtilitiesFor(IOnAirModule):
                delattr(self, name)
            self.on_air = None
        # waiting until hangout windows closes
        tries_n_time_until_true(
            lambda: len(self.browser.window_handles) == 1, try_num=100)
        self.browser.switch_to_window(self.browser.window_handles[-1])

    def __del__(self):
        # leaving the call first
        try:
            if self.hangout_id:
                self.disconnect()
        finally:
            # and quiting browser and display
            self.browser.quit()
            if self.display is not None:
                self.display.stop()
