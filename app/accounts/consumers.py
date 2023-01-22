import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import CustomUser, Friend
from chat.models import chat_roomModel, room_userModel
import base64

from app.settings import MEDIA_ROOT


class Profile(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        await self.accept()

        result = await self.save_entry()

        img_data = bytes(str(self.user.thumbnail), "utf-8")
        b64_data = str(base64.b64encode(img_data))

        data_json = {
            "username": self.user.username,
            "email": self.user.email,
            "thumbnail": b64_data,
            "user_status": result,
            "comment": self.user.comment,
        }
        await self.send(text_data=json.dumps(data_json))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if "submit" == text_data_json.get("data_type"):

            image = text_data_json.get("image")

            await self.save(text_data_json)
            data_json = {"data_type": "reload"}
            await self.send(text_data=json.dumps(data_json))

    @database_sync_to_async
    def save_entry(self):
        result = CustomUser.objects.get(id=self.user.id)

        user_status = CustomUser._meta.get_field("user_status").choices

        for i in user_status:

            if i[0] == result.user_status:

                status = i[1]
                return status

        status = user_status[0][1]
        result.user_status = "A"

        return status

    @database_sync_to_async
    def save(self, data):
        a = CustomUser.objects.get(id=self.user.id)
        if data.get("image"):
            encoded_file = "./media_local/images/thumbnail/" + str(a.id) + ".jpg"

            with open(encoded_file, mode="wb") as f:
                jpg = base64.b64decode(data.get("image"))
                f.write(jpg)

            a.thumbnail = encoded_file

        if data.get("name") != "":
            a.username = data.get("name")

        if data.get("email") != "":
            a.email = data.get("email")

        if data.get("comment") != "":
            a.comment = data.get("comment")

        if data.get("status") != "":
            a.user_status = data.get("status")

        a.save()


class Friend_profile(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if "body_onload" == text_data_json.get("data_type"):

            user = text_data_json.get("user_id")
            data_json = await self.find(user)
            await self.send(text_data=json.dumps(data_json))
        if "add" == text_data_json.get("data_type"):
            follower = text_data_json.get("friend_name")
            await self.follo(follower)
        if "talk" == text_data_json.get("data_type"):

            friend = text_data_json.get("friend_name")
            data_json = await self.talk(friend)

            await self.send(text_data=json.dumps(data_json))

    @database_sync_to_async
    def talk(self, friend):
        def create_new_room():

            new_room = chat_roomModel()
            new_room.room_name = self.user.username + "-" + friend
            new_room.save()

            self_room = room_userModel()
            self_room.room_id = new_room
            self_room.user_id = self.user
            self_room.save()

            friend_room = room_userModel()
            friend_room.room_id = new_room
            friend_room.user_id = CustomUser.objects.get(username=friend)
            friend_room.save()

            data_json = {
                "data_type": "talk",
                "room_name": new_room.room_name,
                "user_name": self.user.username,
            }
            return data_json

        roomName = self.user.username + "-" + friend

        roomName2 = friend + "-" + self.user.username
        try:
            find_room = chat_roomModel.objects.get(room_name=roomName)
            data_json = {
                "data_type": "talk",
                "room_name": find_room.room_name,
                "user_name": self.user.username,
            }
            return data_json
        except Exception as e:
            print(e)

        try:

            find_room2 = chat_roomModel.objects.get(room_name=roomName2)

            data_json = {
                "data_type": "talk",
                "room_name": find_room2.room_name,
                "user_name": self.user.username,
            }
            return data_json
        except Exception as e:

            print(e)

            result = create_new_room()
            return result

    @database_sync_to_async
    def find(self, user):
        friend = CustomUser.objects.get(username=user)

        result = friend.user_status
        img_data = bytes(str(friend.thumbnail), "utf-8")
        b64_data = str(base64.b64encode(img_data))
        if result == "A":
            result = "online"
        else:
            result = "offline"
        data_json = {
            "username": friend.username,
            "email": friend.email,
            "thumbnail": b64_data,
            "user_status": result,
            "comment": friend.comment,
        }
        return data_json

    @database_sync_to_async
    def follo(self, follower):
        follower_id = CustomUser.objects.get(username=follower)
        try:
            Me = Friend.objects.get(follo_id=self.user, follower_id=follower_id.id)

        except:
            saverecord = Friend()
            saverecord.follo_id = self.user
            saverecord.follower_id = follower_id.id
            saverecord.status = "A"
            saverecord.save()

        try:
            friend = Friend.objects.get(follo_id=follower_id, follower_id=self.user.id)

            if friend.status == "A" and Me.status == "A":
                friend.relation = True
                Me.relation = True
                friend.save()
                Me.save()
        except Exception as e:
            print(e)
        else:
            print("new friend\nfinish")
        try:
            friend = Friend.objects.get(follo_id=follower_id, follower_id=self.user.id)

            if friend.status == "A" and saverecord.status == "A":
                friend.relation = True
                saverecord.relation = True
                friend.save()
                saverecord.save()
        except Exception as e:
            print(e)

        else:
            print("new friend\nnew data save\nfinish")


class Friend_List(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        await self.accept()
        data_json = await self.find_friend()

        await self.send(text_data=json.dumps(data_json))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        result = await self.friend(text_data_json)
        await self.send(text_data=json.dumps(result))

    @database_sync_to_async
    def find_friend(self):
        friend_list = Friend.objects.filter(follower_id=self.user.id)
        friend_list_num = friend_list.count()

        result = {}

        for i in range(0, friend_list_num):
            if friend_list[i].relation == True:
                result[i] = friend_list[i].follo_id.id

        result_num = len(result)

        friend_name_list = {"name_list": {}, "img_list": {}}
        for i in range(0, result_num):

            friend = CustomUser.objects.get(id=result[i])

            friend_name_list["name_list"][i] = friend.username

            img_data = bytes(str(friend.thumbnail), "utf-8")
            b64_data = str(base64.b64encode(img_data))
            friend_name_list["img_list"][i] = b64_data

        return friend_name_list

    @database_sync_to_async
    def friend(self, text_data_json):
        friend = CustomUser.objects.get(username=text_data_json.get("input_name"))
        img_data = bytes(str(friend.thumbnail), "utf-8")
        b64_data = str(base64.b64encode(img_data))
        data_json = {
            "data_type": "find_friend",
            "friend_name": friend.username,
            "thumbnail": b64_data,
        }
        return data_json
