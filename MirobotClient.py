from pymirobot.mirobot import Mirobot
from pymirobot.RemoteSerial import RemoteSerial
from time import sleep


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
        self.serial_device.telnet.read_until(
            bytes("ok", "utf-8"), timeout=20
        )
        # If sending a command while returning to zero, coordinates get messed up
        sleep(5)