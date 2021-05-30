#IMPORTANT DO NOT DELETE!
# It verifies if a point is in a polygon
# It takes 2 geojason files and can add the areas to the given map.
# turn_on_off() will give back the boolean used to turn on the led on the raspberry
# TODO: COMLETE IT(merge!)
import locale

import json, folium
from shapely.geometry import shape, Point
import load_polygon
# depending on your version, use: from shapely.geometry import shape, Point
class Led_enabler:
    def __init__(self,map, yellow_area_file, red_area_file):
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform

        self.yellow_file_name = yellow_area_file
        self.red_file_name = red_area_file
        # load as area
        self.my_map = load_polygon.Load_ploygon(map, yellow_area_file, red_area_file)
        self.my_map.load_geo_pol()
        # Uncomment if you need to add it to the map on the server!(generates a new index.html!)
        # self.my_map.add_to_map()
        self.yellow_area_json_gui, self.red_area_json_gui = self.my_map.import_polygon_geojason()
        self.load_area_json_files()
    # check each polygon to see if it contains the point for red_area
    def led_enabler(self,area_json,point):
        for feature in area_json['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(point):
                print('Found containing polygon in zone:', feature)
                return True
            # else:
            #     print("not found")
        return False
# load GeoJSON file containing sectors
    # with this method we can see if a point is inside the area or not(you can access the fields)
    def read_geojason_file(self,file_name):
        with open(file_name) as f:
            return json.load(f)

    #load_json_tones_for_server
    def load_area_json_files(self):
        self.yellow_area_json = self.read_geojason_file(self.yellow_file_name)
        self.red_area_json = self.read_geojason_file(self.red_file_name)
        # return self.yellow_area_json, self.red_area_json

    def turn_on_off(self,point):
        # just work with user_in_red_bool, user_in_yellow_bool
        user_in_yellow_bool = self.led_enabler(self.yellow_area_json,point)
        user_in_red_bool = self.led_enabler(self.red_area_json,point)
        return user_in_yellow_bool, user_in_red_bool



if __name__ == "__main__":
    map = folium.Map(location=[48.208176, 16.373819],tiles="OpenStreetMap", zoom_start=15)
    # construct point based on lon/lat returned by geocoder
    # point = Point(16.479785, 48.215995)
    # point = Point(16.496901 ,48.216505 )
    # point = Point(16.498139, 48.216298 )
    # point = Point(16.374294, 48.198593)
    # point = Point(16.375657,48.199258)

    point = Point(16.334343,48.239931)
    # print(type(js[3]))
    led_enabler = Led_enabler(map, "polygon_geojason/yellow.geojson",
                              "../corona_alarm_final/polygon_geojason/red.geojason")
    user_in_yellow_bool, user_in_red_bool = led_enabler.turn_on_off(point)
    print(user_in_yellow_bool,user_in_red_bool)
            # # load as area
            # x = load_polygon.Load_ploygon(,
            #                               "yellow.geojson", "red.geojason")
            # x.load_geo_pol()

    #just for server







#
#
# folium.Map(location=[48.208176, 16.373819],tiles="OpenStreetMap", zoom_start=15)
#
#     "yellow.geojson"
#     "red.geojason"