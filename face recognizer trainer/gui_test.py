from tkinter import *
from PIL import Image, ImageTk
import cv2
import numpy as np


#Colors(https://color.adobe.com/trends/Travel):
blue_bg = '#3c3f41'
orange = '#F25C05'
green_green = '#7ABF11'
yellow = '#F29F05'
creme = '#F28705'
red = '#F24405'
thermal_image_size = (300,200)


window = Tk()
window.title("Template Matching")
window.config(padx=100, pady=150, bg=blue_bg)


def apply_mask1(self):
    global photo
    print(str(scale.get()))
    hsv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2HSV)[:, :, 2]
    blurredBrightness = cv2.bilateralFilter(hsv_img, 9, 150, 150)
    thresh = 50
    edges = cv2.Canny(blurredBrightness,thresh,thresh*2, L2gradient=True)
    # scale.get was 200!
    _,mask = cv2.threshold(blurredBrightness,scale.get(),1,cv2.THRESH_BINARY)
    print(mask.shape)

    # print(photo)
    erodeSize = 5
    dilateSize = 7
    eroded = cv2.erode(mask, np.ones((erodeSize, erodeSize)))
    mask = cv2.dilate(eroded, np.ones((dilateSize, dilateSize)))
    cv2.imshow("preview", cv2.resize(cv2.cvtColor(mask * edges, cv2.COLOR_GRAY2RGB) | cv_img, thermal_image_size,
                                     interpolation=cv2.INTER_CUBIC))
    my_photo =cv2.resize(cv2.cvtColor(mask * edges, cv2.COLOR_GRAY2RGB) | cv_img, thermal_image_size,
                                     interpolation=cv2.INTER_CUBIC)
    # photo = cv2.cvtColor(mask * edges, cv2.COLOR_GRAY2RGB)   | cv_img
    photo = ImageTk.PhotoImage(image=Image.fromarray(my_photo))

    my_label.configure(image=photo)



#Image
cv_img = cv2.cvtColor(cv2.imread("2021_02_08_T_20_54_25__812.png"), cv2.COLOR_BGR2RGB)
cv_img = cv2.resize(cv_img, thermal_image_size)

photo = ImageTk.PhotoImage(image = Image.fromarray(cv_img))

# my_img = ImageTk.PhotoImage(Image.fromarray(cv_img))
my_label = Label(image=photo)
my_img2 = ImageTk.PhotoImage(Image.open("Maria.png"))
my_label.grid(row=0,column=0)

#apply Button
start_button = Button(text="Apply Mask", highlightthickness=0)
start_button.grid(row=1, column=1)

#scale
v = DoubleVar()
scale = Scale( window, variable = v, from_ = 1, to = 400, orient = HORIZONTAL,command=apply_mask1)
scale.grid(row=0,column=1)



window.mainloop()
