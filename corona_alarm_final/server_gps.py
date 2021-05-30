import locale

import socket
import payload_generator_server

class Server_gps:
    def __init__(self, ip, port, distance):# TODO: set ip and port from the constructor
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform

        self.distance = distance
        # create a socket object
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.continue_server = True
        # get local machine name
        host = ip#socket.gethostname()
        port = port#9999
        # bind to the port
        self.serversocket.bind((host, port))
        # queue up to 5 requests
        self.serversocket.listen(5)
        print("[*] GPS server is running on: ",host, " port: ", port)
    def run_listen(self):
        while self.continue_server:
            # establish a connection
            clientsocket, addr = self.serversocket.accept()
            print("Got a connection from %s" % str(addr))
            rcv_msg = clientsocket.recv(1024)
            print(rcv_msg)
            altitude, longitude = rcv_msg.decode('ascii').split(",")
            current_coordinate = (altitude, longitude)
            my_Payload_generator_server = payload_generator_server.Payload_generator_server(map,
                                                                                            "polygon_geojason/yellow.geojson",
                                                                                            "../corona_alarm_final/polygon_geojason/red.geojason")
            my_Payload_generator_server.set_run_coordinates(float(altitude), float(longitude),
                                                            self.distance)  # altitude, longitude, distance=100
            msg = my_Payload_generator_server.get_payload()
            msg = str(msg)
            clientsocket.send(msg.encode('ascii'))
            clientsocket.close()
        print("[*] GPS server is shutting down!")

if __name__ == "__main__":
    gps_server = Server_gps("127.0.0.1", 9999,1000)
    gps_server.run_listen()