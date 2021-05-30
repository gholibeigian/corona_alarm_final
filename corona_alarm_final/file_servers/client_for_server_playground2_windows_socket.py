# take a look at the source file to find the better version
# it works with server_playground.py
import socket
import sys
import os
from datetime import datetime
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 2400)
print('CLIENT:     connecting to port ', server_address)
sock.connect(server_address)

try:
    # Send data
    # Uncomment this line to send the alarm to the raspnerry pi
    #datetime.datetime.strftime(selected_date_time, "cam_%Y_%m_%d_T_%I_%M_%S__%f")
    message = 'lep_2021_03_04_T_11_17_09__597.png#0.100'.encode("utf-8").strip()
    print('CLIENT:     sending "%s"', message)
    sock.sendall(message)
    # Look for the response
    # amount_received = 0
    # amount_expected = len(message)

    # while amount_received < amount_expected:
    #     data = sock.recv(16)
    #     amount_received += len(data)
    #     print(sys.stderr, 'CLIENT:     received ',data)

finally:
    print('CLIENT:     closing socket')
    sock.close()