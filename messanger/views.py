from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from .models import Message, UserChat, Chat
from . import serializers
from django.core.exceptions import ImproperlyConfigured
from rest_framework.decorators import action
from django.shortcuts import render
from rest_framework.response import Response
from .utils import *

class MessagesViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.MessagesSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        count_messages = self.request.query_params.get('count')
        chat_id = str_to_int(self.kwargs.get('room_id'))
        user = request.user
        verification_user_in_chat(user, chat_id)
        messages = Message.objects.filter(chat_id=chat_id)

        if count_messages:
            slicing_messages(messages, count_messages)
        serializer = self.get_serializer(messages, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def create(self, request, *args, **kwargs):
        user = request.user
        chat_id = str_to_int(self.kwargs.get('room_id'))

        chat = verification_user_in_chat(user, chat_id)

        serializer = self.get_serializer(data=request.data,
                                         context={'user': user, 'chat': chat})

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    @action(methods=['PUT', ], detail=False)
    def update(self, request, *args, **kwargs):
        user = request.user
        chat_id = str_to_int(self.kwargs.get('room_id'))
        chat = verification_user_in_chat(user, chat_id)
        instance = validate_message_ownership(user, chat, self.kwargs.get('message_id'))

        serializer = self.get_serializer(data=request.data, instance=instance,
                                         context={'user': user, 'chat': chat})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(methods=['DELETE', ], detail=False)
    def delete(self, request, *args, **kwargs):
        user = request.user
        chat_id = str_to_int(self.kwargs.get('room_id'))
        chat = verification_user_in_chat(user, chat_id)
        message = validate_message_ownership(user, chat, self.kwargs.get('message_id'))
        message.delete()
        return Response("Successfully removed", status=status.HTTP_202_ACCEPTED)

class ChatsViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.EmptySerializer
    serializer_classes = {
        'list': serializers.UserChatSerializer,
        'create': serializers.ChatCreateSerializer
    }
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        # count_chats = self.request.query_params.get('count')
        user = request.user
        chats = UserChat.objects.filter(user_id=user).select_related("chat_id")
        serializer = self.serializer_class(chats, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def create(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data,
                                         context={'user': user})
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


def index(request):
    return render(request, 'messanger/index.html',
                  {'room_name': 'default_room'})

def room(request, room_id):
    return render(request, 'messanger/room.html', {
        'room_name': room_id
    })

