## IMPORTANT: CHANGE THE IP FROM LOCAL IP!!!
import locale

from tkinter import *
from tkinter import messagebox
import db_navigator_alarm
import cv2
from PIL import ImageTk, Image
import inspect
from shutil import copyfile



class Alarm_Gui:
    def __init__(self, master_window, selected_pyimage_file=None,selected_thermal_file=None ):
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform



        self.top = Toplevel(background='#3c3f41', master=master_window)
        self.top.lift()

        # to see if the caller is from the corona alarm gui
        stack = inspect.stack()
        self.caller_class = stack[1][0].f_locals["self"].__class__.__name__
        the_method = stack[1][0].f_code.co_name

        print("I was called by {}.{}()".format(self.caller_class, the_method))

        if self.caller_class=="Measure_temperature":
            # print("heoo")
            # self.new_row()
            self.selected_pyimage_file = selected_pyimage_file
            self.selected_thermal_file = selected_thermal_file


        # self.top = Tk()
        self.index = 0

        #Colors(https://color.adobe.com/trends/Travel):
        lila = '#3c3f41'
        self.blue_gray= '#3E434C'
        blue = '#4B6EAF'
        self.thermal_image_size = (400,300)
        image_folder = "images"

        # file_name = "2021_02_08_T_20_54_25__812.png"

        self.db_navigator = db_navigator_alarm.Database_navigator()
        self.alarm = self.db_navigator.load_data(" order by alarm_id desc limit 1 ;")

        self.init_photos()
        # seatch btn
        # refresh_button = Button(self.top, text ="Search",padx = "20px", command = search_db)
        # refresh_button.grid(row=1, column=3)
        # drop box search
        self.search_variable = StringVar(self.top)
        self.search_variable.set("Alarm ID(alarm_id)") # default value
        #
        # option_menu = OptionMenu(self.top, search_variable, "Person ID(pid)", "Alarm ID(alarm_id)", "Altitude", "Longitude", "Possibility", "Temperature", "Thermal Photo File Name", "Photo File Name", "Alarm Description")
        # option_menu.configure(padx="40px")
        # option_menu.grid(row=1, column=0)

        #Label for database pid
        self.pid_label = Label(self.top,text="Person ID(pid): ",background =self.blue_gray, fg='white')
        self.pid_label.grid(row=5, column=0)
        # Textbox for database
        self.pid_text = Text(self.top, height=1, width=30)
        self.pid_text.grid(row=6, column=0)
        # first_name_text.insert(END, "Just a text Widget")

        #Label for database alarmid
        self.alarm_id_label = Label(self.top,text="Alarm ID(alarm_id): ",background =self.blue_gray, fg='white')
        self.alarm_id_label.grid(row=3, column=0)
        # Textbox for alarmid


        self.alarm_id_text = Text(self.top, height=1, width=30, bg=blue, fg='white')
        self.alarm_id_text.grid(row=4, column=0)
        self.alarm_id_text.configure(state='disabled')

        # last_name_text.insert(END, "Just a text Widget")

        #Label for database Altitude
        self.altitude_label = Label(self.top,text="Altitude: ",background =self.blue_gray, fg='white')
        self.altitude_label.grid(row=7, column=0)
        # Textbox for database
        self.altitude_text = Text(self.top, height=1, width=30)
        self.altitude_text.grid(row=8, column=0)
        # svnr_text.insert(END, "Just a text Widget")

        #Label for database Longitude
        self.longitude_label = Label(self.top,text="Longitude: ",background =self.blue_gray, fg='white')
        self.longitude_label.grid(row=9, column=0)
        # Textbox for database
        self.longitude_text = Text(self.top, height=1, width=30)
        self.longitude_text.grid(row=10, column=0)
        # birth_date_text.insert(END, "Just a text Widget")

        #Label for database possibility
        self.possibility_label = Label(self.top,text="Possibility: ",background =self.blue_gray, fg='white')
        self.possibility_label.grid(row=11, column=0)
        # Textbox for database
        self.possibility_text = Text(self.top, height=1, width=30)
        self.possibility_text.grid(row=12, column=0)
        # email_text.insert(END, "Just a text Widget")

        #Label for database Temp
        self.temp_label = Label(self.top,text="Temperature: ",background =self.blue_gray, fg='white')
        self.temp_label.grid(row=13, column=0)
        # Textbox for database
        self.temp_text = Text(self.top, height=1, width=30)
        self.temp_text.grid(row=14, column=0)


        #Label for database thermal file name
        self.thermal_filename_label = Label(self.top,text="Thermal Photo File Name: ",background =self.blue_gray, fg='white')
        self.thermal_filename_label.grid(row=5, column=3)
        # Textbox for database
        self.thermal_filename_text = Text(self.top, height=1, width=30)
        self.thermal_filename_text.grid(row=6, column=3)
        # thermal_filename_text.insert(END, "Just a text Widget")

        #Label for database pyimage file name
        self.py_image_label = Label(self.top,text="Photo File Name: ",background =self.blue_gray, fg='white')
        self.py_image_label.grid(row=7, column=3)
        # Textbox for database
        self.py_image_text = Text(self.top, height=1, width=30)
        self.py_image_text.grid(row=8, column=3)
        # py_image_text.insert(END, "Just a text Widget")

        #Label for database alarm_description
        self.alarm_description_label = Label(self.top,text="Alarm Description: ",background =self.blue_gray, fg='white')
        self.alarm_description_label.grid(row=15, column=0)
        # Textbox for database
        self.alarm_description_text = Text(self.top, height=3, width=30)
        self.alarm_description_text.grid(row=16, column=0)
        # address_text.insert(END, "Just a text Widget")

        #Label for database datetime
        self.date_time_label = Label(self.top,text="Date Time: ",background =self.blue_gray, fg='white')
        self.date_time_label.grid(row=9, column=3)
        # Textbox for database
        self.date_time_text = Text(self.top, height=3, width=30)
        self.date_time_text.grid(row=11, column=3)
        # address_text.insert(END, "Just a text Widget")

        # buttons
        self.search_button = Button(self.top, text ="Search",padx = "20px", command = self.search_db)
        self.search_button.grid(row=1, column=3)

        self.new_button = Button(self.top, text="New", padx="25px", command=self.new_row)
        self.new_button.grid(row=14, column=3)

        # def refresh_db():
        #     pass
        #
        # refresh_button = Button(self.top, text ="Refresh",padx = "20px", command = refresh_db)
        # refresh_button.grid(row=15, column=3)

        self.save_button = Button(self.top, text="Save    ", padx="20px", command=self.save_db)
        self.save_button.grid(row=13, column=3)

        self.init_fields()

        self.top.title("Black List")
        self.top.config(bg=lila)
        if self.caller_class=="Measure_temperature":
            print("heoo")
            self.new_row()
            self.selected_pyimage_file = selected_pyimage_file
            self.selected_thermal_file = selected_thermal_file

        # self.top.mainloop()


    def init_photos(self):
        # self.selected_file_date = "images/"+self.alarm["Photo File Name"]
        self.selected_file_date = "images/"+self.alarm["Thermal Photo File Name"]
        # print(self.selected_file_date)
        # selected_file_date = self.selected_file_date
        # print(self.selected_file_date)
        try:
            if self.caller_class == "Measure_temperature":
                self.cv_img = cv2.cvtColor(cv2.imread(self.selected_thermal_file),
                                           cv2.COLOR_BGR2RGB)  # "2021_02_08_T_20_54_25__812.png"
            else:
                self.cv_img = cv2.cvtColor(cv2.imread(self.selected_file_date), cv2.COLOR_BGR2RGB) # "2021_02_08_T_20_54_25__812.png"
        # cv2.imshow("test", cv_img)
        except:
            self.cv_img = cv2.cvtColor(cv2.imread("images/unknown.png"), cv2.COLOR_BGR2RGB) # "2021_02_08_T_20_54_25__812.png"

        self.cv_img = cv2.resize(self.cv_img, self.thermal_image_size)
        # print(self.cv_img)
        self.thermal_photo = ImageTk.PhotoImage(image=Image.fromarray(self.cv_img), master=self.top)

        # print("error")
        # print(self.thermal_photo)
        self.my_label = Label(self.top, image=self.thermal_photo)
        my_img2 = ImageTk.PhotoImage(Image.open("Maria.png"), master=self.top)
        self.my_label.grid(row=2, column=0)

        # image from pycam
        self.width = 400
        self.height = 300
        try:
            if self.caller_class == "Measure_temperature":
                self.img = Image.open(self.selected_pyimage_file) #get the file from the constructor
            else:
                self.img = Image.open("images/"+self.alarm["Photo File Name"])# get the file from db
        except:
            self.img = Image.open("images/unknown.png")# show the unknown.png

        self.img = self.img.resize((self.width, self.height), Image.ANTIALIAS)
        self.photoImg = ImageTk.PhotoImage(self.img, master=self.top)
        self.my_label_pycamera = Label(self.top,image=self.photoImg)
        self.my_label_pycamera.grid(row=2,column=3)
        # search lable
        self.search_label = Label(self.top,text="Search Alarm ID:",background =self.blue_gray, fg='white')
        self.search_label.grid(row=0, column=0)
        # Textbox for database
        self.search_text = Text(self.top, height=1, width=30)
        self.search_text.grid(row=0, column=3)



    # seatch btn
    def search_db(self,*args):
        db_navigator = db_navigator_alarm.Database_navigator()
        searched_value =self.search_text.get("1.0","end-1c")
        where_claus = " where alarm_id = '" +searched_value +"';"
        # print(where_claus)
        self.alarm = db_navigator.load_data(where_claus)
        self.search_text.delete("1.0", "end")
        self.init_fields()

        self.change_photos_from_db()

        print(self.alarm)

    def change_photos_from_db(self):
        # thermal photo from db:
        try:
            self.cv_img = cv2.cvtColor(cv2.imread("images/"+ self.alarm["Thermal Photo File Name"]), cv2.COLOR_BGR2RGB) # "2021_02_08_T_20_54_25__812.png"
        except:
            self.cv_img = cv2.cvtColor(cv2.imread("images/unknown.png"), cv2.COLOR_BGR2RGB) # "2021_02_08_T_20_54_25__812.png"
        self.cv_img = cv2.resize(self.cv_img, self.thermal_image_size)
        self.thermal_photo = ImageTk.PhotoImage(image=Image.fromarray(self.cv_img), master=self.top)
        # self.my_label = Label(self.top, image=self.thermal_photo)
        self.my_label.configure(image=self.thermal_photo)

        # pyImage photo from the db:
        try:
            self.img = Image.open("images/"+self.alarm["Photo File Name"])# get the file from db
        except:
            self.img = Image.open("images/unknown.png")# show the unknown.png

        self.img = self.img.resize((self.width, self.height), Image.ANTIALIAS)
        self.photoImg = ImageTk.PhotoImage(self.img, master=self.top)
        # self.my_label_pycamera = Label(self.top,image=self.photoImg)
        self.my_label_pycamera.configure(image=self.photoImg)



    # add a new row to db
    def new_row(self,*args):
        self.pid_text.delete("1.0", "end")
        self.pid_text.insert('1.0', "")

        self.alarm_id_text.configure(state='normal')
        self.alarm_id_text.delete("1.0", "end")
        self.alarm_id_text.insert('1.0', "")
        self.alarm_id_text.configure(state='disabled')

        self.altitude_text.delete("1.0", "end")
        self.altitude_text.insert('1.0', "")

        self.longitude_text.delete("1.0", "end")
        self.longitude_text.insert('1.0', "")

        self.possibility_text.delete("1.0", "end")
        self.possibility_text.insert('1.0', "")

        self.temp_text.delete("1.0", "end")
        self.temp_text.insert('1.0', "")

        self.thermal_filename_text.delete("1.0", "end")
        self.thermal_filename_text.insert('1.0', "")

        self.py_image_text.delete("1.0", "end")
        self.py_image_text.insert('1.0', "")

        self.alarm_description_text.delete("1.0", "end")
        self.alarm_description_text.insert('1.0', "")

        self.date_time_text.delete("1.0", "end")
        self.date_time_text.insert('1.0', "")

        if self.caller_class=="Measure_temperature":
            self.change_photos_from_gui()
        else:
            self.load_unknown_photos()

    def load_unknown_photos(self):
        # print("CHange to the gui")
        try:
            self.cv_img = cv2.cvtColor(cv2.imread("images/unknown.png"),
                                       cv2.COLOR_BGR2RGB)  # "2021_02_08_T_20_54_25__812.png"
        except:
            self.cv_img = cv2.cvtColor(cv2.imread("images/unknown.png"),
                                       cv2.COLOR_BGR2RGB)  # "2021_02_08_T_20_54_25__812.png"

        self.cv_img = cv2.resize(self.cv_img, self.thermal_image_size)
        # print(self.cv_img)
        self.thermal_photo = ImageTk.PhotoImage(image=Image.fromarray(self.cv_img), master=self.top)

        # my_img2 = ImageTk.PhotoImage(Image.open("Maria.png"), master=self.top)
        self.my_label.configure(image=self.thermal_photo)

        # image from pycam
        self.width = 400
        self.height = 300
        try:
            self.img = Image.open("images/unknown.png")  # show the unknown.png
        except:
            self.img = Image.open("images/unknown.png")  # show the unknown.png

        self.img = self.img.resize((self.width, self.height), Image.ANTIALIAS)
        self.photoImg = ImageTk.PhotoImage(self.img, master=self.top)
        self.my_label_pycamera.configure(image=self.photoImg)



    def change_photos_from_gui(self):
        # print("CHange to the gui")
        try:
            self.cv_img = cv2.cvtColor(cv2.imread(self.selected_thermal_file),
                                       cv2.COLOR_BGR2RGB)  # "2021_02_08_T_20_54_25__812.png"
        except:
            self.cv_img = cv2.cvtColor(cv2.imread("images/unknown.png"),
                                       cv2.COLOR_BGR2RGB)  # "2021_02_08_T_20_54_25__812.png"

        self.cv_img = cv2.resize(self.cv_img, self.thermal_image_size)
        # print(self.cv_img)
        self.thermal_photo = ImageTk.PhotoImage(image=Image.fromarray(self.cv_img), master=self.top)

        # my_img2 = ImageTk.PhotoImage(Image.open("Maria.png"), master=self.top)
        self.my_label.configure(image=self.thermal_photo)

        # image from pycam
        self.width = 400
        self.height = 300
        try:
            self.img = Image.open(self.selected_pyimage_file)  # get the file from the constructor
        except:
            self.img = Image.open("images/unknown.png")  # show the unknown.png

        self.img = self.img.resize((self.width, self.height), Image.ANTIALIAS)
        self.photoImg = ImageTk.PhotoImage(self.img, master=self.top)
        self.my_label_pycamera.configure(image=self.photoImg)


    def save_db(self,*args):
        db_navigator = db_navigator_alarm.Database_navigator()
        alarn_id_value =self.alarm_id_text.get("1.0","end-1c").strip()
        alarm = {}
        alarm["Temperature"]=  self.temp_text.get("1.0","end-1c").strip()
        alarm["Thermal Photo File Name"] = self.thermal_filename_text.get("1.0","end-1c").strip()
        alarm["Detected Date"]= self.date_time_text.get("1.0","end-1c").strip()
        alarm["pid"] =  self.pid_text.get("1.0","end-1c").strip()
        alarm["Photo File Name"] = self.py_image_text.get("1.0","end-1c").strip()
        alarm["Alarm Description"] = self.alarm_description_text.get("1.0","end-1c").strip()
        self.alarm_id_text.configure(state='normal')
        alarm["Alarm id"] = self.alarm_id_text.get("1.0","end-1c").strip()
        self.alarm_id_text.configure(state='disabled')
        alarm["Altitude"]= str(self.altitude_text.get("1.0","end-1c").strip())
        alarm["Longitude"]  = str(self.longitude_text.get("1.0","end-1c").strip())
        alarm["Possibility"] = self.possibility_text.get("1.0","end-1c").strip()
        alarm["thermal_image_hash"] ="nononononononono"
        alarm["pyImage_hash"] = "nononononononono"
        # TODO calculate hash values of the photos

        if alarn_id_value == "" or alarn_id_value == None:
            db_navigator.insert_data(alarm)

        else:
            db_navigator.update_row(alarm)

        try:
            copyfile(self.selected_thermal_file, "images/"+ self.thermal_image_file_name)
            copyfile(self.selected_pyimage_file, "images/" + self.py_image_file_name)
        except:
            print("Error writing the files!")
            pass

    def init_fields(self,*args):
        # pid_label.
        # print(persons[index])
        if self.alarm == {}:
            messagebox.showwarning("Warning", "Please insert value in search box!")
            return
        self.pid_text.delete("1.0", "end")
        self.pid_text.insert('1.0', self.alarm["pid"])

        self.alarm_id_text.configure(state='normal')
        self.alarm_id_text.delete("1.0", "end")
        self.alarm_id_text.insert('1.0', self.alarm["Alarm id"])
        self.alarm_id_text.configure(state='disabled')

        self.altitude_text.delete("1.0", "end")
        self.altitude_text.insert('1.0', self.alarm["Altitude"])

        self.longitude_text.delete("1.0", "end")
        self.longitude_text.insert('1.0', self.alarm["Longitude"])

        self.possibility_text.delete("1.0", "end")
        self.possibility_text.insert('1.0', self.alarm["Possibility"])

        self.temp_text.delete("1.0", "end")
        self.temp_text.insert('1.0', self.alarm["Temperature"])

        self.thermal_filename_text.delete("1.0", "end")
        self.thermal_filename_text.insert('1.0', self.alarm["Thermal Photo File Name"])

        self.py_image_text.delete("1.0", "end")
        self.py_image_text.insert('1.0', self.alarm["Photo File Name"])

        self.alarm_description_text.delete("1.0", "end")
        self.alarm_description_text.insert('1.0', self.alarm["Alarm Description"])

        self.date_time_text.delete("1.0", "end")
        self.date_time_text.insert('1.0', self.alarm["Detected Date"])





if __name__ == '__main__':
    win = Tk("test")
    win.withdraw()
    my_top = Alarm_Gui(win)

    win.mainloop()
