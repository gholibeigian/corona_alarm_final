import locale

import socket
import payload_generator_server
import html_email_generator
import db_navigator_alarm

class Email_server:
    def __init__(self, ip, port):# TODO: set ip and port from the constructor
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform

        # create a socket object
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # to stop the service
        self.continue_server = True
        # get local machine name
        host = ip#socket.gethostname()
        port = port
        # bind to the port
        self.serversocket.bind((host, port))
        # queue up to 5 requests
        self.serversocket.listen(5)
        print("[*] Email server is running on: ",host, " port: ", port)
    def run_listen(self):
        while self.continue_server:
            # establish a connection
            clientsocket, addr = self.serversocket.accept()
            print("Got a connection from %s" % str(addr))
            rcv_msg = clientsocket.recv(50)
            print(rcv_msg)
            rcv_msg_payload = rcv_msg.decode('ascii').split("#")
            # if rcv_msg_payload[0] == "email":
            # altitude, longitude = rcv_msg.decode('ascii').split(",")
            # current_coordinate = (altitude, longitude)
            my_Payload_generator_server = payload_generator_server.Payload_generator_server(map,
                                                                                            "polygon_geojason/yellow.geojson",
                                                                                            "../corona_alarm_final/polygon_geojason/red.geojason")
            altitude, longitude = db_navigator_alarm.Database_navigator().load_last_coordinate()# get the coordinate from the table

            my_Payload_generator_server.set_run_coordinates(float(altitude), float(longitude),
                                                            100)  # altitude, longitude, distance=100
            # altitude, longitude = db_navigator_alarm.Database_navigator().load_last_coordinate()
            print("Email sent to the client!")
            email_to_send = html_email_generator.Html_email_generator(100, my_Payload_generator_server.distance_measurer.distance_datetime)
            email_to_send.send_email('gholibeigian.k85@htlwienwest.at',rcv_msg_payload[0], "Info: Sick people closeer than 100m from you!")
            # msg = "Email sent successfully!"
            # msg = str(msg)
            # clientsocket.send(msg.encode('ascii'))
            clientsocket.close()

if __name__ == "__main__":
    # gps_server = Server_gps("127.0.0.1", 7897)
    # gps_server.run_listen()
    # to test with the localhost!
    gps_server = Email_server("127.0.0.1", 7897)
    gps_server.run_listen()

    # to comminucate to raspberry pi!
    # gps_server = Server_gps("192.168.1.102", 24015)
    # gps_server.run_listen()
