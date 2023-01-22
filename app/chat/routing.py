from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/chat/<str:room_name>/", consumers.test_ChatConsumer.as_asgi()),
    path("ws/list/", consumers.chat_room_list.as_asgi()),
]
