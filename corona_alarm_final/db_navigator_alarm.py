# it has a new method to laod coordinates form alarms table load_data_test_alarms()
import mysql.connector
import locale


class Database_navigator:
    def __init__(self):
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="corona_alarm"
        )
        self.mycursor = self.db.cursor(buffered=True)
    #new
    def insert_into_coordinate(self, altitude, longitude):
        self.mycursor_cordinate = self.db.cursor(buffered=True)
        insert_stmt = (
            "insert into coordinates(altitude, longitude)"
            "VALUES ( %s, %s)"
        )

        # TODO Make hashes from the iamges, then insert into the table!
        val = (altitude,longitude)  #  default value for time is now()!
        print(val)
        try:
            self.mycursor.execute(insert_stmt, val)
            self.db.commit()
        except:
            print("An Error has happened")
            self.db.rollback()
        finally:
            self.mycursor.close()
            self.db.close()
            return self.mycursor.rowcount


        #until here

    def load_data(self, where_clause):
        try:
            # print("select * from alarm " + where_clause)
            self.mycursor.execute("select * from alarm " + where_clause)
            myrow = {}
            for row in self.mycursor:
                # print(row)
                myrow["Alarm id"] = row[0]
                myrow["Altitude"] = row[1]
                myrow["Longitude"] = row[2]
                myrow["Temperature"] = row[3]
                myrow["Possibility"] = row[4]
                myrow["pyImage_hash"] = row[5]
                myrow["thermal_image_hash"] = row[6]
                myrow["Thermal Photo File Name"] = "lep_2021_03_04_T_11_17_09__242.png"
                myrow["Photo File Name"] = "cam_2021_03_04_T_11_03_09__928115.jpg"
                myrow["Alarm Description"] = row[9]
                if row[10] != None:
                    myrow["Detected Date"] = row[10]
                else:
                    myrow["Detected Date"] = "2020/1"

                if row[11] != None:
                    myrow["pid"] = row[11]
                else:
                    myrow["pid"] = "Unknown"

                # export_rows.append(myrow)
            # return export_rows
            return myrow
        finally:
            self.mycursor.close()
            self.db.close()
    #new
    def load_data_test_alarms(self, where_clause):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="corona_alarm"
            )

            mycursor = db.cursor(buffered=True)
            mycursor2 = db.cursor(buffered=True)
            mycursor.execute("select * from alarms;")
            coordinates_alarms = []
            for row in mycursor:
                # print(row)
                pid = row[0]
                altitude = row[1]
                longitude = row[2]
                temperature = row[3]
                time_detected = row[6]
                coordinates_alarm = (float(longitude), float(altitude))
                coordinates_alarms.append((coordinates_alarm, time_detected))

                mycursor2.execute("select * from persons where pid=" + str(pid) + " limit 1;")
                for row in mycursor2:
                    # print(row)
                    first_name = row[1]
                    last_name = row[2]
                    SVNR = row[4]
                    in_blacklist = row[5]
                    # print(first_name, last_name,SVNR, in_blacklist )
            return coordinates_alarms
        finally:
            self.mycursor.close()
            self.db.close()

    def insert_data(self, new_alarm):
        # insert into alarm(alarm_id, altitude, longitude, temperature, possibility, pyImage_hash, termal_imge_hash, pyImage_filename, termal_filename, alarm_description, detected_date, pid)
        # values(1, 44.96, 29.95, 36, 34.9, '374288771172789', '3583142526328348', 'application/excel', 'application/x-troff-msvideo', 'Boa constrictor mexicana', '3/22/2021', 1);
        self.mycursor = self.db.cursor(buffered=True)
        # count_stmt = "select count(alarm_id) from alarm where alarm_id= "+ new_alarm["Alarm id"]
        # self.mycursor.execute(count_stmt)
        # for row in self.mycursor:
        #     print(row)
        insert_stmt = (
            "insert into alarm(altitude, longitude, temperature, possibility, pyImage_hash, "
            "termal_imge_hash, pyImage_filename, termal_filename, alarm_description, detected_date, pid)"
            "VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"
        )

        # TODO Make hashes from the iamges, then insert into the table!
        val = (
        new_alarm["Altitude"],
        new_alarm["Longitude"],
        new_alarm["Temperature"],
        new_alarm["Possibility"],
        new_alarm["pyImage_hash"],
        new_alarm["thermal_image_hash"],
        new_alarm["Thermal Photo File Name"],
        new_alarm["Photo File Name"],
        new_alarm["Alarm Description"],
        new_alarm["Detected Date"],
        new_alarm["pid"])#,      '  person["thermal_image_hash"],        person["pyImage_hash"],
        print(new_alarm)
        try:
            self.mycursor.execute(insert_stmt, val)
            self.db.commit()
        except :
            print("An Error has happened")
            self.db.rollback()
        finally:
            self.mycursor.close()
            self.db.close()
            return self.mycursor.rowcount

    def update_row(self, new_alarm):
        self.mycursor = self.db.cursor(buffered=True)
        sql = "UPDATE ALARM SET altitude=%s, longitude=%s,  temperature=%s, possibility=%s, pyImage_hash=%s, termal_imge_hash=%s, " \
              "pyImage_filename=%s, termal_filename=%s, alarm_description=%s, detected_date=%s, " \
              "pid=%s WHERE alarm_id=%s;"
        val = (
        new_alarm["Altitude"],
        new_alarm["Longitude"],
        new_alarm["Temperature"],
        new_alarm["Possibility"],
        new_alarm["pyImage_hash"],
        new_alarm["thermal_image_hash"],
        new_alarm["Photo File Name"],
        new_alarm["Thermal Photo File Name"],

        new_alarm["Alarm Description"],
        new_alarm["Detected Date"],
        new_alarm["pid"],
        new_alarm["Alarm id"])#,      '  person["thermal_image_hash"],        person["pyImage_hash"],

        # TODO Make hashes from the iamges, then insert into the table!
        print(new_alarm)
        self.mycursor.execute(sql, val)

        try:
            self.db.commit()
        except:
            # Rolling back in case of error
            self.db.rollback()
        finally:
            self.mycursor.close()
            self.db.close()
            return self.mycursor.rowcount


    def load_last_coordinate(self):
        try:
            # print("select * from alarm " + where_clause)
            # self.mycursor.execute("select * from alarm " + where_clause)
            coordinate_cursor = self.db.cursor(buffered=True)
            coordinate_cursor.execute("select max(time_id), altitude, longitude from coordinates;")
            myrow = {}
            for row in coordinate_cursor:
                # print(row)
                last_altitude = row[1]
                last_longitude = row[2]
                return last_altitude,last_longitude
                # export_rows.append(myrow)
            # return export_rows
            return myrow
        finally:
            self.mycursor.close()
            self.db.close()





