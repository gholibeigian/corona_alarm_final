import locale


import tkinter as tk
import threading
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
import inspect

import folium
# Example of embedding CEF Python browser using wxPython library.
# This example has a top menu and a browser widget without navigation bar.

# Tested configurations:
# - wxPython 4.0 on Windows/Mac/Linux
# - wxPython 3.0 on Windows/Mac
# - wxPython 2.8 on Linux
# - CEF Python v66.0+

import wx
from cefpython3 import cefpython as cef
import platform
import sys
import os

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

if MAC:
    try:
        # noinspection PyUnresolvedReferences
        from AppKit import NSApp
    except ImportError:
        print("[wxpython.py] Error: PyObjC package is missing, "
              "cannot fix Issue #371")
        print("[wxpython.py] To install PyObjC type: "
              "pip install -U pyobjc")
        sys.exit(1)

# Configuration
WIDTH = 900
HEIGHT = 640


# Globals
g_count_windows = 0


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
    # fix to exception with wxPython 4.1.1:
    locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform
    locale.getlocale(locale.LC_TIME)

    # load the map
    map_style = "OpenStreetMap"
    my_map = folium.Map(location=[48.204131, 16.373765],tiles=map_style, zoom_start=13)#  48.204131, 16.373765
    # my_map = folium.Map(location=[48.208176, 16.373819], tiles="Stamen Terrain", zoom_start=15)
    # my_map = folium.Map(location=[48.208176, 16.373819], tiles="Stamen Toner", zoom_start=15)
    # my_map = folium.Map(location=[48.208176, 16.373819], tiles="cartodbpositron", zoom_start=15)
    # my_map = folium.Map(location=[48.208176, 16.373819], tiles="Mapbox", zoom_start=15)

    generate_index_html_file(my_map, "polygon_geojason/yellow.geojson", "polygon_geojason/red.geojason")


    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    settings = {}
    if MAC:
        # Issue #442 requires enabling message pump on Mac
        # and calling message loop work in a timer both at
        # the same time. This is an incorrect approach
        # and only a temporary fix.
        settings["external_message_pump"] = False
    if WINDOWS:
        # noinspection PyUnresolvedReferences, PyArgumentList
        cef.DpiAware.EnableHighDpiSupport()
    cef.Initialize(settings=settings)
    app = CefApp(False)
    app.MainLoop()
    del app  # Must destroy before calling Shutdown
    if not MAC:
        # On Mac shutdown is called in OnClose
        cef.Shutdown()


def check_versions():
    print("[wxpython.py] CEF Python {ver}".format(ver=cef.__version__))
    print("[wxpython.py] Python {ver} {arch}".format(
            ver=platform.python_version(), arch=platform.architecture()[0]))
    print("[wxpython.py] wxPython {ver}".format(ver=wx.version()))
    # CEF Python version requirement
    assert cef.__version__ >= "66.0", "CEF Python v66.0+ required to run this"


def scale_window_size_for_high_dpi(width, height):
    """Scale window size for high DPI devices. This func can be
    called on all operating systems, but scales only for Windows.
    If scaled value is bigger than the work area on the display
    then it will be reduced."""
    if not WINDOWS:
        return width, height
    (_, _, max_width, max_height) = wx.GetClientDisplayRect().Get()
    # noinspection PyUnresolvedReferences
    (width, height) = cef.DpiAware.Scale((width, height))
    if width > max_width:
        width = max_width
    if height > max_height:
        height = max_height
    return width, height


class MainFrame(wx.Frame):

    def __init__(self, map_style):
        # fix to exception with wxPython 4.1.1:
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform
        locale.getlocale(locale.LC_TIME)
        self.start_tk()
        self.browser = None
        # this is my code from here!
        self.map_style = map_style
        # I need the thread inside this list!
        self.threads = []


        # Must ignore X11 errors like 'BadWindow' and others by
        # installing X11 error handlers. This must be done after
        # wx was intialized.
        if LINUX:
            cef.WindowUtils.InstallX11ErrorHandlers()

        global g_count_windows
        g_count_windows += 1

        if WINDOWS:
            # noinspection PyUnresolvedReferences, PyArgumentList
            print("[wxpython.py] System DPI settings: %s"
                  % str(cef.DpiAware.GetSystemDpi()))
        if hasattr(wx, "GetDisplayPPI"):
            print("[wxpython.py] wx.GetDisplayPPI = %s" % wx.GetDisplayPPI())
        print("[wxpython.py] wx.GetDisplaySize = %s" % wx.GetDisplaySize())

        print("[wxpython.py] MainFrame declared size: %s"
              % str((WIDTH, HEIGHT)))
        size = scale_window_size_for_high_dpi(WIDTH, HEIGHT)
        print("[wxpython.py] MainFrame DPI scaled size: %s" % str(size))

        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY,
                          title='Corona Alarm', size=size)
        # set full screen
        # wx.Frame.ShowFullScreen(True)self.Maximize(True)
        self.Maximize(True)

        # wxPython will set a smaller size when it is bigger
        # than desktop size.
        print("[wxpython.py] MainFrame actual size: %s" % self.GetSize())

        self.setup_icon()
        self.create_menu()
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Set wx.WANTS_CHARS style for the keyboard to work.
        # This style also needs to be set for all parent controls.
        self.browser_panel = wx.Panel(self, style=wx.WANTS_CHARS)
        self.browser_panel.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.browser_panel.Bind(wx.EVT_SIZE, self.OnSize)

        # self.WindowU

        if MAC:
            # Make the content view for the window have a layer.
            # This will make all sub-views have layers. This is
            # necessary to ensure correct layer ordering of all
            # child views and their layers. This fixes Window
            # glitchiness during initial loading on Mac (Issue #371).
            NSApp.windows()[0].contentView().setWantsLayer_(True)

        if LINUX:
            # On Linux must show before embedding browser, so that handle
            # is available (Issue #347).
            self.Show()
            # In wxPython 3.0 and wxPython 4.0 on Linux handle is
            # still not yet available, so must delay embedding browser
            # (Issue #349).
            if wx.version().startswith("3.") or wx.version().startswith("4."):
                wx.CallLater(100, self.embed_browser)
            else:
                # This works fine in wxPython 2.8 on Linux
                self.embed_browser()
        else:
            self.embed_browser()
            self.Show()
        # start the servers
        # stack = inspect.stack()
        # self.caller_class = stack[1][0].f_locals["self"].__class__.__name__
        # the_method = stack[1][0].f_code.co_nameif ("{}.{}()".format(self.caller_class, the_method)!="MainFrame.reload()"):
        #
        self.start_servers()
        # else:
        #     check_versions()
        #     sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
        #     settings = {}
        #
        #     if WINDOWS:
        #         # noinspection PyUnresolvedReferences, PyArgumentList
        #         cef.DpiAware.EnableHighDpiSupport()
        #     cef.Initialize(settings=settings)

        #


    def setup_icon(self):
        icon_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 "resources", "wxpython.png")
        # wx.IconFromBitmap is not available on Linux in wxPython 3.0/4.0
        if os.path.exists(icon_file) and hasattr(wx, "IconFromBitmap"):
            icon = wx.IconFromBitmap(wx.Bitmap(icon_file, wx.BITMAP_TYPE_PNG))
            self.SetIcon(icon)

    def create_menu(self):
        # corona service menue
        corona_service_menue = wx.Menu()
        alarm_navigator_start = corona_service_menue.Append(1, "Alarm Manager")
        person_navigator_start = corona_service_menue.Append(2, "&Person Navigator")
        temperature_navigator_start = corona_service_menue.Append(3, "&Temperature Navigator")
        lepton_navigator_start = corona_service_menue.Append(4, "&Lepton Navigator")
        exit_function = corona_service_menue.Append(5, "&Exit")
        # map menue
        map_menue = wx.Menu()
        # Map Style
        map_style_menu = wx.Menu()
        opensteetmap_style = map_style_menu.Append(111, "&OpenStreetMap")
        stamen_terrain_style = map_style_menu.Append(112, "&Stamen Terrain")
        stamen_toner_style = map_style_menu.Append(113, "&Stamen Toner")
        cartodbpositron_style = map_style_menu.Append(114, "&Cartodbpositron")

        # for the custom icon in menue
        # mymenu = wx.MenuItem(map_menue, wx.ID_ABOUT)
        # mymenu.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_WARNING))
        # map_style_menu.Append(mymenu)

        # Map Styles
        map_menue.AppendSubMenu(map_style_menu,"&Map Styles")
        import_zones_menue = wx.Menu()
        input_red_geojason = import_zones_menue.Append(1222, "&Red Zone")
        input_yellow_geojason = import_zones_menue.Append(1332, "&Yellow Zone")
        map_menue.AppendSubMenu(import_zones_menue,"&Geofencing")

        reload = map_menue.Append(14, "&Reload Map")


        # server menues
        server_menue = wx.Menu()


        # Email Server
        email_server_menue = wx.Menu()
        start_email_server = email_server_menue.Append(12, "&Start")
        stop_email_server = email_server_menue.Append(13, "&Stop")
        server_menue.AppendSubMenu(email_server_menue,"&Email Server")



        # GPS Server
        gps_server_menue = wx.Menu()
        start_gps_server = gps_server_menue.Append(12, "&Start")
        stop_gps_server = gps_server_menue.Append(13, "&Stop")
        server_menue.AppendSubMenu(gps_server_menue,"&GPS Server")


        # Alarm Server
        alarm_server_menue = wx.Menu()
        start_alarm_server = alarm_server_menue.Append(12, "&Start")
        stop_alarm_server = alarm_server_menue.Append(13, "&Stop")
        server_menue.AppendSubMenu(alarm_server_menue,"&Alarm Server")


        # File Server
        file_server_menue = wx.Menu()
        start_file_server = file_server_menue.Append(12, "&Start")
        stop_file_server = file_server_menue.Append(13, "&Stop")
        server_menue.AppendSubMenu(file_server_menue,"&File Server")


        # help
        help_menue = wx.Menu()
        about_us = help_menue.Append(31, "&About us")
        contact_us = help_menue.Append(32, "&Contact us")


        menubar = wx.MenuBar()
        menubar.Append(corona_service_menue, "&Corona Services")
        menubar.Append(map_menue, "&Map")
        menubar.Append(server_menue, "&Server")
        menubar.Append(help_menue, "&Help")

        self.SetMenuBar(menubar)
        #bind to the functions!
        self.Bind(wx.EVT_MENU, self.alarm_navigator_start, alarm_navigator_start)
        self.Bind(wx.EVT_MENU, self.person_navigator_start, person_navigator_start)
        self.Bind(wx.EVT_MENU, self.temperature_navigator_start, temperature_navigator_start)
        self.Bind(wx.EVT_MENU, self.lepton_navigator_start, lepton_navigator_start)
        self.Bind(wx.EVT_MENU, self.opensteetmap_style, opensteetmap_style)
        self.Bind(wx.EVT_MENU, self.stamen_terrain_style, stamen_terrain_style)
        self.Bind(wx.EVT_MENU, self.stamen_toner_style, stamen_toner_style)
        self.Bind(wx.EVT_MENU, self.cartodbpositron_style, cartodbpositron_style)
        self.Bind(wx.EVT_MENU, self.input_yellow_geojason, input_yellow_geojason)
        self.Bind(wx.EVT_MENU, self.input_red_geojason, input_red_geojason)
        self.Bind(wx.EVT_MENU, self.reload, reload) # todo: funciton reload
        self.Bind(wx.EVT_MENU, self.start_gps_server, start_gps_server)
        self.Bind(wx.EVT_MENU, self.stop_gps_server, stop_gps_server)
        self.Bind(wx.EVT_MENU, self.start_email_server, start_email_server)
        self.Bind(wx.EVT_MENU, self.stop_email_server, stop_email_server)
        self.Bind(wx.EVT_MENU, self.start_alarm_server, start_alarm_server)
        self.Bind(wx.EVT_MENU, self.stop_alarm_server, stop_alarm_server)
        self.Bind(wx.EVT_MENU, self.start_file_server, start_file_server)
        self.Bind(wx.EVT_MENU, self.stop_file_server, stop_file_server)

        # self.Bind(wx.EVT_MENU, self.start_tk, tkinter_start) # todo: funciton about us
        # self.Bind(wx.EVT_MENU, self.start_tk, tkinter_start) #todo: funciton contact us

    def my_tk(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.mainloop()

    def start_tk(self,e):
        # print("HI")
        # self.tkinter_main = threading.Thread(target=self.my_tk)
        # self.tkinter_main.setDaemon(True)
        # # add to the thread array!
        # # self.threads.append(self.gps_server_thread)
        # self.tkinter_main.start()
        pass

    def start_tk(self):
        # fix to exception with wxPython 4.1.1:
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform
        locale.getlocale(locale.LC_TIME)

        print("HI")
        self.tkinter_main = threading.Thread(target=self.my_tk)
        self.tkinter_main.setDaemon(True)
        # add to the thread array!
        # self.threads.append(self.gps_server_thread)
        self.tkinter_main.start()

    def reload(self,e):
        # self.reload
        # self.on_load_url()
        # self.embed_browser()
        self.generate_index_html_file("polygon_geojason/yellow.geojson", "polygon_geojason/red.geojason")
        # cef = 0
        # window_info = cef.WindowInfo()
        # (width, height) = self.browser_panel.GetClientSize().Get()
        # assert self.browser_panel.GetHandle(), "Window handle not available"
        # window_info.SetAsChild(self.browser_panel.GetHandle(),
        #                        [0, 0, width, height])
        # print(cef.GetDataUrl("file:///C:/Users/Jack/PycharmProjects/corona_alarm_final/corona_alarm_final/index.html"))
        # print(cef.Hand)
        # self.browser = None
        # self.browser = cef.CreateBrowserSync(window_info,
                                             # url="file:///C:/Users/Jack/PycharmProjects/corona_alarm_final/corona_alarm_final/index1.html")
        # self.browser.LoadUrl("http://www.yahoo.com")
        # browser = cef.CreateBrowserSync(url=html_to_data_uri("file:///C:/Users/Jack/PycharmProjects/corona_alarm_final/corona_alarm_final/index1.html"),
        #                                 window_title="Tutorial")
        # self.browser.SetClientHandler(FocusHandler())
        # self.browser.ExecuteJavascript('alert("Hello!");')
        self.browser.ExecuteJavascript('window.location.reload();')
        # self.
        # self.browser.GetBrowser.Reload()
        # self.browser.CloseBrowser()
        # self.__init__('OpenStreetMap')
        # self.browser_panel.UpdateWindowUI()
        # self.browser_panel.
        # self.browser.

    def opensteetmap_style(self,e):
        self.map_style = "OpenStreetMap"

    def stamen_terrain_style(self,e):
        self.map_style = "Stamen Terrain"

    def stamen_toner_style(self,e):
        self.map_style = "Stamen Toner"

    def cartodbpositron_style(self,e):
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
        self.main_alarm_server = alarm_server.Alarm_server("127.0.0.1", 20001, 5001, self.root)# "127.0.0.1", 20001
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
    def input_red_geojason(self,e):
        import_red_geojason.Input_red_geojason(self.root)


    # import the red geojason gui
    def input_yellow_geojason(self,e):
        import_yellow_geojason.Input_yellow_geojason(self.root)

    def start_gps_server(self,e):
        if self.gps_server == None:
            # GPS SERVER
            self.gps_server = server_gps.Server_gps("127.0.0.1", 9999, 1000)
            # self.gps_server.run_listen()
            self.gps_server_thread = threading.Thread(target=self.gps_server.run_listen)
            self.gps_server_thread.setDaemon(True)
            # add to the thread array!
            self.threads.append(self.gps_server_thread)
            self.gps_server_thread.start()
            print("Gps server is running")

    def stop_gps_server(self,e):
        if self.gps_server != None:
            self.gps_server.continue_server = False
            # self.gps_server_thread.join()
            # print(self.gps_server)

    def start_email_server(self,e):
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

    def stop_email_server(self,e):
        if self.email_server != None:
            self.email_server.continue_server = False

    def start_alarm_server(self,e):
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

    def stop_alarm_server(self,e):
        if self.main_alarm_server_thread_from_menue != None or self.main_alarm_server != None:
            self.main_alarm_server.continue_server = False

    def start_file_server(self,e):
        if self.main_alarm_server.new_file_server != None:
            self.main_file_server = file_server.File_server_windows("127.0.0.1", 5001)
            # self.gps_server.run_listen()
            self.main_file_server_thread_from_menue = threading.Thread(target=self.main_file_server.run_listen)
            self.main_file_server_thread_from_menue.setDaemon(True)
            # add to the thread array!
            self.threads.append(self.main_file_server_thread_from_menue)
            self.main_file_server_thread_from_menue.start()

            self.main_file_server.run_server()

    def stop_file_server(self,e):
        if self.main_alarm_server.new_file_server != None:
            self.main_alarm_server.new_file_server.continue_server = False

    def close(self,e):  # todo: how to exit carefully? ask prof.Kerer
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

    def lepton_navigator_start(self,e):
        self.main_alarm_server.new_file_server.image_folder = "alarm_images/default"
        corona_alarm.Corona_alarm("alarm_images/default",
                                  "Welcome to Lepton Navigator!\nHere you can select a date and time and download the cooresponding images from the user raspberry pi!",
                                  self.root)

    def temperature_navigator_start(self,e):
        alarm_db_gui.Alarm_Gui(self.root)

    def person_navigator_start(self,e):
        person_db_gui.Person_gui(0, self.root)

    def alarm_navigator_start(self,e):
        self.main_alarm_server = alarm_server.Alarm_server("127.0.0.1", 20001, 5001, self.root)  # "127.0.0.1", 20001

        # self.alarm_navigator_from_main = threading.Thread(target=self.run_alarm_server)
        # self.threads.append(self.alarm_navigator_from_main)
        # self.alarm_navigator_from_main.setDaemon(True)
        # self.alarm_navigator_from_main.start()


    # until here is from me
    def embed_browser(self):
        window_info = cef.WindowInfo()
        (width, height) = self.browser_panel.GetClientSize().Get()
        assert self.browser_panel.GetHandle(), "Window handle not available"
        window_info.SetAsChild(self.browser_panel.GetHandle(),
                               [0, 0, width, height])
        self.browser = cef.CreateBrowserSync(window_info,
                                             url="file:///C:/Users/Jack/PycharmProjects/corona_alarm_final/corona_alarm_final/index.html")
        self.browser.SetClientHandler(FocusHandler())

    def OnSetFocus(self, _):
        if not self.browser:
            return
        if WINDOWS:
            cef.WindowUtils.OnSetFocus(self.browser_panel.GetHandle(),
                                       0, 0, 0)
        self.browser.SetFocus(True)

    def OnSize(self, _):
        if not self.browser:
            return
        if WINDOWS:
            cef.WindowUtils.OnSize(self.browser_panel.GetHandle(),
                                   0, 0, 0)
        elif LINUX:
            (x, y) = (0, 0)
            (width, height) = self.browser_panel.GetSize().Get()
            self.browser.SetBounds(x, y, width, height)
        self.browser.NotifyMoveOrResizeStarted()

    def OnClose(self, event):
        print("[wxpython.py] OnClose called")
        if not self.browser:
            # May already be closing, may be called multiple times on Mac
            return

        if MAC:
            # On Mac things work differently, other steps are required
            self.browser.CloseBrowser()
            self.clear_browser_references()
            self.Destroy()
            global g_count_windows
            g_count_windows -= 1
            if g_count_windows == 0:
                cef.Shutdown()
                wx.GetApp().ExitMainLoop()
                # Call _exit otherwise app exits with code 255 (Issue #162).
                # noinspection PyProtectedMember
                os._exit(0)
        else:
            # Calling browser.CloseBrowser() and/or self.Destroy()
            # in OnClose may cause app crash on some paltforms in
            # some use cases, details in Issue #107.
            self.browser.ParentWindowWillClose()
            event.Skip()
            self.clear_browser_references()

    def clear_browser_references(self):
        # Clear browser references that you keep anywhere in your
        # code. All references must be cleared for CEF to shutdown cleanly.
        self.browser = None


class FocusHandler(object):
    def OnGotFocus(self, browser, **_):
        # Temporary fix for focus issues on Linux (Issue #284).
        if LINUX:
            print("[wxpython.py] FocusHandler.OnGotFocus:"
                  " keyboard focus fix (Issue #284)")
            browser.SetFocus(True)


class CefApp(wx.App):

    def __init__(self, redirect):
        self.timer = None
        self.timer_id = 1
        self.is_initialized = False
        super(CefApp, self).__init__(redirect=redirect)

    def OnPreInit(self):
        super(CefApp, self).OnPreInit()
        # On Mac with wxPython 4.0 the OnInit() event never gets
        # called. Doing wx window creation in OnPreInit() seems to
        # resolve the problem (Issue #350).
        if MAC and wx.version().startswith("4."):
            print("[wxpython.py] OnPreInit: initialize here"
                  " (wxPython 4.0 fix)")
            self.initialize()

    def OnInit(self):
        self.initialize()
        return True

    def initialize(self):
        if self.is_initialized:
            return
        self.is_initialized = True
        self.create_timer()
        frame = MainFrame("OpenStreetMap")
        self.SetTopWindow(frame)
        frame.Show()

    def create_timer(self):
        # See also "Making a render loop":
        # http://wiki.wxwidgets.org/Making_a_render_loop
        # Another way would be to use EVT_IDLE in MainFrame.
        self.timer = wx.Timer(self, self.timer_id)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(10)  # 10ms timer

    def on_timer(self, _):
        cef.MessageLoopWork()

    def OnExit(self):
        self.timer.Stop()
        return 0


if __name__ == '__main__':
    main()