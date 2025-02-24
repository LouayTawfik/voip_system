import os
import argparse
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VoiceCallHandler:
    def __init__(self):
        self.account_sid = os.environ['TWILIO_ACCOUNT_SID']
        self.auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.twilio_number = os.environ['TWILIO_PHONE_NUMBER']
        if not all([self.account_sid, self.auth_token, self.twilio_number]):
            raise ValueError("Missing required Twilio credentials in .env file")
        self.client = Client(self.account_sid, self.auth_token)

    def initiate_call(self, to_number):
        try:
            call = self.client.calls.create(
                to=to_number,
                from_=self.twilio_number,
                url='http://demo.twilio.com/docs/voice.xml',
                record=True
            )
            return True, call.sid
        except TwilioRestException as e:
            logger.error(f"Twilio error: {str(e)}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
        return False, str(e)
    
def main():
    parser = argparse.ArgumentParser(description='Voice Call App')
    parser.add_argument('-n', '--number', required=True, help='Recipient phone number (include country code)')
    parser.add_argument('-m', '--message', help='Optional message to play')

    args = parser.parse_args()

    try:
        handler = VoiceCallHandler()
        success, result = handler.initiate_call(args.number)

        if success:
            print(f"Call initiated successfully! Call SID: {result}")
        else:
            print(f"Failed to initiate call: {result}")
    except Exception as e:
        print(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()