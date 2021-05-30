# TODO: merge it with led_enabler! and make it a class!
# I merged it with load_polygon.py it will be the load_iframes(self)
#        x.load_iframes()
#    x.generate_index_html_marker_polygon()
import locale

import datetime
import mysql.connector
import folium
m = folium.Map(location=[48.208176, 16.373819],tiles="OpenStreetMap", zoom_start=15)

def load_iframes():
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
            thermal_image="images/lep_2021_03_04_T_11_17_08__670.png",
            py_image="images/cam_2021_03_04_T_11_03_09__302214.jpg",
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
        file_name = "html_files/" + datetime.datetime.strftime(time_detected,"%Y_%m_%d_T_%I_%M_%S__%f.html")
        Html_file= open((file_name),"w")
        Html_file.write(custom_html)
        Html_file.close()
        folium.Marker(location=[altitude, longitude],
                      popup="<html><body><iframe frameBorder='0' width='400px' height='%d px' src='%s'></iframe></body></html>" % (
                      400, file_name),
                      tooltip="Click for more information"
                      ).add_to(m)

    mycursor.close()
    mycursor2.close()
load_iframes()


m.save("index.html")
# print(pid, altitude,longitude, temperature,time_detected)