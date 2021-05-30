# Download the helper library from https://www.twilio.com/docs/python/install
# it sends an sms to the user when he is closer than 20 meters to the alarm!
import locale

import os
from twilio.rest import Client

class Sms_send:
    def __init__(self, message):
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform

        self.message = message
        account_sid = "AC0a369211dcc1a462fe3df985c91342d3"  # os.environ['TWILIO_ACCOUNT_SID']#TODO: use envienment variable here
        auth_token = "71fb72857c0741d20c88076af45a5d5c"  # os.environ['TWILIO_AUTH_TOKEN']#TODO: use envienment variable here
        self.client = Client(account_sid, auth_token)
    def send_sms(self, to_num='+436769651423'):
        message = self.client.messages \
            .create(
            body=self.message,
            from_='+13152845608',
            to=to_num
        )
        print(message.sid)

if __name__ == "__main__":
    sms = Sms_send("\nWe have detected a sick person closer than 20 meters from you!\nPlease check your email for more information.\nBest regards,\nCorona Alarm Center")
    sms.send_sms()