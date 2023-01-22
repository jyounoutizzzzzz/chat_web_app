from django.db import models
from django.contrib.auth import get_user, get_user_model
import uuid

# Create your models here.

User = get_user_model()


class chat_roomModel(models.Model):
    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_name = models.CharField(max_length=50)
    update_at = models.DateTimeField(auto_now=True)


class room_userModel(models.Model):
    room_id = models.ForeignKey(chat_roomModel, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now=True)


class messageModel(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.CharField(max_length=50)
    posted_user = models.ForeignKey(room_userModel, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now=True)


class message_statusModel(models.Model):
    message_id = models.ForeignKey(messageModel, on_delete=models.CASCADE)
    read_status = models.BooleanField(default=False)
    read_count = models.IntegerField(default=0)
