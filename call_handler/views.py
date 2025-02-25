from django.http import HttpResponse
from twilio.twiml.voice_response import VoiceResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from voice_call_app import VoiceCallHandler
import redis
import logging
import os

logger = logging.getLogger(__name__)

redis_client = redis.Redis(
    host=os.environ['REDIS_HOST'],
    port=os.environ['REDIS_PORT'],
    db=os.environ['REDIS_db'],
    decode_responses=os.environ['REDIS_DECODE_RESPONSE']
)

voice_app = VoiceCallHandler()


@csrf_exempt
@require_POST
def voice_webhook(request):
    message_id = request.GET.get('message_id')
    message = redis_client.get(message_id)

    twiml = voice_app.get_call_twiml(message)

    return HttpResponse(twiml, content_type='text/xml')


@csrf_exempt
@require_POST
def handle_recording(request):
    """
    Handle the webhook after a recording is completed.
    
    This view receives the webhook after the caller leaves a message
    and responds with TwiML instructions for what to do next.
    """
    # Extract recording information from the request
    recording_sid = request.POST.get('RecordingSid')
    recording_url = request.POST.get('RecordingUrl')
    
    if recording_sid:
        print(f"Recording completed with SID: {recording_sid}")
        print(f"Recording URL: {recording_url}")
        
        recording_details = voice_app.handle_recording_completed(recording_sid)
    
    # Respond with TwiML to end the call
    response = VoiceResponse()
    response.say("Thank you for your message. Goodbye.", voice='alice')
    response.hangup()
    
    return HttpResponse(str(response), content_type='text/xml')