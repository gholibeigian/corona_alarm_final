# corona_alarm_final
Windows Server GUI
Dear Prof. Kerer, 

The Thesis is in two different folder(part)
1. the model trainer for the face recognition (main.py will save the .yml model file in the project)
2. the project 

In the project there are two mains(main.py and main_wxPython.py). File mian.py has dead lock issue with 
https://github.com/cztomczak/cefpython/issues/441
It seems, when you use tkinter 8.4 or an older version of it the problem wont accure.

Main_wxPython works just fine and it does not have the issue with the deadlock!

in coronal_alarm_final project:

-> alarm_iamges: the files will be downloaded to this folder using file_server.py
-> emails: emails to send to the user will be generated here using html_emali_generator.py!
-> html_files: is there to give css and js functionality to the map iframes(Alarms marker in the map) and for the emails 
-> images: When you save an alarm or a person, the files will be copied in this folder
-> models: When you train a model, you can copy the trainer.yml in there(you can train a model in "face recognizer trainer"-> faces_train.py). corona_alarm.py will use the trainer.yml to recognize the person
-> polygon_geojason: you can find red and yellow geojason files there. chrome_driver -> you find the driver for selenium webbrowser


in raspberry project:
client.py to test the alarm_server.py(the small window on start the main_wxPython.py)
playground_gps_client_tcp.py -> to test the functionality of the gps_server
playground_email_client_tcp.py-> to test the functionality of the email_server
Server_playground2_final_raspberry.py is the file server on the raspberry pi, but you can use it to test the functionality of the file_server.py in corona_alarm_final project(It find the closest date_file of pyImages and thermal images and send them to the server on windows(corona_alarm_final)
oit_raspberry.py is the controller of the leds and the button and the lcd on the raspberry
