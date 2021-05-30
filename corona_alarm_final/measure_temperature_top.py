# to work with the temerature perss the ESC to exit the mask selection
# TODO: add the plates and detect the exact temperature of the person!
import locale

import select_mask
import template_matching_top
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import cv2
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import feature_matching_top
import template_matching_top
import alarm_db_gui

class Measure_temperature:
# def mesure_temperature():
    def __init__(self,win, selected_file_date,thermal_image_size,selected_pyimage_file):
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform
        self.selected_pyimage_file = selected_pyimage_file
        monitor_width = win.winfo_screenwidth()
        monitor_height = win.winfo_screenheight()
        #todo find out the size of the thermal_iamge_size
        if monitor_width//2<thermal_image_size[0] and monitor_height//2<thermal_image_size[1]:
            # self.thermal_image_size = thermal_image_size
            self.thermal_image_size = (monitor_width//4,monitor_height//4)

        else: # monitor is big enough!
            self.thermal_image_size = (monitor_width//2,monitor_height//2)


        print("Temp")
        self.selected_file_date = selected_file_date


        self.top = Toplevel(master=win,background='#3c3f41')
        self.top.lift() #list the window

        # main frame
        self.frame_selection = LabelFrame(self.top, background='#3c3f41', fg='white')
        self.frame_selection.grid(row=0, column=0)

        #  labelFrame for image and
        self.image_feature_tools_label_frame = LabelFrame(self.top, background='#3c3f41', fg='white')
        self.image_feature_tools_label_frame.grid(row=1, column=0)

        # labelFrame for buttons features
        self.frame_button_featues = LabelFrame(self.image_feature_tools_label_frame, background='#3c3f41', fg='white')
        self.frame_button_featues.grid(row=0, column=0, sticky="n")



        self.template_matching = Button(self.frame_button_featues, text="Template Matching  ", highlightthickness=0,
                                        command=self.apply_template_matching)

        self.template_matching.grid(row=2, column=0)
        # button feature matching
        self.feature_matching = Button(self.frame_button_featues, text="Feature Matching      ", highlightthickness=0,
                                        command=self.apply_feature_matching)

        self.feature_matching.grid(row=3, column=0)
        # masking for a color range
        self.feature_matching = Button(self.frame_button_featues, text="Color Range Masking", highlightthickness=0,
                                        command=self.color_range_masking)

        self.feature_matching.grid(row=4, column=0)

        # reference button
        self.feature_matching = Button(self.frame_button_featues, text="Reference Masking    ", highlightthickness=0,
                                        command=self.reference_color_range_masking)

        self.feature_matching.grid(row=5, column=0)

        #  labelFrame for buttons save and reload
        self.save_reload_frame = LabelFrame(self.top, background='#3c3f41', fg='white')
        self.save_reload_frame.grid(row=2, column=0)

        # refresh button
        self.feature_matching = Button(self.save_reload_frame, text="Reload", highlightthickness=0,
                                        command=self.refresh, padx="60")

        self.feature_matching.grid(row=0, column=0)

        # save button
        self.save_button = Button(self.save_reload_frame, text="Save  ", highlightthickness=0,
                                        command=self.save, padx="60")

        self.save_button.grid(row=0, column=1)
        # self.frame_selection = LabelFrame(self.top, text="Select by Hand:")

        # tools to select
        self.frame_selection_tools = LabelFrame(self.frame_selection, text="Choose a Pencil", background='#3c3f41', fg='white')
        self.frame_selection_tools.grid(row=0, column=0)
        # Radio buttons
        height_label = Label(self.frame_selection_tools,text="Width: ", background='#3c3f41', fg='white')
        width_label = Label(self.frame_selection_tools,text="Height: ", background='#3c3f41', fg='white')
        height_label.grid(row=4, column=0, sticky="w")
        width_label.grid(row=6, column=0, sticky="w")

        self.shape_v = IntVar(master=self.frame_selection_tools)
        # window.configure(fg="white")
        self.circle_radioButton = Radiobutton(self.frame_selection_tools, text="Circle", variable=self.shape_v, value=0, background='#3c3f41',
                                       fg='yellow')
        self.circle_radioButton.grid(row=1, column=0, sticky="w")
        # male_radioButton.config(fg= "white")
        self.rectangle_radioButton = Radiobutton(self.frame_selection_tools, text="Rectangle", variable=self.shape_v, value=1, background='#3c3f41',
                                         fg='yellow')
        self.rectangle_radioButton.grid(row=3, column=0, sticky="w")

        # circle button
        self.apply_shape_mask_button = Button(self.frame_selection_tools, text="Apply Mask", highlightthickness=0, command=self.draw_circle)

        self.apply_shape_mask_button.grid(row=8 , column=0)

        # clircle scale
        self.var_radius = IntVar(master=self.frame_selection_tools)
        self.scale = Scale(self.frame_selection_tools, from_=1, to=70, orient=HORIZONTAL,
                           background='#3E434C',fg='white',highlightthickness=0, variable=self.var_radius, length=200, command=self.show_circle_preview)

        # self.scale = Scale(self.top)
        self.scale.grid(row=2 , column=0)

        # rectangle scale height
        self.var_height = IntVar(master=self.frame_selection_tools)
        self.height_scale = Scale(self.frame_selection_tools, from_=1, to=200, orient=HORIZONTAL,
                           background='#3E434C',fg='white',highlightthickness=0, variable=self.var_height, length=200,command=self.show_rectangle)

        # self.height_scale = Scale(self.top )
        self.height_scale.grid(row=7 , column=0)

        # rectangle scale width
        self.var_width = IntVar(master=self.frame_selection_tools)
        self.width_scale = Scale(self.frame_selection_tools, from_=1, to=200, orient=HORIZONTAL,
                           background='#3E434C',fg='white',highlightthickness=0, variable=self.var_width, length=200,command=self.show_rectangle)

        # self.width_scale = Scale(self.top )
        self.width_scale.grid(row=5, column=0)



        # Image
        self.cv_img = cv2.cvtColor(cv2.imread(selected_file_date), cv2.COLOR_BGR2RGB)
        self.cv_img = cv2.resize(self.cv_img, self.thermal_image_size)

        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.cv_img),master=self.top)

        # my_img = ImageTk.PhotoImage(Image.fromarray(self.cv_img))
        self.my_label = Label(self.image_feature_tools_label_frame, image=self.photo)
        my_img2 = ImageTk.PhotoImage(Image.open("Maria.png"),master=self.image_feature_tools_label_frame)
        self.my_label.grid(row=0, column=1)

        # the shape
        self.shape_photo_blank = np.zeros((10, 10, 3), np.uint8)
        self.shape_photo_blank = cv2.cvtColor(np.float32(self.shape_photo_blank), cv2.COLOR_RGB2GRAY)
        self.scale_preview_size = 2
        self.shape_photo_blank = cv2.resize(self.shape_photo_blank, (160 * self.scale_preview_size,120 * self.scale_preview_size))
        self.photo_for_label = ImageTk.PhotoImage(image=Image.fromarray(self.shape_photo_blank),master=self.top)
        self.shape_label = Label(self.frame_selection, image=self.photo_for_label)
        # self.shape_photo_blank = np.empty(0)
        # my_img2 = ImageTk.PhotoImage(self.shape_photo_blank ,master=self.top)

        self.shape_label.configure(image=self.photo_for_label)
        self.shape_label.grid(row=0, column=1)

        # apply Button
        # self.start_button = Button(text="Apply Mask", highlightthickness=0)
        # self.start_button.grid(row=1, column=2)

        # Label from alarm
        # self.alarm_information_label = Label(self.top,
        #     text="hi", background='#3E434C',
        #     fg='white')
        # self.alarm_information_label.grid(row=1, column=0)
        # scale<
        color_masking_label = Label(self.frame_button_featues,text="Width: ", background='#3c3f41', fg='white')
        color_masking_label.grid(row=0, column=0, sticky="w")
        self.v = DoubleVar()
        self.scale = Scale(self.frame_button_featues, variable=self.v, from_=1, to=400, orient=HORIZONTAL, command=self.apply_mask1,
                           background='#3E434C',fg='white',highlightthickness=0)
        self.scale.grid(row=1, column=0)

        # self.top.mainloop()
        #aplly feature matching
    def apply_template_matching(self, *args):
        print("Call template matching!")
        start2 = template_matching_top.Template_matching(self.top, self.selected_file_date)

    def apply_feature_matching(self, *args):
        feature_matching_top.Feature_Matching(self.top,selected_file_date=self.selected_file_date)

    def apply_mask1(self, *args):
        global photo
        print(str(self.scale.get()))
        hsv_img = cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2HSV)[:, :, 2]
        blurredBrightness = cv2.bilateralFilter(hsv_img, 9, 150, 150)
        thresh = 50
        edges = cv2.Canny(blurredBrightness, thresh, thresh * 2, L2gradient=True)
        # scale.get was 200!
        _, mask = cv2.threshold(blurredBrightness, self.scale.get(), 1, cv2.THRESH_BINARY)
        print(mask.shape)

        # print(photo)
        erodeSize = 5
        dilateSize = 7
        eroded = cv2.erode(mask, np.ones((erodeSize, erodeSize)))
        mask = cv2.dilate(eroded, np.ones((dilateSize, dilateSize)))
        # cv2.imshow("preview", cv2.resize(cv2.cvtColor(mask * edges, cv2.COLOR_GRAY2RGB) | self.cv_img, self.thermal_image_size,
        #                                  interpolation=cv2.INTER_CUBIC))
        my_photo = cv2.resize(cv2.cvtColor(mask * edges, cv2.COLOR_GRAY2RGB) | self.cv_img, self.thermal_image_size,
                              interpolation=cv2.INTER_CUBIC)
        # photo = cv2.cvtColor(mask * edges, cv2.COLOR_GRAY2RGB)   | self.cv_img
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(my_photo),master=self.top)
        self.my_label.configure(image=self.photo)

    def color_range_masking(self):
        my_photo = cv2.cvtColor(cv2.imread(self.selected_file_date), cv2.COLOR_BGR2RGB)
        hsv = cv2.cvtColor(my_photo, cv2.COLOR_BGR2HSV)

        # Calculate the red values from the references!
        lower_blue = np.array([10, 50, 50])
        upper_blue = np.array([130, 255, 255])

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(my_photo, my_photo, mask=mask)

        # cv2.imshow('frame', my_photo)
        cv2.imshow('mask', mask)
        # cv2.imshow('res',res)


        res = cv2.resize(res, self.thermal_image_size)
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(res),master=self.top)
        self.my_label.configure(image=self.photo)

    def reference_color_range_masking(self):
        #  To do:
        #  Under Construction
        #  Calculate the min reference red value

        #  Calculate the max reference red value

        # Apply mask color_range_masking(minColor, maxColor)

        #calculate the temperature

        pass
    def refresh(self):

        self.cv_img = cv2.cvtColor(cv2.imread(self.selected_file_date), cv2.COLOR_BGR2RGB)
        self.cv_img = cv2.resize(self.cv_img, self.thermal_image_size)
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.cv_img),master=self.top)

        # my_img = ImageTk.PhotoImage(Image.fromarray(self.cv_img))
        self.my_label = Label(self.image_feature_tools_label_frame, image=self.photo)
        my_img2 = ImageTk.PhotoImage(Image.open("Maria.png"),master=self.top)
        self.my_label.grid(row=0, column=1)
    def apply_mask_shape(self):
        pass
    def draw_circle(self):

        int_raduis = self.var_radius.get()
        int_shape = self.shape_v.get()
        print(int_shape)
        mask = select_mask.Select_mask(self.selected_file_date,self.thermal_image_size,int_raduis,int_shape, width=self.var_width.get(),
                                       height=self.var_height.get())
        mask.start()
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(mask.res),master=self.top)
        self.my_label.configure(image=self.photo)
    def show_circle_preview(self, event):
        # (160 * scale_preview_size, 120 * scale_preview_size)
        # change

        # self.var_radius.set(1)
        # int_shape = self.shape_v.get()
        # self.var_radius.set(1)
        self.circle_radioButton.select()

        self.shape_photo_blank = np.zeros((120 * self.scale_preview_size,160 * self.scale_preview_size))
        self.shape_photo_blank = cv2.circle(self.shape_photo_blank, ((160 * self.scale_preview_size//2),((120*self.scale_preview_size)//2)), self.var_radius.get(),(255,255,255),-1)
        # self.photo_for_label
        self.photo_for_label = ImageTk.PhotoImage(image=Image.fromarray( self.shape_photo_blank),master=self.top)
        self.shape_label.configure(image=self.photo_for_label)

        # print("hello from show circle")
    def show_rectangle(self, event):
        self.rectangle_radioButton.select()
        self.shape_photo_blank = np.zeros((240,320))
        self.shape_photo_blank = cv2.rectangle(self.shape_photo_blank, (50, 50),(50+self.var_width.get(),50+self.var_height.get()), (255, 255,255),-1)
        # self.photo_for_label
        self.photo_for_label = ImageTk.PhotoImage(image=Image.fromarray(self.shape_photo_blank), master=self.top)

        self.shape_label.configure(image=self.photo_for_label)

    def save(self):

        my_top = alarm_db_gui.Alarm_Gui(self.top,self.selected_pyimage_file,self.selected_file_date)
# todo save into the db!


if __name__ == "__main__":
    window = Tk()
    image_enlargement = 4
    selected_file_date = "images/lep_2021_04_12_T_17_29_01__430.png"
    selected_pyimage_file = "images/cam_2021_04_12_T_17_29_01__694182.jpg"
    start3 = Measure_temperature(window,selected_file_date,
                                                         (160 * image_enlargement, 120 * image_enlargement),selected_pyimage_file)
    window.mainloop()