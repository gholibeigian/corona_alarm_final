#it works with project learn_server2.client
# it takes msgFromClient = "187-184.312-530.22-501-lep_2021_03_04_T_11_17_07__893.png"
#TODO chage the udp socket on raspberry -> remove altitude and longitude from tne massage

import locale
import socket
import threading
import time
from datetime import datetime
import socket_file_request
from tkinter import *
from dateutil import parser
# from pathlib import Path
# from dateutil import parser
import os
import file_server
import corona_alarm





class Alarm_server:
    def __init__(self, localIP, port_alarm, port_file_server, window):
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform
        print(locale.getlocale(locale.LC_TIME))
        # self.window = window
        self.continue_server = True
        self.alarm_time_label_list = []
        self.init_server(localIP, port_alarm, port_file_server)
        # self.listen()
        self.alarm_server_thread = threading.Thread(target=self.listen)
        self.alarm_server_thread.setDaemon(True)
        self.alarm_server_thread.start()
        # self.init_gui(window)

        # Ask prof. Kerer! Is it ok?
        # self.t2 = threading.Thread(target=self.init_gui, args=(window,))
        # self.t2.start()
        self.master_window = window
        self.init_gui()
    def init_gui(self):
        self.window = Toplevel(master=self.master_window,background='#3c3f41')
        # scrollbar
        self.scrollbar = Scrollbar(self.window, orient=VERTICAL)
        self.scrollbar.grid(row=3, column=0, sticky=N + S + E)
        # self.top = Toplevel()
        #Colors(https://color.adobe.com/trends/Travel):
        self.lila = '#3c3f41'
        self.blue_gray= '#3E434C'
        self.blue = '#4B6EAF'
        self.mylist = Listbox(self.window, yscrollcommand=self.scrollbar.set, width=25)
        self.mylist.grid(row=3, column=0)
        # bind self.scrollbar with the listbox
        self.scrollbar.config(command=self.mylist.yview)

        # self.window.title("Corona Alarm")
        self.window.config(padx=100, pady=150)

        self.load_list()
        # self.reload_list()
        self.mylist.bind("<<ListboxSelect>>", self.callback)
        # Buttons
        self.download_alarm_button = Button(self.window,text="Load Alarm", command=self.load_corona_alarm_gui)
        self.download_alarm_button.grid(row=4, column=0)
        # do not exit! disable x window
        self.window.protocol('WM_DELETE_WINDOW', self.donothing)
        # self.window.withdraw()
        # self.window.mainloop()
    # do not exit! disable x window
    def donothing(self):
        pass
    # load the disctionary as fresh
    def load_corona_alarm_gui(self):
        print(1)# todo : exception handling when the user does not select a valus!
        print("selected item: " + self.mylist.selection_get())
        selected_item_png_format = datetime.strftime(parser.parse(self.mylist.selection_get()),  "lep_%Y_%m_%d_T_%H_%M_%S__%f")+'.png'
        selected_item_png_format = selected_item_png_format.split("__")[0] + "__" +selected_item_png_format.split("__")[1][:3]+ "."  +selected_item_png_format.split(".")[1]
        print("selected pattern: " + selected_item_png_format)
        # create a directory
        directory = "alarm_images/" + selected_item_png_format
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.new_file_server.image_folder = directory
        # file_server = File_server_windows()

        # time.sleep(3)

        # new_file_server.run_server()
        # Path("/my/directory").mkdir(parents=True, exist_ok=True)
        # todo: use these 2 lines # send socket request for the file server
        request_files_after_alarm = socket_file_request.Socket_file_request("alarm/" + selected_item_png_format,
                                                                            "3.00")
        request_files_after_alarm.send_socket()
        time.sleep(3)
        # self.t3 = threading.Thread(target=self.call_corona_alarm(directory,selected_item_png_format))
        # self.t3.start()
        self.call_corona_alarm(directory, selected_item_png_format)


    def call_corona_alarm(self, directory,selected_item_png_format):
        for i in self.alarm_time_label_list:
            if i[0] == selected_item_png_format:
                # todo : I made it a thread! ask Kerer!
                corona_alarm_new_gui = corona_alarm.Corona_alarm(directory, i[1], self.window)

    def load_list(self):
        self.alarm_time_label_list = []

    def reload_list(self):
        list_items = self.mylist.get(0, END)
        # my_list = ["leps12123.png","dsifads.lep"]
        # print(list_items)
        for k in self.alarm_time_label_list:
            # print(type(k))
            str_key = str(k)
            thermal_convert_date_for_pyImage = datetime.strptime(str(k[0]), 'lep_%Y_%m_%d_T_%H_%M_%S__%f.png')
            thermal_convert_date_for_pyImage = self.format_time(thermal_convert_date_for_pyImage)
            if str(thermal_convert_date_for_pyImage) not in list_items:
                print(k, " is not in the list!")
                self.mylist.insert(END, str(thermal_convert_date_for_pyImage))
        # for k in self.alarm_time_label_list:
        #     thermal_convert_date_for_pyImage = datetime.strptime(str(new_imcoming_alarm[0]), 'lep_%Y_%m_%d_T_%H_%M_%S__%f.png')


    #load the callback from the list
    def callback(self,event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            convert_date = parser.parse(data)
            print("convert_date" , convert_date)
        else:
            pass
            print("error")


    def init_server(self, localIP, port_alarm, port_file_server):
        self.localIP =  localIP
        self.localPort = port_alarm
        self.bufferSize = 1024
        msgFromServer = "Hello UDP Client"
        bytesToSend = str.encode(msgFromServer)
        # Create a datagram socket
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Bind to address and ip
        self.UDPServerSocket.bind((localIP, port_alarm))
        print("[*] UDP Alarm server up on IP:" + self.localIP + " and listening on port: " + str(self.localPort))
        self.new_file_server = file_server.File_server_windows(localIP,port_file_server)
        self.file_server_thread = threading.Thread(target=self.new_file_server.run_server)
        # alarm_server_thread
        self.file_server_thread.setDaemon(True)
        self.file_server_thread.start()


    def listen(self):
        # Listen for incoming datagrams
        while (self.continue_server):
            bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            clientMsg = "Message from Client:{}".format(message)
            clientIP = "Client IP Address:{}".format(address)
            data = message.decode("utf-8")
            print('DATA:   received ', data)
            raw_data = data.split("-")
            print(raw_data)
            max_red = raw_data[0]
            avgRedMinValue = raw_data[1]
            avgRedMaxValue = raw_data[2]
            hightRedCount = raw_data[3]
            date_time_data = raw_data[4]
            # receive data(alarm) here and load the gui!
            # TODO. work on it
            alarm_date_time = datetime.strptime(date_time_data, 'lep_%Y_%m_%d_T_%H_%M_%S__%f.png')
            # currect format:
            # print(self.format_time(alarm_date_time))
            # alarm_date_time_formated = self.format_time(alarm_date_time)

            # alarm_date_time.microsecond / 1000
            # lep_2021_04_12_T_17_29_01__336.png
            print(alarm_date_time)
            # sleep for 3 seconds
            print(alarm_date_time)
            # send the soncket request for 3 second
            # request_files_after_alarm = socket_file_request.Socket_file_request("alarm/" + alarm_date_time,3.00)
            # TypeError: can only concatenate str (not "float") to str
            alarm_label = "New Alarm From Corona Alarm Kit\nmaxRed: {}\nAverage Min Value: {}\nAverage Max Value: {}\nCount of Hightest pixels: {}\nDate Time:{}\nAltitude: 48.20302872428539\nLaltitude: 16.36892920432462".format(max_red,avgRedMinValue,avgRedMaxValue,hightRedCount,alarm_date_time)
            self.alarm_time_label_list.append((date_time_data, alarm_label))
            # time.sleep(15)
            # new_corona_alarm = corona_alarm.Corona_alarm("images", alarm_label)
            print(clientMsg)
            print(clientIP)
            # Apply here:
            # UDPServerSocket.sendto(bytesToSend, address)

            # reload the list with the new data from  the socket
            self.reload_list()

    def format_time(self, time_obj):
        t = time_obj
        s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
        head = s[:-7]  # everything up to the '.'
        tail = s[-7:]  # the '.' and the 6 digits after it
        f = float(tail)
        temp = "{:.03f}".format(f)  # for Python 2.x: temp = "%.3f" % f
        new_tail = temp[1:]  # temp[0] is always '0'; get rid of it
        return head + new_tail
if __name__ == "__main__":
    win = Tk("test")
    alarm_server = Alarm_server("127.0.0.1", 20001,win)
    # alarm_server.listen()


    # my_top = Alarm_server()
    win.mainloop()

