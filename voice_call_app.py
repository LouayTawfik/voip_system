import os
import argparse
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from twilio.twiml.voice_response import VoiceResponse
import redis
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
            raise ValueError("Missing required Twilio credentials.")

        self.client = Client(self.account_sid, self.auth_token)

        self.webhook_url = os.environ.get('WEBHOOK_URL', 'http://demo.twilio.com/docs/voice.xml')

        self.redis_client = redis.Redis(
            host=os.environ['REDIS_HOST'],
            port=os.environ['REDIS_PORT'],
            db=os.environ['REDIS_db'],
            decode_responses=os.environ['REDIS_DECODE_RESPONSE']
        )
        logger.info("Connected to Redis.")

    def store_message(self, message):
        message_id = f"msg_{self.redis_client.incr('message_counter')}"

        self.redis_client.set(message_id, message)
        logger.info(f"Message stored in Redis with ID: {message_id}")
        
        return message_id

    def retrieve_message(self, message_id):
        message = self.redis_client.get(message_id)
        if message:
            logger.info(f"Retrieved message from Redis: {message_id}")
            return message
        logger.warning(f"Message not found in Redis: {message_id}")
        return None


    def initiate_call(self, to_number, message):
        try:
            if message:
                message_id = self.store_message(message)
                webhook_url = f'https://d806-156-209-77-128.ngrok-free.app/{self.webhook_url}?message_id={message_id}'

            call = self.client.calls.create(
                to=to_number,
                from_=self.twilio_number,
                url=webhook_url if message else f'https://d806-156-209-77-128.ngrok-free.app/{self.webhook_url}',
                record=True,
                recording_channels='mono'
            )
            return True, call.sid, call.status

        except TwilioRestException as e:
            logger.error(f"Twilio error: {str(e)}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return False, str(e)


    def get_call_twiml(self, message=None):
        """
        TwiML (the Twilio Markup Language) is a set of instructions you can use
        to tell Twilio what to do when you receive an incoming call or SMS.
        """
        response = VoiceResponse()
        
        if message:
            response.say(message, voice='man')
            response.pause(length=1)

        response.say("Please leave a message after the tone. Press # when finished.", voice='man')
        response.record(
            timeout=10,
            max_length=60,
            finish_on_key='#',
            action=f"https://d806-156-209-77-128.ngrok-free.app/{self.webhook_url}handle-recording/"
        )
        return str(response)


    def handle_recording_completed(self, recording_sid):
        """
        Handle the callback when recording is completed.
        """
        recording = self.client.recordings(recording_sid).fetch()
        
        print(f"Message recorded successfully")
        
        return {
            'sid': recording.sid,
            'url': recording.uri,
            'duration': recording.duration
        }


def main():
    parser = argparse.ArgumentParser(description='Voice Call App')
    parser.add_argument('-n', '--number', required=True, help='Recipient phone number (include country code)')
    parser.add_argument('-m', '--message', help='Optional message to play')

    args = parser.parse_args()

    try:
        handler = VoiceCallHandler()
        if args.message:
            success, call_sid, call_status = handler.initiate_call(args.number, args.message)
        else:
            success, call_sid, call_status = handler.initiate_call(args.number)

        if success:
            print(f"Call initiated successfully! Call SID: {call_sid}")
            print(f"Call status is: {call_status}")
        else:
            print(f"Failed to initiate call: {call_sid}")
    except Exception as e:
        print(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()