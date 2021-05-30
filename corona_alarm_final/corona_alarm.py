import locale
    ## IMPORTANT: CHANGE THE IP FROM LOCAL IP!!!
# import socket
# from tkinter import messagebox, Label,Button,Listbox,filedialog
# # from tkinter import filedialog
# from tkinter import  Spinbox, Scrollbar,VERTICAL,N,S,E,Tk,END
# import numpy as np
# import socket_file_request
# import cv2
# from PIL import ImageTk, Image
# import matplotlib.pyplot as plt
# import measure_temperature_top
# import template_matching_top
# import template_matching_top
import time
from tkinter import *
from tkcalendar import *
from tkinter import messagebox
import db_navigator_alarm
import cv2
from PIL import ImageTk, Image, UnidentifiedImageError
import measure_temperature_top
import socket_file_request
import person_db_gui


#import thermal and picamera images and initilize the "time_thermal_file_name_dic"
#and time_pycamera_file_name_dic
from dateutil import parser
import os
from datetime import datetime
import cv2

class Corona_alarm:
    def __init__(self,image_folder, alarm_label, master_window):
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform
        # locale.getlocale(locale.LC_TIME)
        # for face recognition we need a variable:
        self.identified_face_recognition_id  = -1
        #Colors(https://color.adobe.com/trends/Travel):
        lila = '#3c3f41'
        blue_gray= '#3E434C'
        blue = '#4B6EAF'
        monitor_width = master_window.winfo_screenwidth()
        monitor_height = master_window.winfo_screenheight()
        self.thermal_image_size = (monitor_width//2,monitor_height//2)
        self.image_folder = image_folder  # "images"
        # self.image_folder = "images"

        self.init_time_thermal_pycamera_dic()
        # initialize the GUI
        self.window = Toplevel(master_window)
        self.window.lift()

        self.window.title("Template Matching")
        self.window.config( bg=lila)
        # self.window.geometry('1200x400')
        # self.window.setgeo

        try:
            # print("images/" + self.time_thermal_file_name_dic[next(iter(self.time_thermal_file_name_dic))])
            self.selected_file_name = self.time_thermal_file_name_dic[next(iter(self.time_thermal_file_name_dic))]
            # self.selected_file_date = "images/" + self.selected_file_name
            self.selected_file_date =   self.image_folder + "/" + self.selected_file_name
        except StopIteration as e:
            # self.selected_file_date = "unknown.png"
            print(e)
        # print(self.time_pycamera_file_name_dic)
        # print(self.time_thermal_file_name_dic)


        # error log when there is no images in /images :
        # Traceback(most recent call last):  File  "C:\Users\Jack\PycharmProjects\file_server\final_v5\corona_alarm.py", line
        # 439, in < module > corona_alarm = Corona_alarm("images", "11-1-1-1-2")
        #
        # File  "C:\Users\Jack\PycharmProjects\file_server\final_v5\corona_alarm.py", line  69, in __init__
        # print(self.selected_file_date)
        #
        # AttributeError: 'Corona_alarm'  object  has   no   attribute 'selected_file_date'

        # print(self.selected_file_date)
        try:
            self.cv_img = cv2.cvtColor(cv2.imread(self.selected_file_date), cv2.COLOR_BGR2RGB)  # "2021_02_08_T_20_54_25__812.png"
        except AttributeError as e:
            self.cv_img = cv2.cvtColor(cv2.imread("unknown.png"), cv2.COLOR_BGR2RGB)  # "2021_02_08_T_20_54_25__812.png"

        thermal_image_size = self.thermal_image_size
        self.cv_img = cv2.resize(self.cv_img, thermal_image_size)
        # self.photo = ImageTk.PhotoImage(image=PilImage.Image.fromarray(self.cv_img))
        # print(self.cv_img)
        self.photo = ImageTk.PhotoImage(master=self.window,image=Image.fromarray(self.cv_img))


        # frame for the images:
        self.image_frame_right = LabelFrame(self.window, text="images")
        self.image_frame_right.grid(row=0, column=1)
        # frame for the images:
        self.image_frame_left = LabelFrame(self.window, text="images")
        self.image_frame_left.grid(row=0, column=0)

        # my_img = ImageTk.self.photoImage(Image.fromarray(self.cv_img))
        self.my_label = Label(self.image_frame_left,image=self.photo)
        # my_img2 = ImageTk.PhotoImage(Image.open("Maria.png"))
        self.my_label.grid(row=0, column=0)

        self.start_button = Button(self.image_frame_left,text="Mesure Temperature", highlightthickness=0, command=self.mesure_temperature)
        self.start_button.grid(row=1, column=0)

        self.face_recognition_button = Button(self.image_frame_right,text="Face Recognition", highlightthickness=0, command=self.face_recognition)
        self.face_recognition_button.grid(row=1, column=1)

        # button for datetime entry
        # self.start_button = Button(self.window,text="Load Alarm", highlightthickness=0)#, command=)
        # self.start_button.grid(row=0, column=2)
        #calendar
        # root.geometry("600x 400")

        # self.cal.bind("<<CalendarSelected>>", self.grab_date)
        self.frame_mother = LabelFrame(self.window, text="Please insert a time value:")
        self.frame_mother.grid(row=1, column=1)


        self.frame = LabelFrame(self.frame_mother, text="")
        self.frame.pack(side=LEFT)
        # buttons for frame
        self.hourText = StringVar(master=self.window)

        self.hour_label = Label(self.frame,text="Hour:")
        self.hour_label.grid(row=0,column=0)
        self.hour_entry = Entry(self.frame, textvariable=self.hourText)
        self.hour_entry.grid(row=0, column=1)

        self.minText = StringVar(master=self.window)
        self.min_label = Label(self.frame,text="Minute:")
        self.min_label.grid(row=1,column=0)
        self.min_entry = Entry(self.frame, textvariable=self.minText)
        self.min_entry.grid(row=1, column=1)

        self.secondsText = StringVar(master=self.window)
        self.second_label = Label(self.frame,text="Second:")
        self.second_label.grid(row=2,column=0)
        self.second_entry = Entry(self.frame, textvariable= self.secondsText)
        self.second_entry.grid(row=2, column=1)

        self.milisecondsText = StringVar(master=self.window)
        self.milisecond_label = Label(self.frame,text="milisecond:")
        self.milisecond_label.grid(row=3,column=0)
        self.mili_second_entry = Entry(self.frame, textvariable= self.milisecondsText)
        self.mili_second_entry.grid(row=3, column=1)

        #seconds to dowload:
        self.how_long_label = Label(self.frame,text="How Long:")
        self.how_long_label.grid(row=4,column=0)
        self.spin_alarm = Spinbox(self.frame, from_=0.000, to=100.000, format="%.1f", increment=0.1)
        self.spin_alarm.grid(row=4, column=1)

        self.download_alarm_button = Button(self.frame,text="Load Alarm", command=self.grab_date)
        self.download_alarm_button.grid(row=5, column=1)

#calendar
        self.cal = Calendar(self.frame_mother, selectmode="day")
        self.cal.pack(side=LEFT)


        # image from pycam
        self.width = monitor_width//2
        self.height = monitor_height//2
        #find and load the closest pyimage

        # Traceback(most        recent        call        last):        File        "C:\Users\Jack\PycharmProjects\file_server\final_v5\corona_alarm.py", line
        # 453, in < module >        corona_alarm = Corona_alarm("images", "11-1-1-1-2")
        #
        # File        "C:\Users\Jack\PycharmProjects\file_server\final_v5\corona_alarm.py", line        167, in __init__
        # thermal_convert_date_for_pyImage = datetime.strptime(self.selected_file_name, 'lep_%Y_%m_%d_T_%H_%M_%S__%f.png')
        #
        # AttributeError: 'Corona_alarm'        object        has        no        attribute        'selected_file_name'
        self.selected_py_image_for_face_recognition = "unknown.png"
        try:
            thermal_convert_date_for_pyImage = datetime.strptime(self.selected_file_name, 'lep_%Y_%m_%d_T_%H_%M_%S__%f.png')
            min_difference = 90000.88
            for pycamera_key in self.time_pycamera_file_name_dic:
                total_second = abs((pycamera_key - thermal_convert_date_for_pyImage).total_seconds())
                # print(total_second)
                if min_difference > total_second:
                    min_difference = total_second
                    min_key = pycamera_key
            self.time_pycamera_file_name_dic_index = min_key
            #
            # for pycamera_key in self.time_pycamera_file_name_dic:
            #     min_difference = abs((pycamera_key - thermal_convert_date_for_pyImage).total_seconds())
            #     self.time_pycamera_file_name_dic_index = pycamera_key
            # self.img = Image.open("images/"+self.time_pycamera_file_name_dic[self.time_pycamera_file_name_dic_index])
            self.img = Image.open(self.image_folder+"/"+self.time_pycamera_file_name_dic[self.time_pycamera_file_name_dic_index])
            self.selected_py_image_for_face_recognition = self.image_folder+"/"+self.time_pycamera_file_name_dic[self.time_pycamera_file_name_dic_index]
        except UnidentifiedImageError as e:
            self.img = Image.open("unknown.png")
        except AttributeError as e:
            self.img = Image.open("unknown.png")

            print(e)
        self.img = self.img.resize((self.width, self.height), Image.ANTIALIAS)
        self.photoImg = ImageTk.PhotoImage(self.img,master=self.window)
        self.my_label_pycamera = Label(self.image_frame_right,image=self.photoImg)
        self.my_label_pycamera.grid(row=0, column=1)

        # Label from alarm
        self.alarm_label = alarm_label
        self.alarm_information_label = Label(self.window,
            text=alarm_label, background=blue_gray,
            fg='white')
        self.alarm_information_label.grid(row=2, column=0)

        # the number of seconds to retrieve the images

        # frame for the list:

        self.listbox_frame = LabelFrame(self.window, text="Please choose:")
        self.listbox_frame.grid(row=1, column=0)

        # spin = Spinbox(window, from_=0.000, to=100.000, width=5)
        self.spin = Spinbox(self.listbox_frame, from_=0.000, to=100.000, format="%.1f", increment=0.1)
        self.spin.grid(row=4, column=0)

        self.start_button = Button(self.listbox_frame,text="Download", highlightthickness=0, command=self.send_request_download_files)
        self.start_button.grid(row=5, column=0)



        #refresh the list
        self.start_button = Button(self.listbox_frame,text="Refresh List", highlightthickness=0, command=self.clear_list_box)
        self.start_button.grid(row=6, column=0)

        # scrollbar
        self.scrollbar = Scrollbar(self.listbox_frame, orient=VERTICAL)
        self.scrollbar.grid(row=3, column=1, sticky=N + S + E)
        # listbox
        self.mylist = Listbox(self.listbox_frame, yscrollcommand=self.scrollbar.set, width=25)
        self.mylist.grid(row=3, column=0)
        # bind self.scrollbar with the listbox
        self.scrollbar.config(command=self.mylist.yview)

        self.window.title("Corona Alarm")
        self.window.config()

        self.load_list()

        self.mylist.bind("<<ListboxSelect>>", self.callback)

        # print("self.mylist:")
        # print(self.mylist.get(0,END))

        # self.window.mainloop() # no problem!

    def grab_date(self,*args):
        try:
            print("   text                  " + self.hourText.get())# test
            self.hour_value = int(self.hourText.get())
        except ValueError as e:
            self.hour_value =0
        try:
            self.minute_value = int(self.minText.get())
        except ValueError as e:
            self.minute_value =0
        try:
            self.second_value = int(self.secondsText.get())
        except ValueError as e:
            self.second_value = 0
        try:
            self.milisecond_value = int(self.milisecondsText.get())
        except ValueError as e:
            self.milisecond_value = 0
        if self.hour_value<0 or self.hour_value>24 or self.minute_value<0 or self.minute_value>60 or self.second_value<0 or self.second_value>60:
            messagebox.showwarning(title="Invalid Time Value", message="Please insert a valid time value!")
            return
        date_str = self.cal.get_date().split("/")
        year = date_str[2]
        month =""
        if len(date_str[0]) ==1:
            month = "0" + date_str[0]
        if len(date_str[1]) ==1:
            day = "0" + date_str[1]
        else:
            day = date_str[1]
        if self.hour_value<10:
            hour_value = "0"+ str(self.hour_value)
        else:
            hour_value =  str(self.hour_value)
        if self.minute_value<10:
            minute_value = "0" + str(self.minute_value)
        else:
            minute_value = str(self.minute_value)
        if self.second_value<10:
            second_value = "0" + str(self.second_value)
        else:
            second_value = str(self.second_value)
        if self.milisecond_value<10:
            milisecond_value = "00" + str(self.milisecond_value)
        elif self.milisecond_value<100:
            milisecond_value = "0" + str(self.milisecond_value)
        else:
            milisecond_value = str(self.milisecond_value)


        print(day)
        print(month, year, day)
        # date_str_object = datetime.date(year= int(year), month=int(month), days=int(day))
        # print(date_str_object)
        # 'lep_%Y_%m_%d_T_%H_%M_%S__%f.png'
        #   lep_2021_04_12_T_17_29_00__657.png
        #   lep_2020_05_22_T_00_00_00__000.png
        self.date_time_alarm_request_str = "lep_20" +year+"_"+ month+"_"+day+"_T_"+hour_value+"_"+minute_value+"_"+second_value+"__"+milisecond_value+".png"
        print(self.date_time_alarm_request_str)
        #send the socket!
        new_socket_file_request = socket_file_request.Socket_file_request("alarm/"+ self.date_time_alarm_request_str,self.spin_alarm.get())
        new_socket_file_request.send_socket()

        # self.date_time_alarm_request = datetime.strptime(self.selected_file_name, 'lep_%Y_%m_%d_T_%H_%M_%S__%f.png')
        self.alarm_information_label.config(text=self.cal.get_date() + "    " + str(self.hour_value) + ":" + str(self.minute_value)
                                                                                   + ":" + str(self.second_value)
                                                                                   + ":" + str(self.milisecond_value))
        # self.date_time_alarm_request = datetime
        # pass
        # my_label.config(text=cal.get_date())

    def init_time_thermal_pycamera_dic(self):

        self.time_thermal_file_name_dic = {}
        self.time_pycamera_file_name_dic = {}

        self.time_thermal_file_name_dic, self.time_pycamera_file_name_dic = self.init_Image_dictionaries(
            os.listdir(self.image_folder))
        print(self.time_thermal_file_name_dic)
        print(self.time_pycamera_file_name_dic)

    def clear_list_box(self):

        self.mylist.destroy()

        # self.mylist = Listbox(self.window, yscrollcommand=self.scrollbar.set, width=25)
        self.mylist = Listbox(self.listbox_frame, yscrollcommand=self.scrollbar.set, width=25)
        self.init_Image_dictionaries(os.listdir(self.image_folder))
        self.load_list()

        self.mylist.grid(row=3, column=0)
        # bind self.scrollbar with the listbox
        self.scrollbar.config(command=self.mylist.yview)
        self.mylist.bind("<<ListboxSelect>>", self.callback)


        self.reload_list()
    def init_Image_dictionaries(self,my_list):
        # self.time_thermal_file_name_dic = {}
        # self.time_pycamera_file_name_dic = {}
        for file in my_list:
            if file.endswith('png'):
                if file.startswith("lep_"):
                    datetime_object = datetime.strptime(file, 'lep_%Y_%m_%d_T_%H_%M_%S__%f.png')  # 2021_02_08_T_20_54_23__669
                    self.time_thermal_file_name_dic[datetime_object] = file
                # print(self.time_thermal_file_name_dic)
                # print(file)
                # print(datetime_object)
            if file.startswith('cam_'):
                datetime_object = datetime.strptime(file, 'cam_%Y_%m_%d_T_%H_%M_%S__%f.jpg')
                self.time_pycamera_file_name_dic[datetime_object] = file
        return self.time_thermal_file_name_dic, self.time_pycamera_file_name_dic
            #print(datetime_object)




    # button to send to the raspberry using socket

    def send_request_download_files(self):
        # global self.time_thermal_file_name_dic, self.time_pycamera_file_name_dic
        # self.time_thermal_file_name_dic, self.time_pycamera_file_name_dic
        # print(spin.get())
        try:
            new_socket_file_request = socket_file_request.Socket_file_request("alarm/" + self.selected_file_date.split("/")[-1],self.spin.get())
            new_socket_file_request.send_socket()
        except AttributeError as e:
            messagebox.showwarning("No Data","Please Download the files from the Raspberry first!")
        # print(type())
        # time.sleep(int(float(self.spin.get()))*3)
        self.time_thermal_file_name_dic, self.time_pycamera_file_name_dic = self.init_Image_dictionaries(os.listdir(self.image_folder))
        # self.window.after(10000, self.reload_list)

        # self.mylist.bind("<<ListboxSelect>>", self.callback)



    # callback funtion for the Mesure Temperature button
    def mesure_temperature(self):
        image_enlargement = 4
        # start3 = measure_temperature_top.Measure_temperature("images/lep_2021_03_04_T_11_17_08__214.png",
        #                                                      (160 * image_enlargement, 120 * image_enlargement))
        try:
            start3 = measure_temperature_top.Measure_temperature(self.window,self.selected_file_date,
                                                             (160 * image_enlargement, 120 * image_enlargement),self.selected_py_image_for_face_recognition)
        except AttributeError as e:
            messagebox.showwarning("No Data","Please Download the files from the Raspberry first!", parent=self.top)


    #apply face recognition

    def face_recognition(self):
        # print(self.selected_py_image_for_face_recognition)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("models/trainer.yml")
        # self.selected_py_image_for_face_recognition I use it to send the file path to the gui
        frame = cv2.imread(self.selected_py_image_for_face_recognition)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            print(x, y, w, h)
            roi_gray = gray[y:y + h, x:x + w]

            # recognize?
            id_, conf = recognizer.predict(roi_gray)
            if conf >= 45:  # and conf<=85 :
                print(id_)
                self.identified_face_recognition_id = id_

            img_item = "models/my-image.png"
            roi_color = frame[y:y + h, x:x + w]
            cv2.imwrite(img_item, roi_gray)

            color = (255, 0, 0)
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
        person_db_gui_for_face_recognition =person_db_gui.Person_gui(self.identified_face_recognition_id,self.window,self.image_folder,self.selected_file_date.split("/")[-1],self.selected_py_image_for_face_recognition)
        self.identified_face_recognition_id = person_db_gui_for_face_recognition.face_recognition_pid
        print(self.identified_face_recognition_id)
        if self.identified_face_recognition_id  != -1:
            person_db_gui_for_face_recognition.face_recognition(self.identified_face_recognition_id)
        else:
            person_db_gui_for_face_recognition.face_recognition(self.identified_face_recognition_id)
        # print(1)
        # todo : ask Prof. Kerer  about the pid


        #set items inside the listbox
    def load_list(self):
        for k in self.time_thermal_file_name_dic.keys():
           self.mylist.insert(END, str(k))



    # reload the list:
    def reload_list(self):
        # load the dictionary again with the new data!
        self.init_time_thermal_pycamera_dic()
        list_items = self.mylist.get(0, END)
        # print(list_items)
        for k in self.time_thermal_file_name_dic.keys():
            # print(type(k))
            str_key = str(k)
            if str_key not in list_items:
                print(k, " is not in the list!")
                self.mylist.insert(END, str(k))


    def callback(self,event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            convert_date = parser.parse(data)
            print("convert_date" , convert_date)
            my_new_img = cv2.imread(self.image_folder + "/"+self.time_thermal_file_name_dic[convert_date])
            self.selected_file_date = self.image_folder + "/"+ self.time_thermal_file_name_dic[convert_date]# to be sent to detect temperature!
            self.cv_img_new = cv2.cvtColor(my_new_img, cv2.COLOR_BGR2RGB)
            my_photo_resize = cv2.resize(self.cv_img_new, self.thermal_image_size)
            self.photo = ImageTk.PhotoImage(master=self.window,image=Image.fromarray(my_photo_resize))
            self.my_label.configure(image=self.photo)
            # print(self.time_thermal_file_name_dic[convert_date])
            # find the closest pyimage file to the selected thermal image
            min_difference = 90000.88
            for pycamera_key in self.time_pycamera_file_name_dic:
                total_second =abs((pycamera_key - convert_date).total_seconds())
                # print(total_second)
                if min_difference > total_second:
                    min_difference = total_second
                    min_key = pycamera_key
            self.time_pycamera_file_name_dic_index = min_key
            # load and set the pyimage!
            print("min_key:  ",min_key , "min_difference:  " , min_difference , " ",)
            self.img = Image.open(self.image_folder + "/"+self.time_pycamera_file_name_dic[min_key])
            # I will use it to do face recognition!
            self.selected_py_image_for_face_recognition = self.image_folder + "/"+self.time_pycamera_file_name_dic[min_key]
            self.img = self.img.resize((self.width, self.height), Image.ANTIALIAS)
            self.photoImg = ImageTk.PhotoImage(self.img,master=self.window)
            self.my_label_pycamera.configure(image=self.photoImg)
            # print(self.photoImg)
            # print(min_difference)
            # print(self.time_pycamera_file_name_dic[pycamera_key])
        else:
            pass
            print("error")

    # def datemask(self, event):
    #     if len(self.entry1.get()) == 2:
    #         self.entry1.insert(END, "/")
    #     elif len(self.entry1.get()) == 5:
    #         self.entry1.insert(END, "/")
    #     elif len(self.entry1.get()) == 11:
    #         self.entry1.delete(10, END)
if __name__ == "__main__":
    win = Tk()
    corona_alarm = Corona_alarm("images","11-1-1-1-2", win)
    win.mainloop()