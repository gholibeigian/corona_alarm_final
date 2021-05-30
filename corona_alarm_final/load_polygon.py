#it read from yellow.geojson and red.geojason and then loads polygons in yellow and red
import locale

import datetime
import mysql.connector

import json
import pygeoj
import folium

class Load_ploygon:
    #I use 2 methods to load the geo data
    #one for the map -> self.yellow_file , self.red_file
    #one for the server -> self.red_file_json, self.yellow_file_json
    def __init__(self, m, yellow_geojason_file_name, red_geojason_file_name):
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform

        self.map = m
        self.yellow_file = yellow_geojason_file_name
        self.red_file = red_geojason_file_name

        self.red_file_json = red_geojason_file_name
        self.yellow_file_json = yellow_geojason_file_name
    # use it just for gui!!!!!
    def load_geo_pol(self):
        self.yellow_data = pygeoj.load(self.yellow_file)
        self.red_data = pygeoj.load(self.red_file)

    # to export as geojason(use it in server!)
    # with this method we can see if a point is inside the area or not(you can access the fields)
    def import_polygon_geojason(self):
        with open(self.yellow_file) as f:
            self.yellow_data_geojason = json.load(f)
        with open(self.red_file) as f:
            self.red_data_geojason = json.load(f)
        return self.yellow_data_geojason, self.red_data_geojason

    def add_to_map(self):
        self.yellow_polygons = []
        for polygon in self.yellow_data:
            # print(polygon)
            #'fillColor': 'red',
            self.yellow_polygons.append(polygon)
            folium.GeoJson(polygon,
                           style_function=lambda x: {
                               'fillColor': 'yellow',
                           }).add_to(self.map)
        self.red_polygons = []
        for polygon in self.red_data:
            # print(polygon)
            #'fillColor': 'red',
            self.yellow_polygons.append(polygon)
            folium.GeoJson(polygon,
                           style_function=lambda x: {
                               'fillColor': 'red',
                           }).add_to(self.map)
        # self.load_iframes(self.map)
        # self.map.save("index.html") # TODO: please comment
            # folium.GeoJson(i).add_to(m)
            # style_function = lambda x: {'fillColor': '#0000ff'}
        # for i in range(0, len(self.data['features'][0]['geometry']['coordinates'][0])):
        #     print(i)
        #     data = (self.data['features'][0]['geometry']['coordinates'][0][i][0],
        #             self.data['features'][0]['geometry']['coordinates'][0][i][1])
        #     self.list_of_points.append(data)
        # print(self.list_of_points)
    # folium.GeoJson(data_string).add_to(m)
    def import_red_yellow_geojason(self):
        # return self.yellow_polygons, self.red_polygons
        return self.yellow_data,self.red_data

    # it loads the markers on the map
    def load_iframes(self):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="corona_alarm"
        )

        mycursor = db.cursor(buffered=True)
        mycursor2 = db.cursor(buffered=True)
        mycursor.execute("select * from alarms;")
        for row in mycursor:
            # print(row)
            pid = row[0]
            altitude = row[1]
            longitude = row[2]
            temperature = row[3]
            thermal_image = row[4]
            py_image = row[5]
            time_detected = row[6]
            mycursor2.execute("select * from persons where pid=" + str(pid) + " limit 1;")
            for row in mycursor2:
                # print(row)
                first_name = row[1]
                last_name = row[2]
                SVNR = row[4]
                in_blacklist = row[5]
                # print(first_name, last_name,SVNR, in_blacklist )

            custom_html = "<!DOCTYPE html><html lang='en'><head><link rel='stylesheet' href='css/mystyle.css'><link rel='stylesheet' href = 'css/bootstrap_themes.css'><link rel = 'stylesheet' href = 'css/bootstrap_min.css'><meta charset='UTF-8'><meta http-equiv='X-UA-Compatible' content='IE=edge'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Document</title></head><body><h1>Alarm Detected:</h1><h2><span id='blue'> {detected_on}</span></h2><div class='row'><div class='column'><img src= {thermal_image} alt='Thermal Image' style='width:100%'></div><div id='pyimage' class='column'><img src={py_image} alt='PyImage' style='width:100%'></div></div><div class='data'><p>Name:        {first_name} {last_name}</br>Temperature: {temperature}</br>PID:         {PID}</br>SVNR:        {SVNR}</br>Possibility: {possibility}</br><span id='red'>Blacklist:   {in_blacklist}</span></br>Coordinate:  {altitude}, {longitude}</p></div><script src = 'js/jquery.js'> </script><script src = 'js/bootstrap_min.js'> </script></body></html>".format(
                detected_on=time_detected,
                thermal_image="../images/" + thermal_image,
                py_image="../images/" + py_image,
                first_name=first_name,
                last_name=last_name,
                temperature=temperature,
                PID=pid,
                SVNR=SVNR,
                possibility="60%",
                in_blacklist=in_blacklist,
                altitude=altitude,
                longitude=longitude
            )
            print(custom_html)
            file_name = "html_files/" + datetime.datetime.strftime(time_detected, "%Y_%m_%d_T_%I_%M_%S__%f.html")
            Html_file = open((file_name), "w")
            Html_file.write(custom_html)
            Html_file.close()
            folium.Marker(location=[altitude, longitude],
                          popup="<html><body><iframe frameBorder='0' width='400px' height='%d px' src='%s'></iframe></body></html>" % (
                              400, file_name),
                          tooltip="Click for more information"
                          ).add_to(self.map)

        mycursor.close()
        mycursor2.close()
    def generate_index_html_marker_polygon(self, file_index_address):
        self.map.save(file_index_address)


if __name__ == "__main__":
    m = folium.Map(location=[48.208176, 16.373819],tiles="OpenStreetMap", zoom_start=15)
    x = Load_ploygon(m, "polygon_geojason/yellow.geojson", "polygon_geojason/red.geojason")
    x.load_geo_pol()
    x.load_iframes()
    x.add_to_map() # just gui the only the polygons!
    x.generate_index_html_marker_polygon("../corona_alarm_final/index.html")
    # x.import_red_yellow_geojason()# zones for the server!