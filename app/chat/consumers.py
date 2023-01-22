import json
from channels.generic.websocket import AsyncWebsocketConsumer


from channels.db import database_sync_to_async

from chat.models import (
    chat_roomModel,
    room_userModel,
    messageModel,
    message_statusModel,
)

import base64
import re


class test_ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        self.user = self.scope["user"]

        result = await self.find_user()
        if result:

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            await self.accept()

        friend_img = await self.load_img()
        friend_img_data = bytes((friend_img), "utf-8")
        friend_b64_data = str(base64.b64encode(friend_img_data))
        img_data = bytes(str(self.user.thumbnail), "utf-8")
        b64_data = str(base64.b64encode(img_data))
        data_json = {
            "datatype": "load_image",
            "self-image": b64_data,
            "friend-image": friend_b64_data,
        }
        await self.send(text_data=json.dumps(data_json))
        chatlog, chatlog_count, chatlog_users = await self.load_log()

        await self.send_log(chatlog, chatlog_count, chatlog_users)

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        data_json = await self.save_message(message)

        await self.channel_layer.group_send(self.room_group_name, data_json)

    async def chat_message(self, event):

        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "posted_user": event["posted_user"],
                    "posted_at": event["posted_at"],
                    "read_status": event["read_status"],
                    "read_count": event["read_count"],
                }
            )
        )

    @database_sync_to_async
    def find_user(self):

        try:

            room = chat_roomModel.objects.get(room_name=self.room_name)
            user = room_userModel.objects.get(room_id=room, user_id=self.user)
        except:
            return False
        return True

    @database_sync_to_async
    def save_message(self, message):
        room = chat_roomModel.objects.get(room_name=self.room_name)
        posted_user = room_userModel.objects.get(user_id=self.user.id, room_id=room)
        new_message = messageModel()
        new_message.message = message
        new_message.posted_user = posted_user
        new_message.save()
        message_status = message_statusModel()
        message_status.message_id = new_message
        message_status.save()

        data_json = {
            "type": "chat_message",
            "message": new_message.message,
            "posted_user": self.user.username,
            "posted_at": str(new_message.posted_at),
            "read_status": message_status.read_status,
            "read_count": message_status.read_count,
        }
        return data_json

    @database_sync_to_async
    def load_log(self):
        room = chat_roomModel.objects.get(room_name=self.room_name)
        posted_user = room_userModel.objects.filter(room_id=room).all()
        posted_user_count = room_userModel.objects.filter(room_id=room).count()

        chat_log = []
        chat_log_count = []
        chat_log_users = {}
        for i in range(posted_user_count):
            chat_log.append(
                list(messageModel.objects.filter(posted_user=posted_user[i]).values())
            )
            chat_log_count.append(
                messageModel.objects.filter(posted_user=posted_user[i]).count()
            )

            pattern = r"room_userModel object \((\d*)\)$"
            result = re.match(pattern, str(posted_user[i]))

            chat_log_users[int(result.group(1))] = posted_user[i].user_id.username

        return chat_log, chat_log_count, chat_log_users

    async def send_log(self, log, count, users):

        log_list = log[0]

        if len(count) > 1:
            for i in range(1, len(count)):
                for n in range(len(log[i])):
                    log_list.append(log[i][n])

            result = sorted(log_list, key=lambda x: x["posted_at"])

            for i in range(len(log_list)):

                data_json = {
                    "message": result[i]["message"],
                    "posted_user": users[int(result[i]["posted_user_id"])],
                    "posted_at": str(result[i]["posted_at"]),
                }
                await self.send(text_data=json.dumps(data_json))

        else:
            for i in range(len(log_list)):
                data_json = {
                    "message": log_list[i]["message"],
                    "posted_user": users[int(result[i]["posted_user_id"])],
                    "posted_at": str(result[i]["posted_at"]),
                }
                await self.send(text_data=json.dumps(data_json))

    @database_sync_to_async
    def load_img(self):
        room = chat_roomModel.objects.get(room_name=self.room_name)
        user = room_userModel.objects.filter(room_id=room).exclude(user_id=self.user)

        return str(user[0].user_id.thumbnail)


class chat_room_list(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        await self.accept()
        data_json = await self.load_log()
        await self.send(text_data=json.dumps(data_json))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass

    @database_sync_to_async
    def load_log(self):
        room_list = room_userModel.objects.filter(user_id=self.user)
        room_list_count = room_userModel.objects.filter(user_id=self.user).count()
        log_list = {
            "name_list": {},
            "img_list": {},
            "room_list": {},
            "self_name": {0: self.user.username},
        }
        for i in range(room_list_count):
            log = room_userModel.objects.filter(room_id=room_list[i].room_id).exclude(
                user_id=self.user
            )

            log_list["name_list"][i] = log[0].user_id.username

            img_data = bytes(str(log[0].user_id.thumbnail), "utf-8")
            b64_data = str(base64.b64encode(img_data))
            log_list["img_list"][i] = b64_data

            log_list["room_list"][i] = log[0].room_id.room_name

        return log_list
