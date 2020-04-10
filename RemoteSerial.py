from telnetlib import Telnet


class RemoteSerial:
    
    def __init__(self, host, port=2217):
        self.host = host
        self.port = port
        
        self.is_open = False
                
        self.telnet = Telnet()
    
    def open(self):
        self.telnet.open(self.host, self.port)
        
        self.telnet.read_until(bytes("Using reset pos!", "utf-8"), timeout=3)
        
        self.is_open = True
        
    def close(self):
        self.telnet.close()
        self.is_open = False
        
    def send(self, msg, terminator = ""):
        byte_msg = (msg + terminator).encode('UTF-8')
        self.telnet.write(byte_msg)
        