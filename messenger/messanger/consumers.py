from asgiref.sync import sync_to_async
import asyncio
from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message, Chat
from .serializers import MessagesSerializer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope["query_string"]
        query_params = query_string.decode()
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = await self.get_or_create_room()
        self.user = self.scope['user']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )


        if self.user == AnonymousUser:
            await self.close()
        await self.accept(subprotocol='Token')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'chat_message':
            # Обработка нового сообщения
            message = await self.create_message(data['message'])
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message.text,
                    'id': message.id,
                    'sender': self.user.username,
                }
            )

        elif message_type == 'edit_message':
            # Обработка редактирования
            message = await self.edit_message_in_db(data['message_id'], data['new_text'])
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'edit_message',
                    'message': message.text,
                    'id': message.id,
                    'sender': self.user.username,
                }
            )

        elif message_type == 'delete_message':
            # Обработка удаления
            await self.delete_message_in_db(data['message_id'])
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'delete_message',
                    'id': data['message_id'],
                }
            )

        elif message_type == 'get_history':
            # Отправка истории сообщений
            messages = await self.get_messages()
            send_data = json.dumps({
                'type': 'history',
                'messages': messages
            })
            await self.send(text_data=send_data)

    async def chat_message(self, event):
        text = json.dumps({
            'type': 'message',
            'message': event['message'],
            'id': event['id'],
            'sender': event['sender']
        })
        await self.send(text_data=text)

    async def edit_message(self, event):
        text = json.dumps({
            'type': 'message_update',
            'new_text': event['message'],
            'id': event['id'],
            'sender': event['sender']
        })
        await self.send(text_data=text)

    async def delete_message(self, event):
        message = json.dumps({
            'type': 'delete_message',
            'id': event['id'],
        })
        await self.send(text_data=message)

    @sync_to_async
    def get_or_create_room(self):
        room, created = Chat.objects.get_or_create(id=self.room_name)
        return room

    @sync_to_async
    def create_message(self, message):
        message = Message.objects.create(
            creator_id=self.scope['user'],
            chat_id=self.room,
            text=message
        )
        message.save()
        return message

    @database_sync_to_async
    def edit_message_in_db(self, message_id, new_text):
        message = Message.objects.get(chat_id=self.room_name,
                                      id=message_id,
                                      creator_id=self.user)
        message.text = new_text
        message.save()
        return message
    @database_sync_to_async
    def get_messages(self):
        messages = Message.objects.filter(chat_id=self.room_name)
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



