from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def room(request, room_name, name):
    return render(request, "main/room.html", {"room_name": room_name, "name": name})


@login_required
def talk_list(request):
    return render(request, "main/talk_list.html")
