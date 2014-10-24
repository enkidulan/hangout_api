import random


class DummySelenium():
    silent = False
    current_url = \
        'https://plus.google.com/hangouts/_/gs4pp6g62w65moctfqsvihzq2qa'
    window_handles = [1, 3]
    location = 'http://xxx'

    def __init__(*args, **kargs):
        return

    def quit(self):
        return

    def get(*args, **kargs):
        return

    def switch_to_window(*args, **kargs):
        return

    def by_class(self, _, eager=False, **kwargs):
        if eager:
            return [DummySelenium(), ] * 5
        return DummySelenium()

    def by_id(self, _, eager=False, **kwargs):
        return self.by_class(_, eager, **kwargs)

    def xpath(self, _, eager=False, **kwargs):
        return self.by_class(_, eager, **kwargs)

    def by_text(self, _, eager=False, **kwargs):
        return self.by_class(_, eager, **kwargs)

    def click(*args, **kargs):
        return

    def set_text(*args, **kargs):
        return

    def send_keys(*args, **kargs):
        return

    def get_attribute(*args):
        return 1

    def is_displayed(*args):
        return random.choice([True, False])

    @property
    def parent(self):
        return DummySelenium()

    def switch_to_default_content(*args):
        return

    def switch_to_frame(*args):
        return

    def execute_script(*args):
        return


class DummyBase():
    browser = DummySelenium()

    def set_text(*args):
        return

    def click_cancel_button_if_there_is_one(*args, **kargs):
        return

    def click_menu_element(*args, **kargs):
        return


class DummyHangout():
    def __init__(self, name, klass, getter=None, setter=None, current=None):
        setattr(self, name, klass(DummyBase()))
        self.getter = getter
        self.setter = setter
        self.current = current
        getattr(self, name)._devices_getter = self._devices_getter
        getattr(self, name)._device_setter = self._device_setter
        getattr(self, name)._current_device_getter = \
            self._current_device_getter

    def _devices_getter(self, *args):
        return self.getter

    def _device_setter(self, *args):
        return self.setter

    def _current_device_getter(self, *args, **kwargs):
        return self.current
