from zope.component import provideUtility
from .interfaces import IModule
from time import sleep


class ToolBox():

    def __init__(self, base):
        self.base = base

    def set_text(self, node, text):
        if isinstance(node, str):
            node = self.base.browser.xpath(node)
        node.clear()
        node.send_keys(text)

    def open_toolbox_app(self):
        self.base.browser.by_class('Za-Ja-m').click(timeout=0.5)
        self.base.browser.xpath('//div[@aria-label="Hangout Toolbox"]').click(timeout=0.5)
        sleep(2)  # XXX
        self.base.browser.switch_to_frame('__gadget_0')
        self.base.browser.by_class('header-text').get_attribute('innerText')

    def lower_third(self, name, tags="", logo=None, color=None):
        # import pdb; pdb.set_trace()

        self.open_toolbox_app()

        self.base.browser.xpath('//img[contains(@src, "lower_24.png")]').click(timeout=0.5)

        self.set_text('//input[@placeholder="Enter Display Name"]', name)
        self.set_text('//input[@placeholder="Enter Tagline"]', tags)

        logo = '/home/enkidulan/Downloads/qqq.jpg'
        self.set_text(
            self.base.browser.xpath(
                '//button[@title="Choose Logo"]').parent.xpath(
                    '//input[@type="file"]'),
            logo)

        # collor = 'title="Pick Color"'
        self.base.browser.by_text('Save').click(timeout=0.5)

    def lower_third_active(self, value=None):
        active_button = self.base.browser.by_class(
            'goog-switch-text')
        is_active = active_button.get_attribute('innerText') == 'ON'
        if value is None:
            return is_active
        # if value or is_active:
        if (not value and is_active) or (value and not is_active):
            active_button.click(timeout=0.5)

    # def display_clock_active(self):
    #     pass

    def custom_overlay(self):
        raise

    def video_mirror_active(self):
        raise

provideUtility(ToolBox, IModule, 'toolbox')
