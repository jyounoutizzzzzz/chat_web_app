from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    path('ws/profile/', consumers.Profile.as_asgi()),
    path('ws/friend/', consumers.Friend_profile.as_asgi()),
    path('ws/friend_list/',consumers.Friend_List.as_asgi()),
]