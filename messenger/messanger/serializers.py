from django.contrib.auth.base_user import BaseUserManager
from rest_framework import serializers
from django.db import connection
from .models import Message, Chat, UserChat
from django.conf import settings
from .utils import get_and_check_users

from django.contrib.auth import get_user_model
User = get_user_model()

class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('creator_id', 'chat_id', 'time_create')

    def create(self, validated_data):
        user = self.context['user']
        chat = self.context['chat']
        message = Message.objects.create(creator_id=user, chat_id=chat, text=validated_data['text'])
        return message

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'title', 'time_create']
        read_only_fields = ['id', 'time_create']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance

class UserChatSerializer(serializers.ModelSerializer):
    chat = ChatSerializer(source='chat_id')
    class Meta:
        model = UserChat
        fields = ['user_id', 'is_read', 'chat']
        read_only_fields = ['is_read', 'user_id']

class ChatCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=70)
    users_id = serializers.ListSerializer(
        child=serializers.IntegerField(),
        required=False,
        default=list

    )
    users_email = serializers.ListSerializer(
        child=serializers.CharField(max_length=254),
        required=False,
        default=list

    )

    def create(self, validated_data):
        users_id = validated_data.get('users_id', [])
        users_email = validated_data.get('users_email', [])
        title_chat = validated_data.get('title')
        users = get_and_check_users(users_id, users_email)
        creator_chat = self.context['user']
        chat = Chat.objects.create(title=title_chat)

        user_chat_instances = [UserChat(chat_id=chat, user_id=user)
                               for user in users.values()]

        user_chat_instances.append(UserChat(chat_id=chat,
                                            user_id=creator_chat,
                                            is_creator=True))
        UserChat.objects.bulk_create(user_chat_instances)

        return chat

    def to_representation(self, instance):
        print(type(instance))
        chat = ChatSerializer(instance).data
        return chat


class EmptySerializer(serializers.Serializer):
    pass







