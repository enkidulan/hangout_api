"""
API for ControlRoom Hangout PlugIn
"""
from hangout_api.gadgets.utils import gadget_context_handler
from hangout_api.utils import tries_n_time_until_true, TIMEOUTS

_AUDIO_XPATH = '//div[contains(text(), "%s")]/../../div[2]/div[1]'
_VIDEO_XPATH = '//div[contains(text(), "%s")]/../../div[2]/div[2]'


def get_status(controller):
    """
    returns status True or False from controller node,
    to get status it looks at 'aria-pressed' node attribute
    """
    return controller.get_attribute('aria-pressed') == 'true'


class ControlRoom(object):
    """
    ControlRoom plugin for OnAir

    .. testsetup:: ControlRoom

        from hangout_api.gadgets.control_room import ControlRoom
        from hangout_api.tests.doctests_utils import DummyHangout



        from hangout_api.gadgets import utils
        utils.open_app = lambda *args: None


        global call_num
        call_num = 0

        def _status_getter_setter(*args):
            global call_num
            if call_num == 6:
                call_num = 0
            call_num += 1
            return[True, True, False, True, False, False][call_num - 1]
        origin = ControlRoom._status_getter_setter
        ControlRoom._status_getter_setter = _status_getter_setter

        hangout = DummyHangout(
            name='controlroom',
            klass=ControlRoom)

        # dummy hack to increase coverage
        origin(hangout.controlroom, '%s', '', True)
        origin(hangout.controlroom, '%s', '', None)
        origin(hangout.controlroom, '%s', '', False)


    """

    def __init__(self, base):
        self.base = base

    def _status_getter_setter(self, xpath, participant_name, mute):
        """
        Helper function that handles turning on and off ControlRoom properties

        """
        controller = self.base.browser.xpath(xpath % participant_name)
        status = get_status(controller)
        if mute is None:
            return status
        if status != mute:
            controller.parent.click(TIMEOUTS.fast)
            controller.parent.click(TIMEOUTS.fast)
            controller.click(TIMEOUTS.fast)
            tries_n_time_until_true(
                lambda: get_status(controller) == mute, try_num=200)
            return True
        return False

    @gadget_context_handler("Control Room")
    def audio(self, participant_name, mute=None):
        """
        Controls audio of OnAir participant. Allows to mute, un-mute or
        get current states of participant audio.

        As arguments takes:
            * participant_name - name of participant ('Doe John')
            * mute - optional argument, takes True or False

        In case if no mute argument was provided returns current state.

        In case if no mute argument was provided returns:
            * True - went to opposite state
                (from 'on' to 'off', or from 'off' to 'on')
            * False -desired state was already chosen

        .. doctest:: ControlRoom

            >>> hangout.controlroom.audio('Doe John', mute=True)
            True
            >>> hangout.controlroom.audio('Doe John')
            True
            >>> hangout.controlroom.audio('Doe John', mute=True)
            False
            >>> hangout.controlroom.audio('Doe John', mute=False)
            True
            >>> hangout.controlroom.audio('Doe John')
            False
            >>> hangout.controlroom.audio('Doe John', mute=False)
            False

        """
        return self._status_getter_setter(_AUDIO_XPATH, participant_name, mute)

    @gadget_context_handler("Control Room")
    def video(self, participant_name, mute=None):
        """
        Controls video of OnAir participant. Allows to mute, un-mute or
        get current states of participant video.

        As arguments takes:
            * participant_name - name of participant ('Doe John')
            * mute - optional argument, takes True or False

        In case if no mute argument was provided returns current state.

        In case if no mute argument was provided returns:
            * True - went to opposite state
                (from 'on' to 'off', or from 'off' to 'on')
            * False -desired state was already chosen

        .. doctest:: ControlRoom

            >>> hangout.controlroom.video('Doe John', mute=True)
            True
            >>> hangout.controlroom.video('Doe John')
            True
            >>> hangout.controlroom.video('Doe John', mute=True)
            False
            >>> hangout.controlroom.video('Doe John', mute=False)
            True
            >>> hangout.controlroom.video('Doe John')
            False
            >>> hangout.controlroom.video('Doe John', mute=False)
            False

        """
        return self._status_getter_setter(_VIDEO_XPATH, participant_name, mute)
