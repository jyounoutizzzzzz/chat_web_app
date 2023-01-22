from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("<str:room_name>?name=<str:name>", views.room, name="room"),
    path("talk_list/", views.talk_list, name="talk_list"),
]
