from pymirobot.mirobot import Mirobot
from pymirobot.RemoteSerial import RemoteSerial
from time import time, sleep
from pymirobot.ArmState import ArmState


class MirobotClient(Mirobot):
    def __init__(self, host, port=2217, receive_callback=None, debug=False):
        super().__init__(receive_callback, debug)

        self.serial_device = RemoteSerial(host, port)

    def connect(self, receive_callback=None):
        if receive_callback is not None:
            self.receive_callback = receive_callback

        self.serial_device.open()
        self.serial_device.telnet.read_until(
            bytes("Using reset pos!", "utf-8"), timeout=3
        )
        # Sometimes gets sent twice?
        self.serial_device.telnet.read_until(
            bytes("Using reset pos!", "utf-8"), timeout=1
        )

    def home_simultaneous(self):
        msg = "$H"
        self.send_msg(msg)
        self.serial_device.telnet.read_until(bytes("ok", "utf-8"), timeout=20)

        # If sending a command while returning to zero, coordinates get messed up
        # Poll for idle
        start = time()
        while time() - start < 10 and not self.is_idle():
            sleep(0.5)

    def get_arm_state(self):
        status = self._get_status_string()

        if status:
            state = ArmState.from_status_string(status)

            return state

        else:
            return None

    def is_idle(self):
        state = self.get_arm_state()

        if state:
            return not state.active

        else:
            return False

    def _get_status_string(self):
        self.send_msg("?")

        result = self.serial_device.telnet.read_until(
            bytes(">", "utf-8"), timeout=1
        ).decode("utf-8")

        start = result.find("<")

        if start >= 0:
            result = result[start:]

        if ">" in result:
            return result
        else:
            return None
