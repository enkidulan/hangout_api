"""
Python API for controlling Google+ Hangouts
===========================================
"""
import os.path
from os.path import join
from time import sleep
# import pickle
from pyvirtualdisplay.smartdisplay import SmartDisplay
import seleniumwrapper as selwrap


parret_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMEDRIVER_PATH = join(parret_dir_path, 'CHROMEDRIVER')
BASE_HANGOUT_URL = 'https://plus.google.com/hangouts/_/'


class LoginError(BaseException):
    pass


class Hangouts():
    """
    Base class that provide all bunch of options.
    """

    # cookies_dump_path = "cookies.pkl"  # XXX: bad path should be in user conf path

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

        self.browser.timeout = 4
        self.hangout_id = None

        # # XXX: Loading browser cookies:
        # # TODO: it's probably better to have custom persistent FF data patch
        # if os.path.isfile(self.cookies_dump_path):
        #     self.browser.get('https://accounts.google.com/ServiceLogin')
        #     cookies = pickle.load(open(self.cookies_dump_path, "rb"))
        #     for cookie in cookies:
        #         self.browser.add_cookie(cookie)
        #     self.browser.get('https://plus.google.com/hangouts/active')

    def start(self, onair=False):
        """ Start new hangout,
        """
        if not self.browser.current_url.startswith('https://plus.google.com/hangouts/active'):
            self.browser.get('https://plus.google.com/hangouts/active')
        self.browser.by_class('opd').click(timeout=0.5)
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
        # close the inviting popup - the button text and timeots is different
        self.click_cancel_button_if_there_is_one(
            timeout=30, text='Close')
        # setting hangout id property
        self.hangout_id = self.browser.current_url[
            len(BASE_HANGOUT_URL):].split('?', 1)[0]



    def connect(self, hangout_id):
        """
        Connect to an existing hangout
        """
        self.browser.get(BASE_HANGOUT_URL + hangout_id)
        # there may be a big delay before 'Join' button appears, so we need
        # to add longer timeout for this
        self.browser.by_text('Join', timeout=60).click(timeout=0.5)

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
        self.browser.by_id('signIn').click(timeout=0.5)

        # filling up opt
        if otp:
            self.browser.by_id('smsUserPin').send_keys(otp)
            self.browser.by_id('smsVerifyPin').click(timeout=0.5)

        # XXX: checking if log in was successful
        if not self.is_logged_in:
            raise LoginError('Wasn\'t able to login. Check if credentials are correct.')

        # # Saving cookies
        # with open(self.cookies_dump_path, "wb") as cookies_dump:
        #     pickle.dump(self.browser.get_cookies(), cookies_dump)

    def click_cancel_button_if_there_is_one(self, timeout=0.5, text='Cancel'):
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

    def navigate_to_devices_settings(self):
        self.click_menu_element('MQ', func='by_class')

    def open_mics_devices_list(self):
        self.navigate_to_devices_settings()
        # click on MC list to make it load list of all devices
        # self.browser.by_class('qd-pc-kg').click(timeout=0.5)
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

    def set_microphone_devices(self, name):
        # TODO: make sure that browser is on needed context
        self.get_microphone_devices(with_nodes=True)[name].click()
        # click save button
        self.click_on_devices_save_button()

    # def get_video_devices(self, with_nodes=False):
    #     raise
    #     # self.open_mics_devices_list()
    #     # TODO: add caching ??? do we need this? there is self.video_devices prop
    #     # get list of devices
    #     # import pdb; pdb.set_trace()
    #     # video_dev_xpath = '//div[@class="c-i c-i-Ed Hz"]/div/div[@class="c-k-t"]'
    #     # video_devices = {
    #     #     node.get_attribute('innerText'): node
    #     #     for node in self.browser.find_elements_by_xpath(video_dev_xpath)}
    #     # self.video_devices = list(video_devices.keys())
    #     # if with_nodes:
    #     #     return video_devices
    #     # return self.video_devices

    # def set_video_devices(self, name):
    #     # TODO: make sure that browser is on needed context
    #     self.get_video_devices(with_nodes=True)[name].click()
    #     self.click_on_devices_save_button()

    def _get_bandwidth_controooller(self):
        if not self.browser.xpath('//div[text()="Limit Bandwidth"]').is_displayed():
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
            ['']
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
        self.browser.silent = True
        self.leave_call()
        try:
            self.browser.quit()
        finally:
            if self.display is not None:
                self.display.stop()

    def click_menu_element(self, xpath, func='xpath'):
        self.click_cancel_button_if_there_is_one()
        menu_button = getattr(self.browser, func)(xpath)
        if not menu_button.is_displayed():
            # if menu buttons is hidden make them displayed
            self.browser.by_class('Za-Ja-m').click(timeout=0.5)
        menu_button.click(0.5)
