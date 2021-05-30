import locale

from selenium import webdriver
import tkinter
from tkinter import *

class Input_yellow_geojason:
    def __init__(self, master_window):
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform

        self.top = Toplevel(background='#3c3f41', master=master_window)
        self.top.lift()

        lila = '#3c3f41'
        blue_gray= '#3E434C'
        blue = '#4B6EAF'

        # self.text_box =
        # root = tk.Tk()
        self.text = Text(self.top)
        save_button = Button(self.top, text ="Save",padx = "20px", command=self.save)#, command = search_db)
        cancel_button = Button(self.top, text ="Cancel",padx = "20px", command=self.cancel)#, command = search_db)
        graphic_map_button = Button(self.top, text ="Graphical Map",padx = "20px", command=self.open_selenium)#, command = search_db)

        self.text.pack()
        save_button.pack(side=RIGHT)
        cancel_button.pack(side=LEFT)
        graphic_map_button.pack(side=TOP)


        self.load_yellow_geojason()
        # side = tk.LEFT
        # root.mainloop()

    def load_yellow_geojason(self):
        with open('polygon_geojason/yellow.geojson', 'r') as reader:
            # self.text.()
            self.geojason = reader.read()
            self.text.delete(1.0, END)
            self.text.insert(END, self.geojason)

    def open_selenium(self):
        selenium_drive_chrome_path = "polygon_geojason/chrome_driver/chromedriver.exe"
        driver = webdriver.Chrome(selenium_drive_chrome_path)

        driver.get("http://geojson.io/#map=2/21.8/-4.2")

    def save(self):
        with open('polygon_geojason/yellow.geojson', 'w') as writer:
            writer.write(self.text.get("1.0","end-1c").strip())
        self.top.destroy()
        self.top.update()
    # Further file processing goes here

    def cancel(self):
        self.top.destroy()
        self.top.update()

if __name__ == "__main__":
    win = Tk()
    Input_yellow_geojason(win)
    win.mainloop()
