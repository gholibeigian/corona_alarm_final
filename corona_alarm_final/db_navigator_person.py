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

    def load_data(self, where_clause):
        try:
            self.mycursor.execute("select * from persons " + where_clause)
            export_rows = []
            for row in self.mycursor:
                pid  = row[0]
                altitude = row[1]
                # longitude =
                print(row)
                pid = row[0]
                first_name = row[1]
                last_name = row[2]
                SVNR = row[4]
                in_blacklist = row[5]
                # TODO change the gender and file names
                gender = 1
                birth_date = row[6]
                tel = row[7]
                address = row[8]
                email= row[9]
                pyImage = row[10]
                thermal_image = row[11]
                # thermal_file_name = row[12]
                # pyImage_file_name = row[13]
                thermal_file_name = "lep_2021_03_04_T_11_17_09__242.png"
                pyImage_file_name = "cam_2021_03_04_T_11_03_09__928115.jpg"
                # myrow = {
                #     "First Name" : "",
                #     "Last Name",
                #     "SVNR",
                #     "Birth Date",
                #     "Email",
                #     "Phone",
                #     "Address",
                #     "PID",
                #     "Thermal Photo File Name",
                #     "Photo File Name",
                #     "thermal_image_hash",
                #     "pyImage_hash"
                # }
                myrow = {}
                myrow["First Name"] = first_name
                myrow["Last Name"] = last_name
                myrow["SVNR"] =  SVNR
                myrow["Birth Date"] =  birth_date
                myrow["Email"] = email
                myrow["Phone"] = tel
                myrow["Address"] = address
                myrow["PID"] = pid
                myrow["Thermal Photo File Name"] = "lep_2021_03_04_T_11_17_09__242.png"
                myrow["Photo File Name"] = "cam_2021_03_04_T_11_03_09__928115.jpg"
                myrow["thermal_image_hash"] = thermal_image
                myrow["pyImage_hash"] = pyImage
                myrow["Gender"] = gender # chage
                myrow["in_blacklist"] = in_blacklist
                export_rows.append(myrow)
            self.mycursor
            return export_rows
                    # print(first_name, last_name,SVNR, in_blacklist )
                # print(pid, altitude, longitude, temperature, time_detected)
            #return rows
        finally:
            self.mycursor.close()
            self.db.close()

    def insert_data(self, person):
        # insert
        # into
        # persons(pid, first_name, last_name, gender, SVNR, in_blacklist, Birth_date, tel, Address, email, pyimage,
        #         termal_image)
        # values(1, 'Simonne', 'Mabson', 'Non-binary', '68788-9805', false, '3/1/2021', '174-715-3967',
        #        '24 Thierer Point', 'smabson0@sakura.ne.jp', 'EE82 5830 5923 6685 4110',
        #        'PT96 4914 4678 3110 1393 9151 2');
        self.mycursor = self.db.cursor(buffered=True)

        insert_stmt = (
            "INSERT INTO persons( first_name, last_name, gender, SVNR, in_blacklist, Birth_date, tel, Address, email, pyimage, termal_image)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )

        val = (person["First Name"],
        person["Last Name"],
        person["Gender"],
        person["SVNR"],
        person["in_blacklist"],
        person["Birth Date"],
        person["Phone"],
        person["Address"],
        person["Email"],
        person["Photo File Name"],
        person["Thermal Photo File Name"])#,        person["thermal_image_hash"],        person["pyImage_hash"],
        try:
            self.mycursor.execute(insert_stmt, val)
            self.db.commit()

        except:
            # Rolling back in case of error
            self.db.rollback()
        finally:
            self.mycursor.close()
            self.db.close()
            return self.mycursor.rowcount


    def update_row(self, person):
        self.mycursor = self.db.cursor(buffered=True)

        sql = "UPDATE PERSONS SET first_name=%s, last_name=%s,  gender=%s, SVNR=%s, in_blacklist=%s, Birth_date=%s, " \
              "tel=%s, Address=%s, email=%s, pyimage=%s, " \
              "termal_image=%s WHERE pid=%s;"

        val = (person["First Name"],
        person["Last Name"],
        person["Gender"],
        person["SVNR"],
        person["in_blacklist"],
        person["Birth Date"],
        person["Phone"],
        person["Address"],
        person["Email"],
        person["Photo File Name"],
        person["Thermal Photo File Name"],
        person["PID"])#,        person["thermal_image_hash"],        person["pyImage_hash"],
        try:
            self.mycursor.execute(sql, val)
            self.db.commit()
        except:
            # Rolling back in case of error
            self.db.rollback()
        finally:
            self.mycursor.close()
            self.db.close()
            return self.mycursor.rowcount
        # print(self.mycursor2.rowcount, "record(s) affected")
