#https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
import socket
# import tqdm
import os
import base64
# device's IP address
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "#"

# create the server socket
# TCP socket
s = socket.socket()
# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))

# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")


while True:
    # accept connection if there is any
    client_socket, address = s.accept()
    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")

    # receive the file infos
    # receive using client socket, not server socket
    try:
        received = client_socket.recv(BUFFER_SIZE).decode().strip()
    except UnicodeDecodeError:
        continue
    filename, filesize = received.split(SEPARATOR)
    print(filename)
    # remove absolute path if there is
    filename = 'new_' + os.path.basename(filename)
    # convert to integer
    filesize = int(filesize)

    # start receiving the file from the socket
    # and writing to the file stream
    # progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            # bytes_read = bytes_read.rstrip("\n").decode("utf-16")

            f.write(bytes_read)
            # f.write(base64.b64decode(bytes_read))
            # update the progress bar
            # progress.update(len(bytes_read))

    # close the client socket
    client_socket.close()
# close the server socket
s.close()