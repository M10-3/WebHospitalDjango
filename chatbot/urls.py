from django.urls import path
from .views import chatbot_response, chatbot_audio


urlpatterns = [
   path('api/', chatbot_response, name='chatbot_response'),
    path('audio/', chatbot_audio, name='chatbot_audio'),
]
