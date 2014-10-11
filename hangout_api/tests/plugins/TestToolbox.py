import os.path
import unittest
from testfixtures import compare


TESTS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_NAME = 'sample_image_for_testing.jpg'
IMAGE_PATH = os.path.join(TESTS_PATH, 'resources', IMAGE_NAME)


class TestToolboxApp(unittest.TestCase):

    @classmethod
    def setup_class(self):
        from hangout_api.tests import HANGOUT
        self.hangout = HANGOUT

    def _input_value_getter(self, xpath):
        return self.hangout.browser.xpath(xpath).get_attribute('value')

    def test_lower_third_settings(self):
        inputed_data = dict(
            name="J.R. Dou",
            tags="hangout api bot",
            logo=IMAGE_PATH,
            color="#001122")
        self.hangout.toolbox.lower_third(**inputed_data)
        readed_data = dict(
            name=self._input_value_getter(
                '//input[@placeholder="Enter Display Name"]'),
            tags=self._input_value_getter(
                '//input[@placeholder="Enter Tagline"]'),
            logo=self.hangout.browser.xpath(
                '//button[@title="Choose Logo"]').parent.xpath(
                    '//input[@type="file"]').get_attribute('value'),
            color=self._input_value_getter(
                '//*[@class="goog-hsv-palette-sm-input"]'))
        inputed_data['logo'] = 'C:\\fakepath\\' + IMAGE_NAME
        compare(inputed_data, readed_data)

    def test_lower_third_active(self):
        self.hangout.toolbox.lower_third_active(True)
        compare(self.hangout.toolbox.lower_third_active(), True)

        self.hangout.toolbox.lower_third_active(False)
        compare(self.hangout.toolbox.lower_third_active(), False)
        self.hangout.toolbox.lower_third_active(False)
        compare(self.hangout.toolbox.lower_third_active(), False)
        self.hangout.toolbox.lower_third_active(True)
        compare(self.hangout.toolbox.lower_third_active(), True)
        self.hangout.toolbox.lower_third_active(True)
        compare(self.hangout.toolbox.lower_third_active(), True)

    # def test_custom_overlay(self):
    #     self.hangout.toolbox.custom_overlay(image=IMAGE_PATH)

    # def test_custom_overlay_active(self):
    #     self.hangout.toolbox.custom_overlay(image=IMAGE_PATH)
    #     self.hangout.toolbox.custom_overlay_active(True)
    #     compare(self.hangout.toolbox.custom_overlay_active(), True)

    #     self.hangout.toolbox.custom_overlay_active(False)
    #     compare(self.hangout.toolbox.custom_overlay_active(), False)
    #     self.hangout.toolbox.custom_overlay_active(False)
    #     compare(self.hangout.toolbox.custom_overlay_active(), False)
    #     self.hangout.toolbox.custom_overlay_active(True)
    #     compare(self.hangout.toolbox.custom_overlay_active(), True)
    #     self.hangout.toolbox.custom_overlay_active(True)
    #     compare(self.hangout.toolbox.custom_overlay_active(), True)

    def test_video_mirror_active(self):
        self.hangout.toolbox.video_mirror_active(True)
        compare(self.hangout.toolbox.video_mirror_active(), True)

        self.hangout.toolbox.video_mirror_active(False)
        compare(self.hangout.toolbox.video_mirror_active(), False)
        self.hangout.toolbox.video_mirror_active(True)
        compare(self.hangout.toolbox.video_mirror_active(), True)
