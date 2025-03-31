from django.test import TestCase

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')
django.setup()
# test.py
from django.test import Client
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def test_chat_message():
    # Create a client
    c = Client()

    # Send a message to the channel
    c.post('/messanger/channel_name/')

    # Get the channel name from the scope
    channel_name = c.scope['url_route']['kwargs']['channel_name']

    # Get the channel layer
    channel_layer = get_channel_layer()

    # Send a message to the client
    async_to_sync(channel_layer.group_send)(
        channel_name,
        {'type': 'chat.message', 'message': 'Hello, world!'}
    )
    print('sdvs')

def test_disconnect():
    # Create a client
    c = Client()

    # Connect to the chat channel
    c.post('/chat/channel_name/')

    # Disconnect from the chat channel
    c.post('/disconnect/')

    # Get the channel name from the scope
    channel_name = c.scope['url_route']['kwargs']['channel_name']

    # Get the channel layer
    channel_layer = get_channel_layer()

    # Send a message to the client
    async_to_sync(channel_layer.group_discard)(
        channel_name,
        channel_name
    )

