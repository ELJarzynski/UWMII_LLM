from django.urls import path
from . import views

urlpatterns = [
    path('send-message/', views.send_message, name='send_message'),
    path('get-response/', views.get_response, name='get_response'),
    path('get-chat-history/', views.get_chat_history, name='get_chat_history'),
]
