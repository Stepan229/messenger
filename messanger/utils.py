from rest_framework.exceptions import ParseError, NotFound, PermissionDenied, ValidationError
from .models import Message, UserChat, Chat

from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model
User = get_user_model()

def str_to_int(value: str) -> int:
    try:
        value_int = int(value)
        return value_int
    except (ValueError, TypeError):
        raise ParseError({'ValueError': 'Field expected a number'})


def verification_user_in_chat(user, chat_id: int) -> Chat:
    try:
        _ = UserChat.objects.get(chat_id=chat_id, user_id=user.id)
        chat = Chat.objects.get(id=chat_id)
        return chat
    except UserChat.DoesNotExist:
        raise NotFound("Chat not found")

def validate_chat_ownership(user, chat_id: int) -> Chat:
    try:
        _ = UserChat.objects.get(chat_id=chat_id, user_id=user.id, is_creator=True)
        chat = Chat.objects.get(id=chat_id)
        return chat
    except UserChat.DoesNotExist:
        raise NotFound("You don't have access to this chat")

def slicing_messages(messages: QuerySet, end_slice: str) -> QuerySet:
    end_slice = str_to_int(end_slice)
    messages = messages[:end_slice]
    return messages

def validate_message_ownership(user, chat: Chat, message_id: int):
    try:
        instance = Message.objects.get(creator_id=user, chat_id=chat, id=message_id)
        return instance
    except Message.DoesNotExist:
        raise PermissionDenied("Message not found or no rights to edit the message")

def get_and_check_users(id: list, email: list) -> dict[int: User]:
    users = {}
    count_users = 0
    if id:
        users = User.objects.in_bulk(id)
        count_users = len(id)
    elif email:
        users = User.objects.in_bulk(email, field_name='email')
        count_users = len(email)
    else:
        ValidationError("users_id, users_email are empty")

    if len(users) != count_users:
        num_of_lost = count_users - len(users)
        raise NotFound(f"Users not found: {num_of_lost}")

    return users
