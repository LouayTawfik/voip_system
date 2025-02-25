from django.urls import path
from . import views

app_name = 'call_handler'

urlpatterns = [
    path('', views.voice_webhook, name='voice_webhook'),
    path('handle-recording/', views.handle_recording, name='handle_recording')
]
