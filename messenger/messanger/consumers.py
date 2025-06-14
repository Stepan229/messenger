from asgiref.sync import sync_to_async
import asyncio
from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message, Chat
from .serializers import MessagesSerializer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.required_fields = {
            'new_message': ['message'],
            'edit_message': ['message_id', 'new_text'],
            'delete_message': ['message_id']
        }
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        if not self.check_room_access():
            await self.close(code=4001)
            return

        self.room = await self.get_or_create_room()
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept(subprotocol='Token')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send_error("Invalid JSON format")
        else:
            message_type = data.get('type')

            if not await self.validate_message(data, message_type):
                return

            handler = getattr(self, f'handle_{message_type}', None)
            if handler:
                await handler(data)
            else:
                await self.send_error(f"Unknown message type: {message_type}")

    async def send_message(self, data):
        text = json.dumps(data['data'])
        await self.send(text_data=text)

    async def handle_get_history(self, data):
        messages = await self.get_messages_in_db()
        send_data = json.dumps({
                    'type': 'history',
                    'messages': messages
                })
        await self.send(text_data=send_data)

    async def handle_new_message(self, data):
        message = await self.create_message_in_db(data['message'])
        await self.broadcast_message({
             'type': 'new_message',
             'message': message.text,
             'id': message.id,
             'sender': self.user.username,
        })

    async def handle_edit_message(self, data):
        message = await self.edit_message_in_db(data['message_id'], data['new_text'])
        await self.broadcast_message({
             'type': 'message_update',
             'new_text': message.text,
             'id': message.id,
        })

    async def handle_delete_message(self, data):
        await self.delete_message_in_db(data['message_id'])
        await self.broadcast_message({
                'type': 'delete_message',
                'id': data['message_id'],
        })

    async def broadcast_message(self, message_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_message',
                'data': message_data
            })

    async def send_error(self, error_message):
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': error_message
        }))

    async def check_room_access(self):
        # добавить проверку прав доступа к комнате
        return True

    async def validate_message(self, data, message_type):
        if message_type in self.required_fields.keys():
            if not all(field in data for field in self.required_fields[message_type]):
                await self.send_error(f"Missing fields for {message_type}")
                return False
        return True

    @database_sync_to_async
    def get_or_create_room(self):
        room, created = Chat.objects.get_or_create(id=self.room_name)
        return room

    @database_sync_to_async
    def create_message_in_db(self, message):
        message = Message.objects.create(
            creator_id=self.scope['user'],
            chat_id=self.room,
            text=message
        )
        message.save()
        return message

    @database_sync_to_async
    def edit_message_in_db(self, message_id, new_text):
        message = Message.objects.get(
            chat_id=self.room_name,
            id=message_id,
            creator_id=self.user)
        message.text = new_text
        message.save()
        return message

    @database_sync_to_async
    def get_messages_in_db(self):
        messages = Message.objects.filter(chat_id=self.room_name).select_related('creator_id')
        messages = [
                {
                    'id': msg.id,
                    'sender': msg.creator_id.username,
                    'text': msg.text,
                    'created_at': msg.time_create.isoformat(),
                    'read': msg.is_read
                }
                for msg in messages
            ]
        return messages

    @database_sync_to_async
    def delete_message_in_db(self, message_id):
        message = Message.objects.get(chat_id=self.room_name,
                                      id=message_id,
                                      creator_id=self.user)
        message.delete()



