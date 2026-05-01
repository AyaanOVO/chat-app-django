from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:user1>/<str:user2>/', ChatConsumer.as_asgi()),
]