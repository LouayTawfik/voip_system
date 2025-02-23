import os
from twilio.rest import Client


class VoiceCallHandler:
    def __init__(self):
        self.account_sid = os.environ['TWILIO_ACCOUNT_SID']
        self.auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
        if not all([self.account_sid, self.auth_token, self.twilio_number]):
            raise ValueError("Missing required Twilio credentials in .env file")
        self.client = Client(self.account_sid, self.auth_token)