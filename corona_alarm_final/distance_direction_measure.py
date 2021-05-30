# it loads the coordinations from database and then measures the min distance to the alarms
# measure_min_distance measures the min distance to the alarm in meters
# measure_distance_datetime_key gives back a list of (distance, sql_datetime=key)
# !!!!!! def calcNSEW(self): IS FALSE!!!
import locale

from math import sin, cos, sqrt, atan2, radians, degrees, pi, log, tan
import db_navigator_alarm

#  48.188191, 16.431695
#  48.189006, 16.432328
class Distance_measure:
    def __init__(self):
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform

        self.R = 6373.0
        self.db_navigator = db_navigator_alarm.Database_navigator()
        self.coordinates_alarms = self.db_navigator.load_data_test_alarms("")

    def measure_min_distance(self, point):
        self.min_distance = [922337203685477580,0,"",""]
        for alarm in self.coordinates_alarms:
            min_distance_alarm = self.measure_distance(point, alarm[0])
            if min_distance_alarm < self.min_distance[0]:
                direction_close_degree, direction_str = self.calculate_initial_compass_bearing_NSEW_NOTSELF(point,alarm[0])
                self.min_distance[0] =  min_distance_alarm
                self.min_distance[1] =  direction_close_degree
                self.min_distance[2] =  direction_str
                self.min_distance[3] =  alarm[1].strftime('%Y-%m-%d %H:%M:%S')
        return min_distance_alarm


    def measure_distance(self,point_a, point_b):
        lat1 = radians(point_a[0])
        lon1 = radians(point_a[1])
        lat2 = radians(point_b[0])
        lon2 = radians(point_b[1])
        # point_a = (lat1, lon1)
        # point_b = (lat2, lon2)
        dlon = radians(point_b[1]) - radians(point_a[1])
        dlat = radians(point_b[0]) - radians(point_a[0])
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        self.distance = self.R * c * 1000
        return self.distance
    #save the distances and keys in a list:
    def measure_distance_datetime_key(self, distance_border, point):
        self.distance_datetime = []
        for alarm in self.coordinates_alarms:
            distance = self.measure_distance(point, alarm[0])
            if distance < distance_border:
                degree_direction = self.calculate_initial_compass_bearing(point, alarm[0])
                direction = self.calcNSEW()
                self.distance_datetime.append((distance,alarm[1].strftime('%Y-%m-%d %H:%M:%S'),direction,degree_direction))
        self.distance_datetime.sort(key=lambda x: x[0], reverse=False)

   #it does not use self variables safe!
    def calculate_initial_compass_bearing_NSEW_NOTSELF(self,pointA, pointB):
        if (type(pointA) != tuple) or (type(pointB) != tuple):
            raise TypeError("Only tuples are supported as arguments")

        lat1 = radians(pointA[0])
        lat2 = radians(pointB[0])

        diffLong = radians(pointB[1] - pointA[1])

        x = sin(diffLong) * cos(lat2)
        y = cos(lat1) * sin(lat2) - (sin(lat1)
                                               * cos(lat2) * cos(diffLong))

        initial_bearing = atan2(x, y)

        # Now we have the initial bearing but math.atan2 return values
        # from -180° to + 180° which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        initial_bearing = degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360

        points = ["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"]
        # bearing = calcBearing(lat1, long1, lat2, long2)
        # compass_bearing += 22.5
        compass_bearing = compass_bearing % 360
        compass_bearing_index = int(compass_bearing / 45)  # values 0 to 7
        NSEW = points[compass_bearing_index]

        print(compass_bearing,NSEW)
        return compass_bearing,NSEW





    def calculate_initial_compass_bearing(self,pointA, pointB):
        # this funciton had problem!
        # if (type(pointA) != tuple) or (type(pointB) != tuple):
        #     raise TypeError("Only tuples are supported as arguments")
        #
        # lat1 = radians(pointA[0])
        # lat2 = radians(pointB[0])
        #
        # diffLong = radians(pointB[1] - pointA[1])
        #
        # x = sin(diffLong) * cos(lat2)
        # y = cos(lat1) * sin(lat2) - (sin(lat1)
        #         * cos(lat2) * cos(diffLong))
        #
        # initial_bearing = atan2(x, y)
        #
        # # Now we have the initial bearing but math.atan2 return values
        # # from -180° to + 180° which is not what we want for a compass bearing
        # # The solution is to normalize the initial bearing as shown below
        # # initial_bearing = degrees(initial_bearing) + 90
        # # self.compass_bearing = (initial_bearing + 360) % 360
        # # return self.compass_bearing
        #
        # #test
        # self.compass_bearing = initial_bearing
        # return initial_bearing
        deg2rad = pi / 180
        latA = pointA[0] * deg2rad
        latB = pointB[0] * deg2rad
        lonA = pointA[1] * deg2rad
        lonB = pointB[1] * deg2rad

        delta_ratio = log(tan(latB / 2 + pi / 4) / tan(latA / 2 + pi / 4))
        delta_lon = abs(lonA - lonB)

        delta_lon %= pi
        bearing = atan2(delta_lon, delta_ratio) / deg2rad
        if lonA <= lonB :
            if bearing > 0 and bearing < 90:
                self.compass_bearing =  90 - bearing
            elif bearing >= 90 and bearing <= 180:
                self.compass_bearing = 450-bearing
        else:
            self.compass_bearing = bearing + 90


        return self.compass_bearing





    def calcNSEW(self):
        points = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        # bearing = calcBearing(lat1, long1, lat2, long2)
        bearing = self.compass_bearing
        bearing += 22.5
        bearing = bearing % 360
        # self.compass_bearing = self.compass_bearing - 45
        bearing = int(bearing / 45)  # values 0 to 7
        NSEW = points[bearing]

        return NSEW
# lat1 = 38.8976763
# long1 = -77.0365298
# # Lincoln memorial 38.8893° N, 77.0506° W
# lat2 = 38.8893
# long2 = -77.0506
#
# points = calculate_initial_compass_bearing((lat1, long1), (lat2, long2))
# print(points)

if __name__ == "__main__":
    distance_measurer =  Distance_measure()
    # print("Result:", distance_measurer.measure_distance(point_a, point_b), "meters")
    # print(distance_measurer.measure_min_distance((16.381392,48.211338))) #16.381392 ,48.211338
    # print(distance_measurer.measure_min_distance((16.381392 ,48.211338))) #16.381392 ,48.211338
    # print(distance_measurer.min_distance)
    distance_measurer.measure_distance_datetime_key(1000,(16.381392,48.211338))
    # print(distance_measurer.distance_datetime)
    # distance_measurer.calculate_initial_compass_bearing((16.381392,48.211338), (48.189006, 16.432328))# calculates the degree
    # print(distance_measurer.calcNSEW()) #show the direction eg:north west
    print(distance_measurer.distance_datetime) # this is the perfect output it sorts it out!!!


    # 48.193595, 16.411717
    # 48.211812, 16.383711
    # 48.211338, 16.381392