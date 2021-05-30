#https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
# to trasnfer the file to the windows!
import locale

import socket
# import tqdm
import os
import base64

class File_server_windows:
    def __init__(self, ip, port):
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform

        self.image_folder = "alarm_images/default"
        self.continue_server = True
        # device's IP address
        self.SERVER_HOST = ip
        self.SERVER_PORT = port
        # receive 4096 bytes each time
        self.BUFFER_SIZE = 4096
        self.SEPARATOR = "#"

        # create the server socket
        # TCP socket
        self.s = socket.socket()
        # bind the socket to our local address
        self.s.bind((self.SERVER_HOST, self.SERVER_PORT))

        # enabling our server to accept connections
        # 5 here is the number of unaccepted connections that
        # the system will allow before refusing new connections
        self.s.listen(5)
        print(f"[*] Windows File Server Listening on {self.SERVER_HOST}:{self.SERVER_PORT}")

    def run_server(self):
        while self.continue_server:
            # accept connection if there is any
            client_socket, address = self.s.accept()
            # if below code is executed, that means the sender is connected
            print(f"[+] {address} is connected.")

            # receive the file infos
            # receive using client socket, not server socket
            try:
                # received = client_socket.recv(self.BUFFER_SIZE).decode().strip()
                received = client_socket.recv(47).decode().strip()
                # client_socket.
            except UnicodeDecodeError as e:
                print(e)
                continue
            print("received", received)
            filename, filesize,junk = received.split(self.SEPARATOR)
            print("filesize",filesize)
            print("filename",filename)
            # remove absolute path if there is
            filename = self.image_folder + "/" + os.path.basename(filename)
            # filename = os.path.basename(filename)
            # convert to integer
            filesize = int(filesize)

            # start receiving the file from the socket
            # and writing to the file stream
            # progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "wb") as f:
                while True:
                    # read 1024 bytes from the socket (receive)
                    bytes_read = client_socket.recv(self.BUFFER_SIZE)
                    if not bytes_read:
                        # nothing is received
                        # file transmitting is done
                        f.close()
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
        self.s.close()


if __name__ == "__main__":
    # file_server = File_server_windows("images")
    file_server = File_server_windows("127.0.0.1", 5001)
    file_server.run_server()