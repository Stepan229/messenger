import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from messenger.messanger.models import Message, Chat
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_messages_list_authenticated():
    user = User.objects.create_user(username='testuser', password='testpass')
    chat = Chat.objects.create(title='Test Chat')
    Message.objects.create(creator_id=user, chat_id=chat, text='Test message')

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('messages-list', kwargs={'room_id': chat.id})
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['text'] == 'Test message'

@pytest.mark.django_db
def test_messages_list_unauthenticated():
    chat = Chat.objects.create(title='Test Chat')
    url = reverse('messages-list', kwargs={'room_id': chat.id})
    client = APIClient()
    response = client.get(url)

    assert response.status_code == 401

@pytest.mark.django_db
def test_create_message_authenticated():
    user = User.objects.create_user(username='testuser', password='testpass')
    chat = Chat.objects.create(title='Test Chat')

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('messages-create', kwargs={'room_id': chat.id})
    data = {'text': 'New message'}
    response = client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['text'] == 'New message'

@pytest.mark.django_db
def test_create_message_unauthenticated():
    chat = Chat.objects.create(title='Test Chat')
    url = reverse('messages-create', kwargs={'room_id': chat.id})
    data = {'text': 'New message'}
    client = APIClient()
    response = client.post(url, data, format='json')

    assert response.status_code == 401

@pytest.mark.django_db
def test_update_message_authenticated():
    user = User.objects.create_user(username='testuser', password='testpass')
    chat = Chat.objects.create(title='Test Chat')
    message = Message.objects.create(creator_id=user, chat_id=chat, text='Old message')

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('messages-update', kwargs={'room_id': chat.id, 'message_id': message.id})
    data = {'text': 'Updated message'}
    response = client.put(url, data, format='json')

    assert response.status_code == 200
    assert response.data['text'] == 'Updated message'

@pytest.mark.django_db
def test_delete_message_authenticated():
    user = User.objects.create_user(username='testuser', password='testpass')
    chat = Chat.objects.create(title='Test Chat')
    message = Message.objects.create(creator_id=user, chat_id=chat, text='Test message')

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('messages-delete', kwargs={'room_id': chat.id, 'message_id': message.id})
    response = client.delete(url)

    assert response.status_code == 202
    assert Message.objects.filter(id=message.id).count() == 0