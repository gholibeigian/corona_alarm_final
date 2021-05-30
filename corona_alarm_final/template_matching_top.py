import locale

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import cv2
from PIL import ImageTk, Image
import matplotlib.pyplot as plt


class Template_matching:
    def __init__(self,window ,selected_file_date):
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform
        self.top = window
        print(selected_file_date)
        self.top2 = Toplevel(self.top)
        self.top2.lift()
        self.top2.title = "Featuer Matching" # ask Dr. Kerrer
        self.face_address = filedialog.askopenfilename(parent=self.top,initialdir=".", title="Select the face photo"
                                                  , filetypes=(
            ("png files", "*.png"), ("jpg files", "*.jpg"), ("all files", "*.*")))
        self.start_button = Button(self.top2, text="Show Details", highlightthickness=0, command=self.show_plot)
        self.start_button.grid(row=2, column=1)

        # # file_name = face_loader()
        # self.start_button = Button(text="Apply Mask", highlightthickness=0)
        # self.start_button.grid(row=3, column=1)

        self.cv_img = cv2.cvtColor(cv2.imread(selected_file_date), cv2.COLOR_BGR2RGB)
        img_cv2_TM_CCOEFF, mapped_img = self.template_matching('cv2.TM_CCOEFF')

        img_TM_CCOEFF = ImageTk.PhotoImage(image=Image.fromarray(img_cv2_TM_CCOEFF))
        my_label = Label(self.top2, image=img_TM_CCOEFF)
        my_label.grid(row=0, column=0)

        plt.subplot(2, 3, 1)

        plt.imshow(mapped_img)
        plt.title('TM_CCOEFF')

        ##2
        img_cv2_TM_CCOEFF, mapped_img = self.template_matching('cv2.TM_CCOEFF_NORMED')

        img_CCOEFF = ImageTk.PhotoImage(image=Image.fromarray(img_cv2_TM_CCOEFF))
        my_label2 = Label(self.top2,image=img_CCOEFF)
        my_label2.grid(row=0, column=1)
        plt.subplot(2, 3, 2)

        plt.imshow(mapped_img)
        plt.title('TM_CCOEFF_NORMED')

        ##3
        img_cv2_TM_CCORR, mapped_img = self.template_matching('cv2.TM_CCORR')

        img_TM_CCORR = ImageTk.PhotoImage(image=Image.fromarray(img_cv2_TM_CCORR))
        my_label3 = Label(self.top2,image=img_TM_CCORR)
        my_label3.grid(row=0, column=2)
        plt.subplot(2, 3, 3)

        plt.imshow(mapped_img)
        plt.title('TM_CCORR')

        ##4
        img_cv2_TM_CCORR_NORMED, mapped_img = self.template_matching('cv2.TM_CCORR_NORMED')

        img_TM_CCORR_NORMED = ImageTk.PhotoImage(image=Image.fromarray(img_cv2_TM_CCORR_NORMED))
        my_label4 = Label(self.top2,image=img_TM_CCORR_NORMED)
        my_label4.grid(row=1, column=0)
        plt.subplot(2, 3, 4)

        plt.imshow(mapped_img)
        plt.title('TM_CCORR_NORMED')
        ##5
        img_cv2_TM_SQDIFF, mapped_img = self.template_matching('cv2.TM_SQDIFF')

        img_TM_SQDIFF = ImageTk.PhotoImage(image=Image.fromarray(img_cv2_TM_SQDIFF))
        my_label5 = Label(self.top2,image=img_TM_SQDIFF)
        my_label5.grid(row=1, column=1)
        plt.subplot(2, 3, 5)

        plt.imshow(mapped_img)
        plt.title('TM_SQDIFF')
        ##6
        img_cv2_TM_SQDIFF_NORMED, mapped_img = self.template_matching('cv2.TM_SQDIFF_NORMED')

        img_TM_SQDIFF_NORMED = ImageTk.PhotoImage(image=Image.fromarray(img_cv2_TM_SQDIFF_NORMED))
        my_label6 = Label(self.top2,image=img_TM_SQDIFF_NORMED)
        my_label6.grid(row=1, column=2)
        plt.subplot(2, 3, 6)
        plt.imshow(mapped_img)
        plt.title('TM_SQDIFF_NORMED')
        self.top2.lift()
        self.top2.mainloop()

    def template_matching(self,m):
        # global self.face_address
#            print(self.face_address)
        face = cv2.cvtColor(cv2.imread(self.face_address), cv2.COLOR_BGR2RGB)
        # face = ImageTk.PhotoImage(image=Image.fromarray(face))

        full_copy = self.cv_img.copy()
        method = eval(m)

        res = cv2.matchTemplate(full_copy, face, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        height, width, channels = face.shape
        bottom_right = (top_left[0] + width, top_left[1] + height)
        # cv2.rectangle(full_copy, top_left, bottom_right, (255,0,0), 10)
        my_photo = cv2.rectangle(full_copy, top_left, bottom_right, (0, 0, 255), 1)

        # my_img2 = ImageTk.PhotoImage(image=Image.fromarray(res))

        return my_photo, res


    def show_plot(self, *args):
        plt.show()




