#!/usr/bin/python3

import sys

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import logging
import socket
from remote_serial_server import Redirector
import serial

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.INFO)

DEFAULT_SOCKET_PORT     = 2217

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    try:
        # Setup argument parser
        parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-s", "--serial", dest="serial_port",  required=True, help="local Mirobot serial port")

        # Process arguments
        args = parser.parse_args()
        
        # connect to serial port
        ser = serial.serial_for_url(args.serial_port, baudrate=115200, stopbits=1, do_not_open=True)
        ser.timeout = 3     # required so that the reader thread can exit
        # reset control line as no _remote_ "terminal" has been connected yet
        ser.dtr = False
        ser.rts = False
    
        try:
            ser.open()
        except serial.SerialException as e:
            logger.error("Could not open serial port {}: {}".format(ser.name, e))
            sys.exit(1)
    
        logger.info("Serving serial port: {}".format(ser.name))
        settings = ser.get_settings()
    
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(('', DEFAULT_SOCKET_PORT))
        srv.listen(1)
        logger.info("TCP/IP port: {}".format(DEFAULT_SOCKET_PORT))
        while True:
            try:
                client_socket, addr = srv.accept()
                logger.info('Connected by {}:{}'.format(addr[0], addr[1]))
                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                ser.rts = True
                ser.dtr = True
                # enter network <-> serial loop
                r = Redirector(
                    ser,
                    client_socket,
                    True)
                try:
                    r.shortcircuit()
                finally:
                    logger.info('Disconnected')
                    r.stop()
                    client_socket.close()
                    ser.dtr = False
                    ser.rts = False
                    # Restore port settings (may have been changed by RFC 2217
                    # capable client)
                    ser.apply_settings(settings)
            except KeyboardInterrupt:
                sys.stdout.write('\n')
                break
            except socket.error as msg:
                logger.error(str(msg))

        return 0
    except KeyboardInterrupt:
        print("Handling KI")
        return 0


if __name__ == "__main__":
    main()