from django.urls import path
from . import views

urlpatterns = [
    path('send-message/', views.send_message, name='send_message'),
    path('get-chat-history/', views.get_chat_history, name='get_chat_history'),
    path('get-response-from-rag/', views.generate_response_view, name='generate_response_view'),
    path('load-pdf/', views.load_pdf, name='load_pdf'),
]
