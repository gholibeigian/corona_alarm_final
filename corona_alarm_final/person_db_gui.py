## IMPORTANT: CHANGE THE IP FROM LOCAL IP!!!
import locale

import numpy as np
from tkinter import *
from tkinter import messagebox
import cv2
from PIL import ImageTk, Image
# import playground_database_gui3_person
import db_navigator_person
from shutil import copyfile
import inspect
import mysql.connector

class Person_gui:
    # todo set the id here
    def __init__(self, face_recognition_pid, win, working_directory="images/", thermal_image_file_name="unknown.png", py_image_file_name="unknown.png"):
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform


        stack = inspect.stack()
        self.caller_class = stack[1][0].f_locals["self"].__class__.__name__
        the_method = stack[1][0].f_code.co_name

        print("I was called by {}.{}()".format(self.caller_class, the_method))


        # if __name__ == "__corona_alarm":
        #     print("I am from corona alarm")
        # print(__name__)
        self.working_directory = working_directory
        print(self.working_directory)
        self.thermal_image_file_name = thermal_image_file_name
        self.py_image_file_name = py_image_file_name.split("/")[-1]
        print(self.py_image_file_name+ "\n" + self.py_image_file_name)
        # window = Tk()
        self.face_recognition_pid = face_recognition_pid
        self.top = Toplevel(background='#3c3f41', master=win)
        self.top.lift()

        self.index = 0

        #Colors(https://color.adobe.com/trends/Travel):
        self.lila = '#3c3f41'
        self.blue_gray= '#3E434C'
        self.blue = '#4B6EAF'
        self.thermal_image_size = (400,300)
        # self.image_folder = "images"

        # such a nub I am!
        # self.db = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     passwd="",
        #     database="corona_alarm"
        # )
        # self.mycursor = self.db .cursor(buffered=True)
        #
        # self.mycursor.execute("select * from alarms;")
        # for row in self.mycursor:
        #     # print(row)
        #     pid = row[0]
        #     altitude = row[1]
        #     longitude = row[2]
        #     temperature = row[3]
        #     time_detected = row[6]
        #     # self.file_name = "lep_2021_03_04_T_11_17_07__778.png" #row[7]
        # self.file_name = "unknown.png" #row[7]

        # print("images/"+self.file_name)
        if self.working_directory == "images/":
            self.selected_file_date = "images/"+thermal_image_file_name
        else:
            self.selected_file_date = self.working_directory + "/" + thermal_image_file_name

        print(self.selected_file_date)
        self.cv_img = cv2.cvtColor(cv2.imread(self.selected_file_date), cv2.COLOR_BGR2RGB) # "2021_02_08_T_20_54_25__812.png"
        # cv2.imshow("test", self.cv_img)
        self.cv_img = cv2.resize(self.cv_img, self.thermal_image_size)
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img), master=self.top)
        # imgtk = ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2image)
        # my_img = ImageTk.PhotoImage(Image.fromarray(self.cv_img))
        self.my_label = Label(self.top,image=self.photo)
        # my_img2 = ImageTk.PhotoImage(Image.open("Maria.png"),master= self.top )
        self.my_label.grid(row=2,column=0)

        # image from pycam
        self.width = 400
        self.height = 300
        # self.img = Image.open("images/cam_2021_03_04_T_11_03_05__657162.jpg") # old try
        if self.working_directory=="images/":
            self.img = Image.open("images/"+ py_image_file_name) # new try
        else:#
            self.img = Image.open(py_image_file_name)
        self.img = self.img.resize((self.width, self.height), Image.ANTIALIAS)
        self.photoImg = ImageTk.PhotoImage(self.img,master= self.top)
        self.my_label_pycamera = Label(self.top,image=self.photoImg)
        self.my_label_pycamera.grid(row=2,column=3)


        # search lable
        self.search_label = Label(self.top,text="Search: ",background =self.blue_gray, fg='white')
        self.search_label.grid(row=0, column=0)
        # Textbox for database
        self.search_text = Text(self.top, height=1, width=30)
        self.search_text.grid(row=0, column=3)

        # next and previous buttons
        self.next_button = Button(self.top, text="Next", padx="25px", command=self.next_row)
        self.previous_button = Button(self.top, text="previous", padx="25px", command=self.previous_row)

        # seatch btn
        self.refresh_button = Button(self.top, text="Search", padx="20px", command=self.search_db)
        self.refresh_button.grid(row=1, column=3)
        # drop box search
        self.search_variable = StringVar(self.top)
        self.search_variable.set("SVNR")  # default value

        self.option_menu = OptionMenu(self.top, self.search_variable, "First Name", "Last Name", "SVNR", "Birth Date", "Email",
                                 "Phone", "Address", "PID", "Thermal Photo File Name", "Photo File Name")
        self.option_menu.configure(padx="40px")
        self.option_menu.grid(row=1, column=0)

        # Label for database firstname
        self.first_name_label = Label(self.top,text="First Name: ", background=self.blue_gray, fg='white')
        self.first_name_label.grid(row=3, column=0)
        # Textbox for database
        self.first_name_text = Text(self.top, height=1, width=30)
        self.first_name_text.grid(row=4, column=0)
        # self.first_name_text.insert(END, "Just a text Widget")

        # Label for database lastname
        self.last_name_label = Label(self.top,text="Last Name: ", background=self.blue_gray, fg='white')
        self.last_name_label.grid(row=5, column=0)
        # Textbox for database
        self.last_name_text = Text(self.top, height=1, width=30)
        self.last_name_text.grid(row=6, column=0)
        # self.last_name_text.insert(END, "Just a text Widget")

        # Label for database SVNR
        self.svnr_label = Label(self.top,text="SVNR: ", background=self.blue_gray, fg='white')
        self.svnr_label.grid(row=7, column=0)
        # Textbox for database
        self.svnr_text = Text(self.top, height=1, width=30)
        self.svnr_text.grid(row=8, column=0)
        # self.svnr_text.insert(END, "Just a text Widget")

        # Label for database birth date
        self.birth_date_label = Label(self.top,text="Birth Date: ", background=self.blue_gray, fg='white')
        self.birth_date_label.grid(row=9, column=0)
        # Textbox for database
        self.birth_date_text = Text(self.top, height=1, width=30)
        self.birth_date_text.grid(row=10, column=0)
        # self.birth_date_text.insert(END, "Just a text Widget")

        # Label for database email
        self.email_label = Label(self.top,text="Email: ", background=self.blue_gray, fg='white')
        self.email_label.grid(row=11, column=0)
        # Textbox for database
        self.email_text = Text(self.top, height=1, width=30)
        self.email_text.grid(row=12, column=0)
        # self.email_text.insert(END, "Just a text Widget")

        # Label for database tel
        self.phone_label = Label(self.top,text="Phone: ", background=self.blue_gray, fg='white')
        self.phone_label.grid(row=13, column=0)
        # Textbox for database
        self.phone_text = Text(self.top, height=1, width=30)
        self.phone_text.grid(row=14, column=0)
        # self.phone_text.insert(END, "Just a text Widget")

        # Label for database pid
        self.pid_label = Label(self.top,text="PID: ", background=self.blue_gray, fg='white')
        self.pid_label.grid(row=3, column=3)
        # Textbox for database
        self.pid_text = Text(self.top, height=1, width=30)
        self.pid_text.config(state='disabled')
        self.pid_text.grid(row=4, column=3)
        # self.pid_text.insert(END, "Just a text Widget")

        # Label for database thermal file name
        self.thermal_filename_label = Label(self.top,text="Thermal Photo File Name: ", background=self.blue_gray, fg='white')
        self.thermal_filename_label.grid(row=5, column=3)
        # Textbox for database
        self.thermal_filename_text = Text(self.top, height=1, width=30)
        self.thermal_filename_text.grid(row=6, column=3)
        # self.thermal_filename_text.insert(END, "Just a text Widget")

        # Label for database pyimage file name
        self.py_image_label = Label(self.top,text="Photo File Name: ", background=self.blue_gray, fg='white')
        self.py_image_label.grid(row=7, column=3)
        # Textbox for database
        self.py_image_text = Text(self.top, height=1, width=30)
        self.py_image_text.grid(row=8, column=3)

        # self.py_image_text.insert(END, "Just a text Widget")

        # RADIO BOX
        # able to store any string value

        # Loop is used to create multiple Radiobuttons
        # rather than creating each button separately
        # def do_nothing():
        #     pass

        ## TKINTER BUG
        # v = IntVar()
        #
        # male_radioButton = Radiobutton(self.top, text="Male", variable=v,background =self.blue_gray, fg='white',value=0, command=do_nothing)
        # male_radioButton.grid(row=9, column=3)
        # female_radioButton = Radiobutton(self.top, text="Female", variable=v,background =self.blue_gray, fg='white',value=1, command=do_nothing)
        # female_radioButton.grid(row=10, column=3)

        self.gender_label = Label(self.top,text="Gender: ", background=self.blue_gray, fg='white')
        self.gender_label.grid(row=9, column=3)

        self.gender_v = IntVar(master= self.top)
        # self.top.configure(fg="white")
        self.male_radioButton = Radiobutton(self.top, text="Male", variable=self.gender_v, value=0, background=self.blue_gray,
                                       fg='green').grid(row=10, column=3, sticky="w")
        # self.male_radioButton.config(fg= "white")
        self.male_radioButton = Radiobutton(self.top, text="Female", variable=self.gender_v, value=1, background=self.blue_gray,
                                         fg='green').grid(row=11, column=3, sticky="w")

        # in black list
        self.in_blacklist_label = Label(self.top,text="Is he/she in blacklist? ", background=self.blue_gray, fg='white')
        self.in_blacklist_label.grid(row=12, column=3)

        self.blacklist_v = IntVar(master= self.top)
        # self.top.configure(fg="white")
        self.in_blacklist_radiobutton_true = Radiobutton(self.top, text="True", variable=self.blacklist_v, value=1,
                                                    background=self.blue_gray, fg='green').grid(row=13, column=3,
                                                                                                sticky="w")
        # self.male_radioButton.config(fg= "white")
        self.in_blacklist_radiobutton_false = Radiobutton(self.top, text="False", variable=self.blacklist_v, value=0,
                                                     background=self.blue_gray, fg='green').grid(row=14, column=3,
                                                                                                 sticky="w")

        # Label for database address
        self.address_label = Label(self.top,text="Address: ", background=self.blue_gray, fg='white')
        self.address_label.grid(row=15, column=0)
        # Textbox for database
        self.address_text = Text(self.top, height=3, width=30)
        self.address_text.grid(row=16, column=0)
        # self.address_text.insert(END, "Just a text Widget")

        # save btn
        self.save_button = Button(self.top, text ="Save",padx = "25px", command = self.save_in_db)
        self.save_button.grid(row=15, column=3)
        # refresh btn

        self.refresh_button = Button(self.top, text="Refresh", padx="20px", command=self.refresh_db)
        self.refresh_button.grid(row=16, column=3)

        # add a new row to db
        self.new_button = Button(self.top, text="New", padx="25px", command=self.new_row)
        self.new_button.grid(row=17, column=3)

        # close and set the face recognition_pid

        self.save_close_button = Button(self.top, text="Select & Close", padx="5px",command= lambda: self.save_close(face_recognition_pid) )
        self.save_close_button.grid(row=18, column=3)

        self.persons = []
    def save_close(self, pid_face_recognized):
        # TODO pass the parameters to the function 2- handel this error
        self.face_recognition_pid = int(self.pid_text.get("1.0","end-1c"))
        # print(args[0])
        print(int(self.pid_text.get("1.0","end-1c")))
        pid_face_recognized =int(self.pid_text.get("1.0","end-1c"))

        # print(type(pid), type(self.pid_text.get("1.0","end-1c")))
        # just like the save function, but with image file name from the corona alarm!

        # create a dictionary to send to the database
        new_person = {}
        # search_text.get("1.0","end-1c").strip()
        new_person["First Name"] = self.first_name_text.get("1.0","end-1c").strip()
        new_person["Last Name"] = self.last_name_text.get("1.0","end-1c").strip()
        new_person["SVNR"] = self.svnr_text.get("1.0","end-1c").strip()
        new_person["Birth Date"] = self.birth_date_text.get("1.0","end-1c").strip()
        new_person["Email"] = self.email_text.get("1.0","end-1c").strip()
        new_person["Phone"] = self.phone_text.get("1.0","end-1c").strip()
        new_person["Address"] = self.address_text.get("1.0","end-1c").strip()
        new_person["PID"] = self.pid_text.get("1.0","end-1c").strip()
        # new_person["Thermal Photo File Name"] = self.thermal_filename_text.get("1.0","end-1c").strip()#"lep_2021_03_04_T_11_17_09__242.png"
        new_person["Thermal Photo File Name"] = self.thermal_image_file_name#"lep_2021_03_04_T_11_17_09__242.png"
        # new_person["Photo File Name"] = self.py_image_text.get("1.0","end-1c").strip()#"cam_2021_03_04_T_11_03_09__928115.jpg"
        new_person["Photo File Name"] = self.py_image_file_name#"cam_2021_03_04_T_11_03_09__928115.jpg"
        new_person["thermal_image_hash"] = "HASHVALUE"
        new_person["pyImage_hash"] = "HASHVALUE"
        new_person["Gender"] = self.gender_v.get()  # chage
        new_person["in_blacklist"] = self.blacklist_v.get()
        # connect to the database and update the row
        # copy the files to the /images folder:
        try:
            copyfile(self.working_directory + "/" + self.thermal_image_file_name, "images/"+ self.thermal_image_file_name)
            copyfile(self.working_directory + "/" + self.py_image_file_name, "images/" + self.py_image_file_name)
        except:
            print("Error writing the files!")
            pass
        db_executor =db_navigator_person.Database_navigator()
        if self.pid_text.get("1.0","end-1c").strip()!="" or self.pid_text.get("1.0","end-1c").strip()==None:
            rows_affected_update = db_executor.update_row(new_person)
            messagebox.showinfo('Info', str(rows_affected_update) + " person record(s) affected!", parent=self.top)
        else:
            rows_affected_insert = db_executor.insert_data(new_person)
            messagebox.showinfo('Info', str(rows_affected_insert) + " new person is added!")
            if rows_affected_insert == -1:
                self.face_recognition_save_load_gui_data(" where pid=(select max(pid) from persons)")
            #TODO IMPLEMERT INSERT
            # rows_affected_insert =




        self.top.destroy()
        self.top.update()# todo : ask Prof. Kerer  about the pid

    def init_person_data(self):
        # print("test: "  )
        print(self.persons[self.index])
        self.first_name_text.delete("1.0", "end")
        self.first_name_text.insert('1.0',self.persons[self.index]["First Name"])

        self.last_name_text.delete("1.0", "end")
        self.last_name_text.insert('1.0',self.persons[self.index]["Last Name"])

        self.svnr_text.delete("1.0", "end")
        self.svnr_text.insert('1.0',self.persons[self.index]["SVNR"])

        # self.birth_date_text.delete("1.0", "end")
        # self.birth_date_text.insert('1.0',self.persons[self.index]["Birth Date"])

        self.email_text.delete("1.0", "end")
        self.email_text.insert('1.0',self.persons[self.index]["Email"])

        self.phone_text.delete("1.0", "end")
        self.phone_text.insert('1.0',self.persons[self.index]["Phone"])

        self.address_text.delete("1.0", "end")
        self.address_text.insert('1.0',self.persons[self.index]["Address"])

        self.pid_text.configure(state='normal')
        self.pid_text.delete("1.0", "end")
        self.pid_text.insert('1.0',self.persons[self.index]["PID"])
        self.pid_text.configure(state='disabled')

        self.thermal_filename_text.delete("1.0", "end")
        self.thermal_filename_text.insert('1.0',self.persons[self.index]["Thermal Photo File Name"])
        try:
            # change thermal image
            self.thermal_image_in_show= "images/" + self.persons[self.index]["Thermal Photo File Name"]  # to be sent to detect temperature!
            my_new_img = cv2.imread(self.thermal_image_in_show)
            cv_img_new = cv2.cvtColor(my_new_img, cv2.COLOR_BGR2RGB)
            my_photo_resize = cv2.resize(cv_img_new, self.thermal_image_size)
            self.photo = ImageTk.PhotoImage(master=self.top, image=Image.fromarray(my_photo_resize))
            self.my_label.configure(image=self.photo)

            # change pyImage
            self.img = Image.open("images/" + self.persons[self.index]["Photo File Name"])
            self.img = self.img.resize((self.width, self.height), Image.ANTIALIAS)
            self.photoImg = ImageTk.PhotoImage(self.img, master=self.top)
            self.my_label_pycamera.configure(image=self.photoImg)
        except:
            # when there is a problem while loading the images, it should load the /images/unknown.png!
            self.img = Image.open("images/" + "unknown.png")
            self.img = self.img.resize((self.width, self.height), Image.ANTIALIAS)
            self.photoImg = ImageTk.PhotoImage(self.img, master=self.top)
            self.my_label_pycamera.configure(image=self.photoImg)

            self.thermal_image_in_show= "images/"+ "unknown.png"  # to be sent to detect temperature!
            my_new_img = cv2.imread(self.thermal_image_in_show)
            cv_img_new = cv2.cvtColor(my_new_img, cv2.COLOR_BGR2RGB)
            my_photo_resize = cv2.resize(cv_img_new, self.thermal_image_size)
            self.photo = ImageTk.PhotoImage(master=self.top, image=Image.fromarray(my_photo_resize))
            self.my_label.configure(image=self.photo)


        self.py_image_text.delete("1.0", "end")
        self.py_image_text.insert('1.0',self.persons[self.index]["Photo File Name"])
        #blacklist
        if self.persons[self.index]["in_blacklist"] =="1":
            print("inblacklist")
            self.blacklist_v.set(1)
            self.pid_text.configure(background="red")

        if self.persons[self.index]["in_blacklist"] =="0":
            self.blacklist_v.set(0)
            self.pid_text.configure(background="green")
        #gender
        if self.persons[self.index]["Gender"] == "1":
            self.gender_v.set(0)
        if self.persons[self.index]["Gender"] == "0":
            self.gender_v.set(1)

    def search_db(self):
        # global index
        # global persons
        self.index = 0
        print(self.search_variable.get())
        where_claus = " where "
        if  (self.search_text.get("1.0","end-1c")).strip() =="":
            messagebox.showwarning( "Warning" , "Please insert value in search box!", master=self.top)
            return

        if self.search_variable.get() == "First Name":
            searched_value =self.search_text.get("1.0","end-1c").strip()
            where_claus += " First_name like '%" +searched_value +"%';"

        elif self.search_variable.get() == "Last Name":
            searched_value =self.search_text.get("1.0","end-1c").strip()
            where_claus += " Last_name like '%" +searched_value +"%';"

        elif self.search_variable.get() == "SVNR":
            searched_value =self.search_text.get("1.0","end-1c")
            where_claus += " SVNR = '" +searched_value +"';"

        elif self.search_variable.get() == "Birth Date":
            searched_value =self.search_text.get("1.0","end-1c")
            where_claus += " Birth_date = '" +searched_value +"';"

        elif self.search_variable.get() == "Email":
            searched_value =self.search_text.get("1.0","end-1c")
            where_claus += " Email = '" +searched_value +"';"

        elif self.search_variable.get() == "Phone":
            searched_value =self.search_text.get("1.0","end-1c")
            where_claus += " Tel = '" +searched_value +"';"

        elif self.search_variable.get() == "Address":
            searched_value =self.search_text.get("1.0","end-1c").strip()
            where_claus += " Address LIKE '%" +searched_value +"%';"

        elif self.search_variable.get() == "PID":
            searched_value =self.search_text.get("1.0","end-1c")
            where_claus += " pid = '" +searched_value +"';"

        elif self.search_variable.get() == "Thermal Photo File Name":
            raise EXCEPTION("please change the database to have the file names")
            searched_value =self.search_text.get("1.0","end-1c")
            where_claus += " thermal_file_name = '" +searched_value +"';"

        elif self.search_variable.get() == "Photo File Name":
            raise EXCEPTION("please change the database to have the file names")
            searched_value =self.search_text.get("1.0","end-1c")
            where_claus += " pyImage_file_name = '" +searched_value +"';"

        else:
            where_claus = ";"

        person_query = db_navigator_person.Database_navigator()
        # global persons
        self.persons  =person_query.load_data(where_claus)
        # print(self.persons)
        messagebox.showinfo('Info', str(len(self.persons)) + ' records have been found',parent=self.top)

        if len(self.persons)> 1:
            # Next btn
            self.next_button.grid(row=2, column=1)

            # Previous btn
            self.previous_button.grid(row=2, column=2)
            self.index = 0
            self.init_person_data()

        elif len(self.persons) == 1:
            self.index =0
            self.next_button.grid_forget()
            self.previous_button.grid_forget()
            self.init_person_data()


        print(where_claus)
        self.search_text.delete("1.0", "end")
    def face_recognition_save_load_gui_data(self, where_claus):
        person_query = db_navigator_person.Database_navigator()
        # global persons
        self.persons = person_query.load_data(where_claus)
        # print(self.persons)
        # messagebox.showinfo('Info', str(len(self.persons)) + ' records have been found')

        print(where_claus)
        self.search_text.delete("1.0", "end")
        self.init_person_data()

    def face_recognition(self,pid):

        self.index = 0
        print(self.search_variable.get())
        where_claus = " where "
        where_claus += " pid = '" + str(pid) + "';"
        person_query = db_navigator_person.Database_navigator()
        # global persons
        self.persons = person_query.load_data(where_claus)
        # print(self.persons)
        messagebox.showinfo('Info', str(len(self.persons)) + ' records have been found', parent=self.top)

        if len(self.persons) > 1:
            # Next btn
            self.next_button.grid(row=2, column=1)

            # Previous btn
            self.previous_button.grid(row=2, column=2)
            self.index = 0
            self.init_person_data()

        elif len(self.persons) == 1:
            self.index = 0
            self.next_button.grid_forget()
            self.previous_button.grid_forget()
            self.init_person_data()

        # print(where_claus)
        self.search_text.delete("1.0", "end")

    def next_row(self):
        # global index
        self.index+=1
        if self.index<len(self.persons):
            self.init_person_data()
        else:
            self.index =len(self.persons)-1
            messagebox.showwarning("Warning", "There is no other person!",parent=self.top)

    def previous_row(self):
        # global self.index
        self.index-=1
        if self.index>=0:
            self.init_person_data()
        else:
            messagebox.showwarning("Warning", "There is no other person!", parent=self.top)

    #Buttons
    def save_in_db(self):
        # create a dictionary to send to the database
        new_person = {}
        # search_text.get("1.0","end-1c").strip()
        new_person["First Name"] = self.first_name_text.get("1.0","end-1c").strip()
        new_person["Last Name"] = self.last_name_text.get("1.0","end-1c").strip()
        new_person["SVNR"] = self.svnr_text.get("1.0","end-1c").strip()
        new_person["Birth Date"] = self.birth_date_text.get("1.0","end-1c").strip()
        new_person["Email"] = self.email_text.get("1.0","end-1c").strip()
        new_person["Phone"] = self.phone_text.get("1.0","end-1c").strip()
        new_person["Address"] = self.address_text.get("1.0","end-1c").strip()
        new_person["PID"] = self.pid_text.get("1.0","end-1c").strip()
        new_person["Thermal Photo File Name"] = self.thermal_filename_text.get("1.0","end-1c").strip()#"lep_2021_03_04_T_11_17_09__242.png"
        # new_person["Thermal Photo File Name"] = self.thermal_image_file_name#"lep_2021_03_04_T_11_17_09__242.png"
        new_person["Photo File Name"] = self.py_image_text.get("1.0","end-1c").strip()#"cam_2021_03_04_T_11_03_09__928115.jpg"
        # new_person["Photo File Name"] = self.py_image_file_name#"cam_2021_03_04_T_11_03_09__928115.jpg"
        new_person["thermal_image_hash"] = "HASHVALUE"
        new_person["pyImage_hash"] = "HASHVALUE"
        new_person["Gender"] = self.gender_v.get()  # chage
        new_person["in_blacklist"] = self.blacklist_v.get()
        # connect to the database and update the row
        db_executor =db_navigator_person.Database_navigator()
        if self.pid_text.get("1.0","end-1c").strip()!="" or self.pid_text.get("1.0","end-1c").strip()==None:
            rows_affected_update = db_executor.update_row(new_person)
            messagebox.showinfo('Info', str(rows_affected_update) + " person record(s) affected!", parent=self.top)
        else:
            rows_affected_insert = db_executor.insert_data(new_person)
            messagebox.showinfo('Info', str(rows_affected_insert) + " new person is added!")
            if rows_affected_insert == -1:
                self.face_recognition_save_load_gui_data(" where pid=(select max(pid) from persons)")
            #TODO IMPLEMERT INSERT
            # rows_affected_insert =

    def refresh_db(self):
        self.init_person_data()

    # refresh btn
    def new_row(self):
        self.first_name_text.delete("1.0", "end")
        self.last_name_text.delete("1.0", "end")
        self.svnr_text.delete("1.0", "end")
        self.birth_date_text.delete("1.0", "end")
        self.email_text.delete("1.0", "end")
        self.phone_text.delete("1.0", "end")
        self.address_text.delete("1.0", "end")
        self.pid_text.configure(state='normal')
        self.pid_text.delete("1.0", "end")
        self.pid_text.configure(state='disabled')
        self.thermal_filename_text.delete("1.0", "end")
        self.py_image_text.delete("1.0", "end")
        if self.caller_class=="Corona_alarm":
            try:
                self.thermal_filename_text.insert('1.0', self.thermal_image_file_name)
                self.py_image_text.insert('1.0', self.py_image_file_name)
                # change thermal image
                self.thermal_image_in_show = self.working_directory + "/" + self.thermal_image_file_name
                my_new_img = cv2.imread(self.thermal_image_in_show)
                cv_img_new = cv2.cvtColor(my_new_img, cv2.COLOR_BGR2RGB)
                my_photo_resize = cv2.resize(cv_img_new, self.thermal_image_size)
                self.photo = ImageTk.PhotoImage(master=self.top, image=Image.fromarray(my_photo_resize))
                self.my_label.configure(image=self.photo)

                # change pyImage
                self.img = Image.open(self.working_directory + "/" + self.py_image_file_name)
                self.img = self.img.resize((self.width, self.height), Image.ANTIALIAS)
                self.photoImg = ImageTk.PhotoImage(self.img, master=self.top)
                self.my_label_pycamera.configure(image=self.photoImg)
            except:
                # when there is a problem while loading the images, it should load the /images/unknown.png!
                self.img = Image.open("images/" + "unknown.png")
                self.img = self.img.resize((self.width, self.height), Image.ANTIALIAS)
                self.photoImg = ImageTk.PhotoImage(self.img, master=self.top)
                self.my_label_pycamera.configure(image=self.photoImg)

                self.thermal_image_in_show = "images/" + "unknown.png"  # to be sent to detect temperature!
                my_new_img = cv2.imread(self.thermal_image_in_show)
                cv_img_new = cv2.cvtColor(my_new_img, cv2.COLOR_BGR2RGB)
                my_photo_resize = cv2.resize(cv_img_new, self.thermal_image_size)
                self.photo = ImageTk.PhotoImage(master=self.top, image=Image.fromarray(my_photo_resize))
                self.my_label.configure(image=self.photo)




if __name__ == "__main__":
    win = Tk("test")
    # my_top = Person_gui(-1,win, working_directory="images/", thermal_image_file_name="lep_2021_04_12_T_17_29_00__657.png",py_image_file_name="cam_2021_04_12_T_17_29_01__694182.jpg")
    my_top = Person_gui(-1,win)#, working_directory="images/", thermal_image_file_name="lep_2021_04_12_T_17_29_00__657.png",py_image_file_name="cam_2021_04_12_T_17_29_01__694182.jpg")
    win.mainloop()
