from asgiref.sync import sync_to_async
import asyncio
from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message, Chat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope["query_string"]
        query_params = query_string.decode()
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = await self.get_or_create_room()
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        user = self.scope['user']
        if user == AnonymousUser:
            await self.close()
        await self.accept(subprotocol='Token')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']
        await self.save_message(message)
        print(user)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['user'].username
        text = json.dumps({
            'message': message,
            'user': username
        })
        await self.send(text_data=text)

    @sync_to_async
    def get_or_create_room(self):
        room, created = Chat.objects.get_or_create(title=self.room_name)
        return room

    @sync_to_async
    def save_message(self, message):
        print(self.scope['user'].id)
        Message.objects.create(
            creator_id=self.scope['user'],
            chat_id=self.room,
            text=message
        )


