# It generates the payload to send to the raspberry
# you can set a coordinate and run it for the coordinates YOU DO NOT HAVE TO USE THE CONSTRUCTOR EVERY TIME!!
# it needs db_navigator_alarm.py and insert_into_coordinate
import locale

import datetime
import db_navigator_alarm
import distance_direction_measure
import led_enabler
from shapely.geometry import  Point
import html_email_generator
import send_sms


class Payload_generator_server():
    def __init__(self, map, yellow_area_file_name, red_area_file_name):
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform

        # print(self.coordiantes)
        # distance_deg = (int, int)
        self.distance_deg_list = []
        self.contact_person = []
        self.yellow_area_file_name = yellow_area_file_name
        self.red_area_file_name = red_area_file_name
        self.map = map

        # self.get_payload()

    def set_run_coordinates(self,altitude, longitude, distance_border=100):
        self.distance_border = distance_border
        self.coordiantes = (altitude, longitude)
        self.coordiantes_point = Point(altitude, longitude)  # from raspberry
        self.insert_into_coordinates_table(altitude, longitude)
        self.distance_measurer = distance_direction_measure.Distance_measure()
        self.distance_measurer.measure_distance_datetime_key(distance_border, (self.coordiantes_point.x, self.coordiantes_point.y))
        self.user_in_yellow_bool, self.user_in_red_bool = self.area_led_enable()

    # list = [(20,230),(50,260),(70,270),(250,250),(100,260)]
    # print(list[-5:])
    def init_contact_person(self,contact_person):# I do not annoy the client whenever he pass to the sick person again!
        for person in contact_person:
            print(person)
            pass #TODO IMPLEMENT!!
    def toward_direction(self):
        toward_direction_bool = False
        if len(self.distance_deg_list) == 40:
            self.distance_deg_list = self.distance_deg_list[-5:]
            # print(distance_deg_list)
        if len(self.distance_deg_list) < 5:
            # toward_direction_bool = False
            return
        else:
            true_dir = 0
            false_dir = 0
            true_distance = 0
            false_distance = 0
            for i in range(len(self.distance_deg_list)-1, len(self.distance_deg_list)-6, -1):
                # print(i)
                if (self.distance_deg_list[i][0] < self.distance_deg_list[i-1][0]) :
                    true_distance += 1
                else:
                    false_distance += 1
                if (abs(self.distance_deg_list[i][3]- self.distance_deg_list[i-1][3]) < 45) or (abs(self.distance_deg_list[i][3]- self.distance_deg_list[i-1][3]) > 320):
                    true_dir +=1
                else:
                    false_dir += 1
            true_dir_possibility = true_dir / len(self.distance_deg_list)
            true_distance_possibility = true_distance / len(self.distance_deg_list)

            if true_dir_possibility > 0.6 and true_distance_possibility > 0.6:
                toward_direction_bool = True

            print(toward_direction_bool)
            return toward_direction_bool

    # lat2 =16.379849
    # long2 = 48.208205
    # 16.381392,48.211338
    # p1 = 48.211338, 16.381392
    # p1 = 48.211338, 16.381392
    # p1 = 48.211327, 16.381339
    # p1 = 48.211327, 16.381307
    # p1 = 48.211308, 16.381300
    # p1 = 48.211294, 16.381289
    # p1 = 48.211269, 16.381273






    def insert_into_coordinates_table(self,altitude, longitude):# 16.379849,48.208205
        db_coordinates = db_navigator_alarm.Database_navigator()
        db_coordinates.insert_into_coordinate(altitude, longitude)


    def area_led_enable(self):# "yellow.geojson", "red.geojason"
        my_led_enabler = led_enabler.Led_enabler(self.map, self.yellow_area_file_name, self.red_area_file_name)
        user_in_yellow_bool, user_in_red_bool = my_led_enabler.turn_on_off(self.coordiantes_point)
        print(user_in_yellow_bool, user_in_red_bool) # to send to the raspberry
        return user_in_yellow_bool, user_in_red_bool


    def count_degree_direction(self):
        print(len(self.distance_measurer.distance_datetime))# TO SEND to the raspberry count
        count = len(self.distance_measurer.distance_datetime)
        print(self.distance_measurer.distance_datetime[0][0])#distance (20.96669047875604, '2021-03-29 23:18:48', 'South-West', 282.25150846134215)
        min_distance = self.distance_measurer.distance_datetime[0][0]
        print(int(self.distance_measurer.distance_datetime[0][3]))# degree TO SEND
        degree = int(self.distance_measurer.distance_datetime[0][3])
        print(self.distance_measurer.distance_datetime[0][2])# the direction TO SEND
        direction = self.distance_measurer.distance_datetime[0][2]
        return count, min_distance, degree, direction




    def append_into_get_list(self):
        #append TODO: make the distance_deg_list with self!!
        self.distance_deg_list.append(self.distance_measurer.distance_datetime[0])



    def buzzer_red_led__on_off(self,current_min_distance, toward_direction_bool):
        print(current_min_distance)
        red_on_off = False
        buzzer = False
        #uncomment to test the email functionality!
        # email_sender = html_email_generator.Html_email_generator(self.distance_border, self.distance_measurer.distance_datetime)
        # # (20.96669047875604, '2021-03-29 23:18:48', 'West', 282.25150846134215),
        # # (353.48332167934547, '2021-03-29 19:27:32', 'South-West', 230.72028895216073),
        # # (907.4177354127442, '2021-03-29 19:26:17', 'South', 201.83119608979754)])
        #
        # email_sender.send_email('gholibeigian.k85@htlwienwest.at', 'kokolubilubi@gmail.com',
        #                         'Critical Situation Detected!')

        # sms = send_sms.Sms_send(
        #     "\nWe have detected a sick person closer than 20 meters from you!\nPlease check your email for more information.\nBest regards,\nCorona Alarm Center")
        # sms.send_sms()

        if current_min_distance <= 50:
            red_on_off = True
            if current_min_distance <= 20 and toward_direction_bool == True:
                buzzer = True
                # email()
                # you cannot change the distance below becouse of the self.distance_measurer.distance_datetime. It comes from the
                # first call of the calss!
                email_sender = html_email_generator.Html_email_generator(self.distance_border, self.distance_measurer.distance_datetime)
                    # (20.96669047875604, '2021-03-29 23:18:48', 'West', 282.25150846134215),
                    # (353.48332167934547, '2021-03-29 19:27:32', 'South-West', 230.72028895216073),
                    # (907.4177354127442, '2021-03-29 19:26:17', 'South', 201.83119608979754)])

                email_sender.send_email('gholibeigian.k85@htlwienwest.at', 'kokolubilubi@gmail.com',
                                          'Critical Situation Detected!')

                # sms()
                sms = send_sms.Sms_send(
                    "\nWe have detected a sick person closer than 20 meters from you!\nPlease check your email for more information.\nBest regards,\nCorona Alarm Center")
                sms.send_sms()

                # TODO: insert in table self.contact_person()
                self.contact_person.append((datetime.datetime.now(), self.distance_measurer.distance_datetime[0][1]))
            else:
                buzzer = False
        return buzzer, red_on_off

    def get_payload(self):
        if len(self.distance_measurer.distance_datetime) != 0:
            count, min_distance, degree, direction = self.count_degree_direction()
            current_min_distance = int(self.distance_measurer.distance_datetime[0][0])
            toward_direction_bool = self.toward_direction()
            buzzer, red_on_off = self.buzzer_red_led__on_off(current_min_distance,toward_direction_bool)
            self.contact_person.append((datetime.datetime.now(), self.distance_measurer.distance_datetime[0][1]))
            print(self.user_in_yellow_bool,
                  self.user_in_red_bool,
                  count,
                  current_min_distance,
                  int(self.distance_measurer.distance_datetime[0][3]),buzzer,
                  red_on_off)
            print(self.contact_person)
            return self.user_in_yellow_bool,self.user_in_red_bool, count, current_min_distance, direction,int(self.distance_measurer.distance_datetime[0][3]),buzzer,red_on_off

        else:
            print(self.user_in_yellow_bool,
                  self.user_in_red_bool,
                  0,
                  None,
                  None,False,
                  False)
            return str(self.user_in_yellow_bool), str(self.user_in_red_bool), str(0),"None", "None", "None", "False", "False"



if __name__ == "__main__":
    my_Payload_generator_server = Payload_generator_server(map, "polygon_geojason/yellow.geojson",
                                                           "../corona_alarm_final/polygon_geojason/red.geojason")
    # my_Payload_generator_server.set_run_coordinates(16.334343,48.239931,100) # altitude, longitude, distance=100
    my_Payload_generator_server.set_run_coordinates(16.381392, 48.211338,100)
    my_Payload_generator_server.get_payload()

    # my_Payload_generator_server.set_run_coordinates(16.381385, 48.211385)
    # my_Payload_generator_server.get_payload()