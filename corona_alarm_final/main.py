
# Example of embedding CEF Python browser using Tkinter toolkit.
# This example has two widgets: a navigation bar and a browser.
#
# NOTE: This example often crashes on Mac (Python 2.7, Tk 8.5/8.6)
#       during initial app loading with such message:
#       "Segmentation fault: 11". Reported as Issue #309.
#
# Tested configurations:
# - Tk 8.5 on Windows/Mac
# - Tk 8.6 on Linux
# - CEF Python v55.3+
#
# Known issue on Linux: When typing url, mouse must be over url
# entry widget otherwise keyboard focus is lost (Issue #255
# and Issue #284).
# Other focus issues discussed in Issue #535.

# GUI map!
import threading
from cefpython3 import cefpython as cef
import ctypes
import alarm_server
import person_db_gui
import alarm_db_gui
import corona_alarm
import load_polygon
# import runpy
import server_gps
import file_server
import email_server
import import_yellow_geojason
import import_red_geojason

import folium
# import pygeoj # for the
import sys

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import sys
import os
import platform
import logging as _logging

# Fix for PyCharm hints warnings
WindowUtils = cef.WindowUtils()

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Globals
logger = _logging.getLogger("tkinter_.py")

# Constants
# Tk 8.5 doesn't support png images
IMAGE_EXT = ".png" if tk.TkVersion > 8.5 else ".gif"

# this function generates the index.html for the first use in main method. There is an other inside the class to relaod the page!
def generate_index_html_file(map,yellow_geojason, red_geojason):
    # runpy.run_path(path_name=path_to_html_generator_load_polygon_py,run_name="__main__")
    # load_polygon.Load_ploygon()
    x = load_polygon.Load_ploygon(map,yellow_geojason, red_geojason)
    x.load_geo_pol()
    x.load_iframes()
    x.add_to_map() # just gui the only the polygons!
    x.generate_index_html_marker_polygon("index.html")

def main():
    map_style = "OpenStreetMap"
    my_map = folium.Map(location=[48.204131, 16.373765],tiles=map_style, zoom_start=13)#  48.204131, 16.373765
    # my_map = folium.Map(location=[48.208176, 16.373819], tiles="Stamen Terrain", zoom_start=15)
    # my_map = folium.Map(location=[48.208176, 16.373819], tiles="Stamen Toner", zoom_start=15)
    # my_map = folium.Map(location=[48.208176, 16.373819], tiles="cartodbpositron", zoom_start=15)
    # my_map = folium.Map(location=[48.208176, 16.373819], tiles="Mapbox", zoom_start=15)

    generate_index_html_file(my_map, "polygon_geojason/yellow.geojson", "polygon_geojason/red.geojason")
    logger.setLevel(_logging.DEBUG)
    stream_handler = _logging.StreamHandler()
    formatter = _logging.Formatter("[%(filename)s] %(message)s")
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.info("CEF Python {ver}".format(ver=cef.__version__))
    logger.info("Python {ver} {arch}".format(
        ver=platform.python_version(), arch=platform.architecture()[0]))
    logger.info("Tk {ver}".format(ver=tk.Tcl().eval('info patchlevel')))
    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    # Tk must be initialized before CEF otherwise fatal error (Issue #306)
    root = tk.Tk()
    app = MainFrame(root, map_style)
    settings = {}
    if MAC:
        settings["external_message_pump"] = True
    cef.Initialize(settings=settings)
    #try
    # main_alarm_server = alarm_server.Alarm_server("127.0.0.1", 20001, app)
    app.mainloop()
    logger.debug("Main loop exited")
    cef.Shutdown()


class MainFrame(tk.Frame):

    def __init__(self, root, map_style):
        # map from the main method:
        self.map_style = map_style
        self.browser_frame = None
        self.navigation_bar = None
        self.root = root
        # I need the thread inside this list!
        self.threads = []

        # Root
        root.geometry("900x640")
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)
        #set it in full screen:
        root.state('zoomed')

        menubar = tk.Menu(root)
        corona_service_menue = tk.Menu(menubar, tearoff=0)
        corona_service_menue.add_command(label="Alarm Manager", command=self.alarm_navigator_start)
        corona_service_menue.add_command(label="Person Navigator", command=self.person_navigator_start)
        corona_service_menue.add_command(label="Temperature Navigator", command=self.temperature_navigator_start)
        corona_service_menue.add_command(label="Lepton Navigator", command=self.lepton_navigator_start)
        corona_service_menue.add_separator()

        corona_service_menue.add_command(label="Exit", command=self.close)
        # filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="Corona Services", menu=corona_service_menue)

        map_menue = tk.Menu(menubar, tearoff=0)

        # map_menue.add_command(label="Map Style")
        # submenue of map style!
        openstreet_style_submenue = tk.Menu(map_menue)
        openstreet_style_submenue.add_command(label="OpenStreetMap", command=self.opensteetmap_style)
        openstreet_style_submenue.add_command(label="Stamen Terrain", command=self.stamen_terrain_style)
        openstreet_style_submenue.add_command(label="Stamen Toner", command=self.stamen_toner_style)
        openstreet_style_submenue.add_command(label="Cartodbpositron", command=self.cartodbpositron_style)
        map_menue.add_cascade(label='Map Style', menu=openstreet_style_submenue)


        map_menue.add_command(label="Red Zone", command=self.input_red_geojason)
        map_menue.add_command(label="Yellow Zone", command=self.input_yellow_geojason)
        map_menue.add_command(label="Reload Map", command=self.reload)

        menubar.add_cascade(label="Map", menu=map_menue)

        servermenu = tk.Menu(menubar, tearoff=0)
        gps_submenue = tk.Menu(servermenu)
        gps_submenue.add_command(label="Start", command=self.start_gps_server)
        gps_submenue.add_command(label="Stop", command=self.stop_gps_server)
        servermenu.add_cascade(label='GPS Server', menu=gps_submenue)


        email_submenue = tk.Menu(servermenu)
        email_submenue.add_command(label="Start", command=self.start_email_server)
        email_submenue.add_command(label="Stop", command=self.stop_email_server)
        servermenu.add_cascade(label='Email Server', menu=email_submenue)

        alarm_submenue = tk.Menu(servermenu)
        alarm_submenue.add_command(label="Start", command=self.start_alarm_server)
        alarm_submenue.add_command(label="Stop", command=self.stop_alarm_server)
        servermenu.add_cascade(label='Alarm Server', menu=alarm_submenue)

        file_server_submenue = tk.Menu(servermenu)
        file_server_submenue.add_command(label="Start", command=self.start_file_server)
        file_server_submenue.add_command(label="Stop", command=self.stop_file_server)
        servermenu.add_cascade(label='File Server', menu=file_server_submenue)
        menubar.add_cascade(label="Server", menu=servermenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index")
        helpmenu.add_command(label="About...")
        menubar.add_cascade(label="Help", menu=helpmenu)

        root.config(menu=menubar)
        # MainFrame
        tk.Frame.__init__(self, root)
        self.master.title("Corona Alarm")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.bind("<Configure>", self.on_root_configure)
        self.setup_icon()
        self.bind("<Configure>", self.on_configure)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        # NavigationBar
        # self.navigation_bar = NavigationBar(self)
        # self.navigation_bar.grid(row=0, column=0,
        #                          sticky=(tk.N + tk.S + tk.E + tk.W))
        # tk.Grid.rowconfigure(self, 0, weight=0)
        # tk.Grid.columnconfigure(self, 0, weight=0)

        # BrowserFrame
        self.browser_frame = BrowserFrame(self, self.navigation_bar)
        self.browser_frame.grid(row=1, column=0,
                                sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)

        self.start_servers()

        # Pack MainFrame
        self.pack(fill=tk.BOTH, expand=tk.YES)

    # my_map = folium.Map(location=[48.208176, 16.373819],tiles="OpenStreetMap", zoom_start=15)
    # my_map = folium.Map(location=[48.208176, 16.373819], tiles="Stamen Terrain", zoom_start=15)
    # my_map = folium.Map(location=[48.208176, 16.373819], tiles="Stamen Toner", zoom_start=15)
    # my_map = folium.Map(location=[48.208176, 16.373819], tiles="cartodbpositron", zoom_start=15)
    # my_map = folium.Map(location=[48.208176, 16.373819], tiles="Mapbox", zoom_start=15)

    # openstreet_style_submenue.add_command(label="OpenStreetMap", command=self.opensteetmap_style)
    # openstreet_style_submenue.add_command(label="Stamen Terrain", command=self.stamen_terrain_style)
    # openstreet_style_submenue.add_command(label="Stamen Toner", command=self.stamen_toner_style)
    # openstreet_style_submenue.add_command(label="Cartodbpositron", command=self.cartodbpositron_style)
    # openstreet_style_submenue.add_command(label="Mapbox", command=self.mapbox_style)

    def reload(self):
        # self.reload
        # self.on_load_url()
        # self.embed_browser()
        self.generate_index_html_file( "polygon_geojason/yellow.geojson", "polygon_geojason/red.geojason")
        self.get_browser().Reload()


    def opensteetmap_style(self):
        self.map_style = "OpenStreetMap"

    def stamen_terrain_style(self):
        self.map_style = "Stamen Terrain"

    def stamen_toner_style(self):
        self.map_style = "Stamen Toner"

    def cartodbpositron_style(self):
        self.map_style = "cartodbpositron"



    def generate_index_html_file(self, yellow_geojason, red_geojason):
        # runpy.run_path(path_name=path_to_html_generator_load_polygon_py,run_name="__main__")
        # load_polygon.Load_ploygon()
        new_map = folium.Map(location=[48.204131, 16.373765], tiles=self.map_style, zoom_start=13)
        x = load_polygon.Load_ploygon(new_map, yellow_geojason, red_geojason)
        x.load_geo_pol()
        x.load_iframes()
        x.add_to_map()  # just gui the only the polygons!
        x.generate_index_html_marker_polygon("index.html")

    def start_servers(self):
        # run the server and the alarm manager! it runs the alarms server from itself! it runs file server too!
        self.main_alarm_server = alarm_server.Alarm_server("127.0.0.1", 20001,5001, self.root)# "127.0.0.1", 20001
        # add alarm server to the thread array!
        self.threads.append(self.main_alarm_server.alarm_server_thread)
        # add file server to the thread array!
        self.threads.append(self.main_alarm_server.file_server_thread)

        # GPS SERVER
        self.gps_server = server_gps.Server_gps("127.0.0.1", 9999,1000)
        # self.gps_server.run_listen()
        self.gps_server_thread = threading.Thread(target=self.gps_server.run_listen)
        self.gps_server_thread.setDaemon(True)
        # add to the thread array!
        self.threads.append(self.gps_server_thread)
        self.gps_server_thread.start()

        # Email SERVER
        self.email_server = email_server.Email_server("127.0.0.1", 7897)
        # self.gps_server.run_listen()
        self.email_server_thread = threading.Thread(target=self.email_server.run_listen)
        self.email_server_thread.setDaemon(True)
        # add to the thread array!
        self.threads.append(self.email_server_thread)
        self.email_server_thread.start()



        # FILE SERVER
        # self.windows_file_server = file_server.File_server_windows("127.0.0.1", 5001)
        # # self.windows_file_server.run_server()
        # self.windows_file_server_thread = threading.Thread(target=self.windows_file_server.run_server)
        # # add to the thread array!
        # self.threads.append(self.windows_file_server_thread)
        # self.windows_file_server_thread.start()

    # import the red geojason gui
    def input_red_geojason(self):
        import_red_geojason.Input_red_geojason(self.root)

    # import the red geojason gui
    def input_yellow_geojason(self):
        import_yellow_geojason.Input_yellow_geojason(self.root)

    def start_gps_server(self):
        if self.gps_server == None:
            # GPS SERVER
            self.gps_server = server_gps.Server_gps("127.0.0.1", 9999,1000)
            # self.gps_server.run_listen()
            self.gps_server_thread = threading.Thread(target=self.gps_server.run_listen)
            self.gps_server_thread.setDaemon(True)
            # add to the thread array!
            self.threads.append(self.gps_server_thread)
            self.gps_server_thread.start()
            print("Gps server is running")

    def stop_gps_server(self):
        if self.gps_server != None:
            self.gps_server.continue_server = False
            # self.gps_server_thread.join()
            # print(self.gps_server)

    def start_email_server(self):
        if self.email_server == None:
            # GPS SERVER
            self.email_server = email_server.Email_server("127.0.0.1", 7897)
            # self.gps_server.run_listen()
            self.email_server_thread = threading.Thread(target=self.email_server.run_listen)
            self.email_server_thread.setDaemon(True)
            # add to the thread array!
            self.threads.append(self.email_server_thread)
            self.email_server_thread.start()
            print("Gps server is running")

    def stop_email_server(self):
        if self.email_server != None:
            self.email_server.continue_server = False

    def start_alarm_server(self):
        if self.main_alarm_server == None:
            # GPS SERVER
            self.main_alarm_server = alarm_server.Alarm_server("127.0.0.1", 20001, 5001,
                                                               self.root)  # "127.0.0.1", 20001

            # self.gps_server.run_listen()
            self.main_alarm_server_thread_from_menue = threading.Thread(target=self.main_alarm_server.run_listen)
            self.main_alarm_server_thread_from_menue.setDaemon(True)
            # add to the thread array!
            self.threads.append(self.main_alarm_server_thread_from_menue)
            self.main_alarm_server_thread_from_menue.start()
            print("Gps server is running")

    def stop_alarm_server(self):
        if self.main_alarm_server_thread_from_menue != None or self.main_alarm_server != None:
            self.main_alarm_server.continue_server = False

    def start_file_server(self):
        if self.main_alarm_server.new_file_server != None:
            self.main_file_server = file_server.File_server_windows("127.0.0.1", 5001)
            # self.gps_server.run_listen()
            self.main_file_server_thread_from_menue = threading.Thread(target=self.main_file_server.run_listen)
            self.main_file_server_thread_from_menue.setDaemon(True)
            # add to the thread array!
            self.threads.append(self.main_file_server_thread_from_menue)
            self.main_file_server_thread_from_menue.start()

            self.main_file_server.run_server()

    def stop_file_server(self):
        if self.main_alarm_server.new_file_server != None:
            self.main_alarm_server.new_file_server.continue_server = False

    def close(self):# todo: how to exit carefully? ask prof.Kerer
        # stop the servers!
        self.gps_server.continue_server = False
        self.email_server.continue_server = False
        self.main_alarm_server.continue_server = False
        self.main_alarm_server.new_file_server.continue_server = False
        # stop the threads!
        # if len(self.threads)!=0:
        #     for thread in self.threads:
        #         thread.join()
        self.root.quit()
        exit(0)


    def lepton_navigator_start(self):
        self.main_alarm_server.new_file_server.image_folder = "alarm_images/default"
        corona_alarm.Corona_alarm("alarm_images/default",
                                  "Welcome to Lepton Navigator!\nHere you can select a date and time and download the cooresponding images from the user raspberry pi!",
                                  self.root)



    def temperature_navigator_start(self):
        alarm_db_gui.Alarm_Gui(self.root)


    def person_navigator_start(self):
        person_db_gui.Person_gui(0,self.root)


    def alarm_navigator_start(self):
        self.main_alarm_server = alarm_server.Alarm_server("127.0.0.1", 20001, 5001, self.root)  # "127.0.0.1", 20001


        # self.alarm_navigator_from_main = threading.Thread(target=self.run_alarm_server)
        # self.threads.append(self.alarm_navigator_from_main)
        # self.alarm_navigator_from_main.setDaemon(True)
        # self.alarm_navigator_from_main.start()



    def on_root_configure(self, _):
        logger.debug("MainFrame.on_root_configure")
        if self.browser_frame:
            self.browser_frame.on_root_configure()

    def on_configure(self, event):
        logger.debug("MainFrame.on_configure")
        if self.browser_frame:
            width = event.width
            height = event.height
            if self.navigation_bar:
                height = height - self.navigation_bar.winfo_height()
            self.browser_frame.on_mainframe_configure(width, height)

    def on_focus_in(self, _):
        logger.debug("MainFrame.on_focus_in")

    def on_focus_out(self, _):
        logger.debug("MainFrame.on_focus_out")

    def on_close(self):
        if self.browser_frame:
            self.browser_frame.on_root_close()
            self.browser_frame = None
        else:
            self.master.destroy()

    def get_browser(self):
        if self.browser_frame:
            return self.browser_frame.browser
        return None

    def get_browser_frame(self):
        if self.browser_frame:
            return self.browser_frame
        return None

    def setup_icon(self):
        resources = os.path.join(os.path.dirname(__file__), "resources")
        icon_path = os.path.join(resources, "tkinter" + IMAGE_EXT)
        if os.path.exists(icon_path):
            self.icon = tk.PhotoImage(file=icon_path)
            # noinspection PyProtectedMember
            self.master.call("wm", "iconphoto", self.master._w, self.icon)


class BrowserFrame(tk.Frame):

    def __init__(self, mainframe, navigation_bar=None):
        self.navigation_bar = navigation_bar
        self.closing = False
        self.browser = None
        tk.Frame.__init__(self, mainframe)
        self.mainframe = mainframe
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Configure>", self.on_configure)
        """For focus problems see Issue #255 and Issue #535. """
        self.focus_set()

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info,
                                             url="file:///C:/Users/Jack/PycharmProjects/corona_alarm_final/corona_alarm_final/index.html")
        # self.browser = cef.CreateBrowserSync(window_info,
        #                                      url="file:///C:/Users/Jack/PycharmProjects/file_server/final_v7/corona_alarm_final/index.html")
        assert self.browser
        self.browser.SetClientHandler(LifespanHandler(self))
        self.browser.SetClientHandler(LoadHandler(self))
        self.browser.SetClientHandler(FocusHandler(self))
        self.message_loop_work()

    def get_window_handle(self):
        if MAC:
            # Do not use self.winfo_id() on Mac, because of these issues:
            # 1. Window id sometimes has an invalid negative value (Issue #308).
            # 2. Even with valid window id it crashes during the call to NSView.setAutoresizingMask:
            #    https://github.com/cztomczak/cefpython/issues/309#issuecomment-661094466
            #
            # To fix it using PyObjC package to obtain window handle. If you change structure of windows then you
            # need to do modifications here as well.
            #
            # There is still one issue with this solution. Sometimes there is more than one window, for example when application
            # didn't close cleanly last time Python displays an NSAlert window asking whether to Reopen that window. In such
            # case app will crash and you will see in console:
            # > Fatal Python error: PyEval_RestoreThread: NULL tstate
            # > zsh: abort      python tkinter_.py
            # Error messages related to this: https://github.com/cztomczak/cefpython/issues/441
            #
            # There is yet another issue that might be related as well:
            # https://github.com/cztomczak/cefpython/issues/583

            # noinspection PyUnresolvedReferences
            from AppKit import NSApp
            # noinspection PyUnresolvedReferences
            import objc
            logger.info("winfo_id={}".format(self.winfo_id()))
            # noinspection PyUnresolvedReferences
            content_view = objc.pyobjc_id(NSApp.windows()[-1].contentView())
            logger.info("content_view={}".format(content_view))
            return content_view
        elif self.winfo_id() > 0:
            return self.winfo_id()
        else:
            raise Exception("Couldn't obtain window handle")

    def message_loop_work(self):
        cef.MessageLoopWork()
        self.after(10, self.message_loop_work)

    def on_configure(self, _):
        if not self.browser:
            self.embed_browser()

    def on_root_configure(self):
        # Root <Configure> event will be called when top window is moved
        if self.browser:
            self.browser.NotifyMoveOrResizeStarted()

    def on_mainframe_configure(self, width, height):
        if self.browser:
            if WINDOWS:
                ctypes.windll.user32.SetWindowPos(
                    self.browser.GetWindowHandle(), 0,
                    0, 0, width, height, 0x0002)
            elif LINUX:
                self.browser.SetBounds(0, 0, width, height)
            self.browser.NotifyMoveOrResizeStarted()

    def on_focus_in(self, _):
        logger.debug("BrowserFrame.on_focus_in")
        if self.browser:
            self.browser.SetFocus(True)

    def on_focus_out(self, _):
        logger.debug("BrowserFrame.on_focus_out")
        """For focus problems see Issue #255 and Issue #535. """
        if LINUX and self.browser:
            self.browser.SetFocus(False)

    def on_root_close(self):
        logger.info("BrowserFrame.on_root_close")
        if self.browser:
            logger.debug("CloseBrowser")
            self.browser.CloseBrowser(True)
            self.clear_browser_references()
        else:
            logger.debug("tk.Frame.destroy")
            self.destroy()

    def clear_browser_references(self):
        # Clear browser references that you keep anywhere in your
        # code. All references must be cleared for CEF to shutdown cleanly.
        self.browser = None


class LifespanHandler(object):

    def __init__(self, tkFrame):
        self.tkFrame = tkFrame

    def OnBeforeClose(self, browser, **_):
        logger.debug("LifespanHandler.OnBeforeClose")
        self.tkFrame.quit()


class LoadHandler(object):

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnLoadStart(self, browser, **_):
        if self.browser_frame.master.navigation_bar:
            self.browser_frame.master.navigation_bar.set_url(browser.GetUrl())


class FocusHandler(object):
    """For focus problems see Issue #255 and Issue #535. """

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnTakeFocus(self, next_component, **_):
        logger.debug("FocusHandler.OnTakeFocus, next={next}"
                     .format(next=next_component))

    def OnSetFocus(self, source, **_):
        logger.debug("FocusHandler.OnSetFocus, source={source}"
                     .format(source=source))
        if LINUX:
            return False
        else:
            return True

    def OnGotFocus(self, **_):
        logger.debug("FocusHandler.OnGotFocus")
        if LINUX:
            self.browser_frame.focus_set()


class NavigationBar(tk.Frame):

    def __init__(self, master):
        self.back_state = tk.NONE
        self.forward_state = tk.NONE
        self.back_image = None
        self.forward_image = None
        self.reload_image = None

        tk.Frame.__init__(self, master)
        resources = os.path.join(os.path.dirname(__file__), "resources")

        # Back button
        back_png = os.path.join(resources, "back" + IMAGE_EXT)
        if os.path.exists(back_png):
            self.back_image = tk.PhotoImage(file=back_png)
        self.back_button = tk.Button(self, image=self.back_image,
                                     command=self.go_back)
        self.back_button.grid(row=0, column=0)

        # Forward button
        forward_png = os.path.join(resources, "forward" + IMAGE_EXT)
        if os.path.exists(forward_png):
            self.forward_image = tk.PhotoImage(file=forward_png)
        self.forward_button = tk.Button(self, image=self.forward_image,
                                        command=self.go_forward)
        self.forward_button.grid(row=0, column=1)

        # Reload button
        reload_png = os.path.join(resources, "reload" + IMAGE_EXT)
        if os.path.exists(reload_png):
            self.reload_image = tk.PhotoImage(file=reload_png)
        self.reload_button = tk.Button(self, image=self.reload_image,
                                       command=self.reload)
        self.reload_button.grid(row=0, column=2)

        # Url entry
        self.url_entry = tk.Entry(self)
        self.url_entry.bind("<FocusIn>", self.on_url_focus_in)
        self.url_entry.bind("<FocusOut>", self.on_url_focus_out)
        self.url_entry.bind("<Return>", self.on_load_url)
        self.url_entry.bind("<Button-1>", self.on_button1)
        self.url_entry.grid(row=0, column=3,
                            sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 0, weight=100)
        tk.Grid.columnconfigure(self, 3, weight=100)

        # Update state of buttons
        self.update_state()

    def go_back(self):
        if self.master.get_browser():
            self.master.get_browser().GoBack()

    def go_forward(self):
        if self.master.get_browser():
            self.master.get_browser().GoForward()
# TODO: change it to reload the project with each new row of data in database
    def reload(self):
        if self.master.get_browser():
            self.master.get_browser().Reload()

    def set_url(self, url):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)

    def on_url_focus_in(self, _):
        logger.debug("NavigationBar.on_url_focus_in")

    def on_url_focus_out(self, _):
        logger.debug("NavigationBar.on_url_focus_out")

    def on_load_url(self, _):
        if self.master.get_browser():
            self.master.get_browser().StopLoad()
            self.master.get_browser().LoadUrl(self.url_entry.get())

    def on_button1(self, _):
        """For focus problems see Issue #255 and Issue #535. """
        logger.debug("NavigationBar.on_button1")
        self.master.master.focus_force()

    def update_state(self):
        browser = self.master.get_browser()
        if not browser:
            if self.back_state != tk.DISABLED:
                self.back_button.config(state=tk.DISABLED)
                self.back_state = tk.DISABLED
            if self.forward_state != tk.DISABLED:
                self.forward_button.config(state=tk.DISABLED)
                self.forward_state = tk.DISABLED
            self.after(100, self.update_state)
            return
        if browser.CanGoBack():
            if self.back_state != tk.NORMAL:
                self.back_button.config(state=tk.NORMAL)
                self.back_state = tk.NORMAL
        else:
            if self.back_state != tk.DISABLED:
                self.back_button.config(state=tk.DISABLED)
                self.back_state = tk.DISABLED
        if browser.CanGoForward():
            if self.forward_state != tk.NORMAL:
                self.forward_button.config(state=tk.NORMAL)
                self.forward_state = tk.NORMAL
        else:
            if self.forward_state != tk.DISABLED:
                self.forward_button.config(state=tk.DISABLED)
                self.forward_state = tk.DISABLED
        self.after(100, self.update_state)


class Tabs(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        # TODO: implement tabs


if __name__ == '__main__':
    main()