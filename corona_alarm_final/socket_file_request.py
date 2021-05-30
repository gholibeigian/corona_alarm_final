## IMPORTANT: CHANGE THE IP FROM LOCAL IP!!!
import locale

import socket
import sys
import os
from datetime import datetime
class Socket_file_request:
    def __init__(self, selected_date_time_filename, seconds):
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # raspberry pi addres
        self.server_address = ('localhost', 2400)
        self.selected_date_time = selected_date_time_filename.split("/")[1]
        self.seconds = seconds
        print(self.selected_date_time)

    def send_socket(self):
        # Connect the socket to the port where the server is listening
        print('CLIENT:     connecting to port ', self.server_address)
        try:
            self.sock.connect(self.server_address)

            # Send data
            # Uncomment this line to send the alarm to the raspnerry pi
            #datetime.datetime.strftime(selected_date_time, "cam_%Y_%m_%d_T_%I_%M_%S__%f")
            message = (self.selected_date_time + '#' + self.seconds).encode("utf-8").strip()
            print('CLIENT:     sending "%s"', message)
            self.sock.sendall(message)
        except ConnectionRefusedError:
            pass
        finally:
            print('CLIENT:     closing socket')
            self.sock.close()