# it receives a mimum distance in meters and a list of distance_datetime in (distance, (datetime= key of the sql database)
# and it generates a html file in /emails and returns the html file name from .write_file()
# send_email() sends the email
import locale


import datetime
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.image import  MIMEImage
from email.mime.multipart import MIMEMultipart
# import folium
# m = folium.Map(location=[48.208176, 16.373819],tiles="OpenStreetMap", zoom_start=15)

class Html_email_generator:
    def __init__(self, min_distance, distance_datetime_list):
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform

        self.image_num_even_counter = 0
        # self.detected_on = detected_on
        self.min_distance = min_distance
        self.distance_datetime = distance_datetime_list

        # to have the addresses of the iamges to send by email. It is indipendent from other parts!
        self.images_address_for_email = []


    def write_file(self):
        self.start_html = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title></head><body><h1 style="color:blueviolet;">Alart Area!</h1><h2 style="color:red;">We believe that you are close to potentially sick people! We kindly ask you to keep your distance from them.</h2><h3>We have already detected an alarm in {min_distance} meters away from you!</h3>'.format(min_distance=self.min_distance)
        self.divs = ""
        for elemet in self.distance_datetime:
            self.divs = self.divs + self.load_divs(elemet)

        self.end_html = '<p>Best regards,<br>Corona Alarm Center</p></body></html>'
        self.html_file = self.start_html + self.divs + self.end_html
        # print(self.html_file)
        file_name = "emails/" + datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d_T_%I_%M_%S__%f.html")
        Html_file = open((file_name), "w")
        Html_file.write(self.html_file)
        Html_file.close()
        return file_name

    def load_divs(self, distance_datetime):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="corona_alarm"
        )

        mycursor = db.cursor(buffered=True)
        mycursor2 = db.cursor(buffered=True)
        mycursor.execute("select * from alarms where detected_on='"+ distance_datetime[1] + "';")

        # design issue
        # possibility = "60%"

        for row in mycursor:
            # print(row)
            pid = row[0]
            altitude = row[1]
            longitude = row[2]
            temperature = row[3]
            time_detected = row[6]
            mycursor2.execute("select * from persons where pid=" + str(pid) + " limit 1;")
            for row in mycursor2:
                # print(row)
                first_name = row[1]
                last_name = row[2]
                SVNR = row[4]
                in_blacklist = row[5]
                # print(first_name, last_name,SVNR, in_blacklist )
            #start of the html file
#{direction} in {degree}
#(907.4177354127442, '2021-03-29 19:26:17', 'South', 201.83119608979754)
            custom_html = '<div><h2><span> {detected_on}</span></h2><div style="clear: both; display: table;"><div style="float: left;width: 33.33%; padding: 5px;width: 40%"><img src={thermal_image} alt="Thermal Image" style="width:100%"></div><div style="display: block; float:right;float: left;width: 33.33%; padding: 5px;width: 40%"><img src={py_image} alt="PyImage" style="width:100%"></div></div><div class="data"><p>Name: {first_name} {last_name}</br>Temperature: {temperature}</br>PID: {PID}</br>Possibility: {possibility}</br><span>Blacklist: {in_blacklist}</span></br>Coordinate:  {altitude}, {longitude}</p></div><h3>Your distance to the person:<mark> {distacne} meters</mark> </h3>  <h3>He is on your <mark>{direction}</mark>(<mark>{degree}&deg;</mark>) </h3></div>'.format(
                detected_on=time_detected,
                thermal_image="../images/lep_2021_03_04_T_11_17_08__670.png",
                py_image="../images/cam_2021_03_04_T_11_03_09__302214.jpg",
                first_name=first_name,
                last_name=last_name,
                temperature=temperature,
                PID=pid,
                possibility="60%",
                in_blacklist=in_blacklist,
                altitude=altitude,
                longitude=longitude,
                distacne=int(distance_datetime[0]),
                direction = distance_datetime[2],
                degree = int(distance_datetime[3])
            )
            return custom_html

        mycursor.close()
        mycursor2.close()
    def send_email(self, strFrom, strTo, title):
        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = title
        msgRoot['From'] = strFrom
        msgRoot['To'] = strTo
        msgRoot.preamble = 'Message from Corona Service!'

        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgText = MIMEText(
            'This is the alternative plain text message. Your email provider does not let us to send you iamges in html format! Please visit our website')
        msgAlternative.attach(msgText)

        start_html = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title></head><body><h1 style="color:blueviolet;">Alart Area!</h1><h2 style="color:red;">We believe that you are close to potentially sick people! We kindly ask you to keep your distance from them.</h2><h3>We have already detected an alarm in {min_distance} meters away from you!</h3>'.format(min_distance=self.min_distance)
        divs = ""
        for elemet in self.distance_datetime:
            divs = divs + self.load_email_parts(elemet)

        end_html = '<p>Best regards,<br>Corona Alarm Center</p></body></html>'

        html_to_send_per_email = start_html + divs + end_html
        print(html_to_send_per_email)

        msgText = MIMEText(html_to_send_per_email, 'html')
        msgAlternative.attach(msgText)

        # msgText = MIMEText(
        #     'This is the alternative plain text message. Your email provider does not let us to send you iamges in html format! Please visit our website')
        # msgAlternative.attach(msgText)
        count = 0
        for photo_name in self.images_address_for_email:
            # images / cam_2021_03_04_T_11_03_09__302214.jpg
            photo_name = "images/" + photo_name.split("/")[-1] #TODO FOR GOD SAKE CHANGE THE PATHS!
            print(photo_name)
            with open(photo_name, 'rb') as fp:
                msgImage = MIMEImage(fp.read())
                fp.close()
            msgImage.add_header('Content-ID', '<image' + str(count)+'>')
            msgRoot.attach(msgImage)
            count += 1

        # msgAlternative.attach(msgText)

        # smtp = smtplib.SMTP()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('gholibeigian.k85@htlwienwest.at', 'ybjtbsbouvhifsky')#TODO: use envienment variable here
            smtp.sendmail(strFrom, strTo, msgRoot.as_string())

        # the loop:
        # This example assumes the image is in the current directory
        # fp = open('C:/Users/Jack/PycharmProjects/geolocation_test/test.jpg', 'rb')
        # msgImage = MIMEImage(fp.read())
        # fp.close()
        # # Define the image's ID as referenced above
        # msgImage.add_header('Content-ID', '<image1>')
        # msgRoot.attach(msgImage)

    def load_email_parts(self, distance_datetime):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="corona_alarm"
        )

        mycursor = db.cursor(buffered=True)
        mycursor2 = db.cursor(buffered=True)
        mycursor.execute("select * from alarms where detected_on='" + distance_datetime[1] + "';")

        # design issue
        # possibility = "60%"
        # to solve the problem with <img src="cid:image1"> just for iteration!
        image_num_odd_counter = len(self.images_address_for_email)
        image_num_even_counter = image_num_odd_counter + 1
        for row in mycursor:
            # print(row)
            pid = row[0]
            altitude = row[1]
            longitude = row[2]
            temperature = row[3]
            time_detected = row[6]
            mycursor2.execute("select * from persons where pid=" + str(pid) + " limit 1;")
            for row in mycursor2:
                # print(row)
                first_name = row[1]
                last_name = row[2]
                SVNR = row[4]
                in_blacklist = row[5]
                # print(first_name, last_name,SVNR, in_blacklist )
            # start of the html file
            # {direction} in {degree}
            # (907.4177354127442, '2021-03-29 19:26:17', 'South', 201.83119608979754)
            custom_html = '<div><h2><span> {detected_on}</span></h2><div style="clear: both; display: table;"><div style="float: left;width: 33.33%; padding: 5px;width: 40%"><img src={thermal_image} alt="Thermal Image" style="width:100%"></div><div style="display: block; float:right;float: left;width: 33.33%; padding: 5px;width: 40%"><img src={py_image} alt="PyImage" style="width:100%"></div></div><div class="data"><p>Name: {first_name} {last_name}</br>Temperature: {temperature}</br>PID: {PID}</br>Possibility: {possibility}</br><span>Blacklist: {in_blacklist}</span></br>Coordinate:  {altitude}, {longitude}</p></div><h3>Your distance to the person:<mark> {distacne} meters</mark> </h3>  <h3>He is on your <mark>{direction}</mark>(<mark>{degree}&deg;</mark>) </h3></div>'.format(
                detected_on=time_detected,
                thermal_image='"cid:image'+str(image_num_even_counter)+'"', # ../images/lep_2021_03_04_T_11_17_08__670.png",
                py_image='"cid:image'+str(image_num_odd_counter)+'"',#"../images/cam_2021_03_04_T_11_03_09__302214.jpg",
                first_name=first_name,
                last_name=last_name,
                temperature=temperature,
                PID=pid,
                possibility="60%",
                in_blacklist=in_blacklist,
                altitude=altitude,
                longitude=longitude,
                distacne=int(distance_datetime[0]),
                direction=distance_datetime[2],
                degree=int(distance_datetime[3])
            )
            self.images_address_for_email.append("../images/lep_2021_03_04_T_11_17_08__670.png") #TODO. change with the currect one in db
            self.images_address_for_email.append("../images/cam_2021_03_04_T_11_03_09__302214.jpg")#TODO. change with the currect one in db

            # self.image_num_odd_counter += 2
            # image_num_even_counter += 2
            return custom_html

        mycursor.close()
        mycursor2.close()

if __name__ == "__main__":
    # to use it in a server you should retrieve the current coordinates from database and then use distance_direction_measure.py and pass
    # distance_measurer.distance_datetime as the constructor to the class
    html_generator =  Html_email_generator(100,[(20.96669047875604, '2021-03-29 23:18:48', 'West', 282.25150846134215), (353.48332167934547, '2021-03-29 19:27:32', 'South-West', 230.72028895216073), (907.4177354127442, '2021-03-29 19:26:17', 'South', 201.83119608979754)])
    # file_name_to_send = html_generator.write_file() # wite a html file!
    # print(file_name_to_send)
    html_generator.send_email('gholibeigian.k85@htlwienwest.at','kokolubilubi@gmail.com', 'Critical Situation Detected!')

    # load_iframes()


# m.save("index.html")
# print(pid, altitude,longitude, temperature,time_detected)