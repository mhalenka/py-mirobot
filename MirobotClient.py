from pymirobot.mirobot import Mirobot
from pymirobot.RemoteSerial import RemoteSerial


class MirobotClient(Mirobot):
    def __init__(self, host, port=2217, receive_callback=None, debug=False):
        super().__init__(receive_callback, debug)

        self.serial_device = RemoteSerial(host, port)

    def connect(self, receive_callback=None):
        if receive_callback is not None:
            self.receive_callback = receive_callback

        self.serial_device.open()
