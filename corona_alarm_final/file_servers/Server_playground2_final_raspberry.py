# read the alarm datetime and send the needed data
# it works with client_for_server_playground.py
import os
from datetime import datetime
import socket
# import tqdm
import base64
# host = "192.168.1.103"
host = "127.0.0.1"

port_file = 5001

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

# the ip address or hostname of the server, the receiver
port_listen = 2400

my_list = os.listdir("images")


# intialize the dictionaries for thermal and pycam photos
def init_Image_dictionaries():
    time_thermal_file_name_dic = {}
    time_pycamera_file_name_dic = {}
    for file in my_list:
        if file.endswith('png'):
            if file.startswith("lep_"):
                datetime_object = datetime.strptime(file,
                                                    'lep_%Y_%m_%d_T_%H_%M_%S__%f.png')  # 2021_02_08_T_20_54_23__669
                time_thermal_file_name_dic[datetime_object] = file
            # print(time_thermal_file_name_dic)
            # print(file)
            # print(datetime_object)
        if file.startswith('cam_'):
            datetime_object = datetime.strptime(file, 'cam_%Y_%m_%d_T_%H_%M_%S__%f.jpg')
            time_pycamera_file_name_dic[datetime_object] = file
    return time_thermal_file_name_dic, time_pycamera_file_name_dic
    # print(datetime_object)



# Create a datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to address and ip
sock.bind((host, port_listen))

print("TCP server up and listening on ",host,":",port_listen)
sock.listen(5)
while True:
    # Wait for a connection
    connection, client_address = sock.accept()
    try:
        print('SERVER:   connection from', client_address)
        # Receive the data in small chunks and retransmit it
        while True:
            
            data = connection.recv(512)
            if data:
                print('DATA->', data)
                ####This part is to identify the files and to send them
                #   This file takes a alarm_date_time and time_difference and find the close images(Key) and print it in the console!
                #   just send files_to_send_dictionary to the server!

                # alarm_date_time = datetime(2021, 3, 4, 11, 17, 7, 530000) # sample datetime
                # convert datetime into string
                # datetime.datetime.strftime(st, "cam_%Y_%m_%d_T_%I_%M_%S__%f")

                # convert into datetime
                data = data.decode("utf-8")
                data_striped = data
                alarm_data_time_striped = data_striped.split("#")[0]
                time_difference = float(data_striped.split("#")[1])

                alarm_date_time = datetime.strptime(alarm_data_time_striped, 'lep_%Y_%m_%d_T_%H_%M_%S__%f.png')
                print(alarm_date_time)
                # time from the windows server!
                files_to_send_dictionary = []


                time_thermal_file_name_dic, time_pycamera_file_name_dic = init_Image_dictionaries()
                # print(time_thermal_file_name_dic)
                # print(time_pycamera_file_name_dic)

                # Alarm time from the raspberry

                for thermal_key, file_name in time_thermal_file_name_dic.items():
                    min_difference = abs((thermal_key - alarm_date_time).total_seconds())
                    if min_difference < time_difference:
                        # print(min_difference)
                        # print(type(min_difference))
                        files_to_send_dictionary.append(file_name)

                for pycamera_key, file_name in time_pycamera_file_name_dic.items():
                    min_difference = abs((pycamera_key - alarm_date_time).total_seconds())
                    if min_difference < time_difference:
                        # print(min_difference)
                        # print(type(min_difference))
                        files_to_send_dictionary.append(file_name)

                print(files_to_send_dictionary)  # just send files_to_send_dictionary to the server!
                print(len(files_to_send_dictionary))
                ### Send files to the server!

                for file in files_to_send_dictionary:
                    s = socket.socket()
                    # get the file size
                    #images/lep_2021_03_04_T_11_17_09__010.png
                    filesize = os.path.getsize("images/"+file)
                    print(f"[+] Connecting to {host}:{port_file}")
                    print(client_address[0])
                    s.connect((client_address[0], port_file))
                    print("[+] Connected.")

                    # send the filename and filesize
                    SEPARATOR = '#'
                    s.send(f"{file}{SEPARATOR}{filesize}".encode().strip())
                    file = "images/"+file

                    # start sending the file

                    # for beautifulness!
                    # progress = tqdm.tqdm(range(filesize), f"Sending {file}", unit="B", unit_scale=True,
                    #                      unit_divisor=1024)
                    with open(file, "rb") as f:
                        while True:
                            # read the bytes from the file
                            bytes_read = f.read(BUFFER_SIZE)
                            if not bytes_read:
                                # file transmitting is done
                                break
                            # we use sendall to assure transimission in
                            # busy networks

                            # bytes_read = bytes_read.rstrip("\n").decode("utf-16")
                            # s.sendall(bytes_read)
                            # s.sendall(base64.b64encode(bytes_read))
                            # update the progress bar
                            # progress.update(len(bytes_read))
                            s.sendall(bytes_read)

                    # close the socket
                    s.close()
                break

            #### Until here!
            # if data:
            #     # print('sending data back to the client')
            #     # connection.sendall(data)
            # else:
            #     # print('SERVER:   no more data from', client_address)
            #     break

    finally:
        print("New request from windows server!")
        pass
        # Clean up the connection
        #connection.close()
