"""
API for Tollbox Hangout PlugIn
"""
from zope.component import provideUtility
from ..interfaces import IModule
from hangout_api.gadgets.utils import gadget_context_handler


class ToolBox(object):
    """
    Tollbox Hangout API
    """

    def __init__(self, base):
        self.base = base
        self.mirrored = False

    @gadget_context_handler('Hangout Toolbox')
    def lower_third(self, name, tags=None, logo=None, color=None):
        """
        Lower Third, allows to set name, tags, logo and color
        """

        self.base.browser.xpath(
            '//img[contains(@src, "lower_24.png")]').click(timeout=0.5)

        self.base.set_text('//input[@placeholder="Enter Display Name"]', name)

        if tags is not None:
            self.base.set_text('//input[@placeholder="Enter Tagline"]', tags)

        if logo:
            self.base.browser.xpath(
                '//button[@title="Choose Logo"]').parent.xpath(
                    '//input[@type="file"]').send_keys(logo)

        if color:
            self.base.browser.by_class(
                'color-picker-container').click(timeout=0.5)
            self.base.set_text(
                '//*[@class="goog-hsv-palette-sm-input"]', color)

    @gadget_context_handler('Hangout Toolbox')
    def lower_third_active(self, value=None):
        """
        Returns or sets lower third status
        """
        self.base.browser.xpath(
            '//img[contains(@src, "lower_24.png")]').click(timeout=0.5)
        active_button = self.base.browser.by_class('goog-switch-text')
        is_active = active_button.get_attribute('innerText') == 'ON'
        if value is None:
            return is_active
        if (not value and is_active) or (value and not is_active):
            active_button.click(timeout=0.5)

    # @gadget_context_handler('Hangout Toolbox')
    # def custom_overlay(self, image):
    #     """
    #     Sets custom overlay
    #     """
    #     raise NotImplemented(
    #         "Can't find a way to set image")
    #     self.base.browser.xpath(
    #         '//img[contains(@src, "lower_24.png")]').click(timeout=0.5)
    #     self.base.browser.by_text("Custom Upload").click(timeout=0.5)
    #     self.base.browser.execute_script(
    #         'return gapi.hangout.getParticipants()')

    # @gadget_context_handler('Hangout Toolbox')
    # def custom_overlay_active(self, value=None):
    #     """
    #     Returns or sets Custom Overlay status. Custom Overlay should be set
    #     """
    #     self.base.browser.xpath(
    #         '//img[contains(@src, "lower_24.png")]').click(timeout=0.5)
    #     active_button = self.base.browser.xpath(
    #         '//div[@class="custom-upload"]//*[@class="goog-switch-text"]')
    #     is_active = active_button.get_attribute('innerText') == 'ON'
    #     if value is None:
    #         return is_active
    #     if (not value and is_active) or (value and not is_active):
    #         active_button.click(timeout=0.5)

    def video_mirror_active(self, value=None):
        """
        Returns or sets Video Mirror status.
        """
        if value is None:
            return self.mirrored
        self.base.browser.execute_script(
            'gapi.hangout.av.setLocalParticipantVideoMirrored(%s);'
            % str(value).lower())
        self.mirrored = value


provideUtility(ToolBox, IModule, 'toolbox')
