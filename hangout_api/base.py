import os.path
from time import sleep
from pyvirtualdisplay.smartdisplay import SmartDisplay
import seleniumwrapper as selwrap
from chromedriver import CHROMEDRV_PATH
from .utils import NavigationHelpers, URLS
from .exceptions import LoginError


class Hangouts(NavigationHelpers):
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

        self.browser = selwrap.create(
            browser, executable_path=executable_path or CHROMEDRV_PATH)

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

    def set_microphone_devices(self, name):
        # TODO: make sure that browser is on needed context
        self.get_microphone_devices(with_nodes=True)[name].click()
        # click save button
        self.click_on_devices_save_button()

    # def get_video_devices(self, with_nodes=False):
    #     raise
    #     # self.open_mics_devices_list()
    #     # TODO: add caching ??? do we need this? there
    #     #       is self.video_devices prop
    #     # get list of devices
    #     # import pdb; pdb.set_trace()
    #     # video_dev_xpath =
    #'//div[@class="c-i c-i-Ed Hz"]/div/div[@class="c-k-t"]'
    #     # video_devices = {
    #     #     node.get_attribute('innerText'): node
    #     #     for node in
    #self.browser.find_elements_by_xpath(video_dev_xpath)}
    #     # self.video_devices = list(video_devices.keys())
    #     # if with_nodes:
    #     #     return video_devices
    #     # return self.video_devices

    # def set_video_devices(self, name):
    #     # TODO: make sure that browser is on needed context
    #     self.get_video_devices(with_nodes=True)[name].click()
    #     self.click_on_devices_save_button()

    def _get_bandwidth_controooller(self):
        limit_bandwidth_xpath = '//div[text()="Limit Bandwidth"]'
        if not self.browser.xpath(limit_bandwidth_xpath).is_displayed():
            # no need to open bandwidth settings tab if it's opened already
            self.click_menu_element(
                '//div[@aria-label="Adjust bandwidth usage"]')
        return self.browser.xpath(
            '//div[@aria-label="Adjust the quality of your video"]')

    def set_bandwidth(self, bandwidth):
        """
        Set bandwidth setting for hangout:
            * 0 - Audio only
            * 1 - Very Low
            * 2 - Low
            * 3 - Medium
            * 4 - Auto HD
        """
        controller = self._get_bandwidth_controooller()
        levels = controller.by_class('Sa-IU-HT', eager=True)
        # setting levels
        levels[bandwidth].click(timeout=0.5)

    def get_bandwidth(self):
        """
        Get bandwidth setting for hangout
        """
        controller = self._get_bandwidth_controooller()
        return int(controller.get_attribute('aria-valuenow'))

    def unmute_audio(self):
        """
        Un-mute audio device. Returns:
            * True - Audio went from muted to un-muted
            * False - Audio was already un-muted
        """
        self.click_cancel_button_if_there_is_one()
        xpath = '//div[contains(@aria-label, "ute microphone")]'
        mute_button = self.browser.xpath(xpath)
        if mute_button.get_attribute('aria-label') == 'Mute microphone':
            return False
        self.click_menu_element(xpath)
        return True

    def mute_audio(self):
        """
        Mute audio device. Returns:
            * True - Audio went from un-muted to muted
            * False - Audio was already muted
        """
        self.click_cancel_button_if_there_is_one()
        xpath = '//div[contains(@aria-label, "ute microphone")]'
        mute_button = self.browser.xpath(xpath)
        if mute_button.get_attribute('aria-label') == 'Unmute microphone':
            return False
        self.click_menu_element(xpath)
        return True

    def mute_video(self):
        """
        Mute video device. Returns:
            * True - Video went from un-muted to muted
            * False - Video was already muted
        """
        self.click_cancel_button_if_there_is_one()
        xpath = '//div[contains(@aria-label, "Turn camera")]'
        mute_button = self.browser.xpath(xpath)
        if mute_button.get_attribute('aria-label') == 'Turn camera on':
            return False
        self.click_menu_element(xpath)
        return True

    def unmute_video(self):
        """
        Un-mute video device. Returns:
            * True - Video went from muted to un-muted
            * False - Video was already un-muted
        """
        self.click_cancel_button_if_there_is_one()
        xpath = '//div[contains(@aria-label, "Turn camera")]'
        mute_button = self.browser.xpath(xpath)
        if mute_button.get_attribute('aria-label') == 'Turn camera off':
            return False
        self.click_menu_element(xpath)
        return True

    def get_audio_devices(self, with_nodes=False):
        self.navigate_to_devices_settings()
        # click on MC list to make it load list of all devices
        self.browser.by_class('iph_s_ao').click(timeout=0.5)

        # get list of devices
        xpath = '//div[@class="c-i c-i-Ed Iz"]/div/div[@class="c-k-t"]'
        audio_devices = {
            node.get_attribute('innerText'): node
            for node in self.browser.xpath(xpath, eager=True)}
        if with_nodes:
            return audio_devices
        return list(audio_devices.keys())

    def set_audio_devices(self, device_name):
        # TODO: make sure that browser is on needed context
        self.get_audio_devices(with_nodes=True)[device_name].click()
        # click save button
        self.click_on_devices_save_button()

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
