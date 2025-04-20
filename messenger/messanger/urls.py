from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

app_name = "mess"

# router = DefaultRouter()
# router.register(r'api/chat/', MessagesViewSet, basename='message')
# urlpatterns = router.urls
# print(MessagesViewSet.reverse_action(MessagesViewSet.list, args=['1'], url_name='list'))

# UUID https://stackoverflow.com/questions/31687423/create-uuid-on-client-and-save-primary-key-with-django-rest-framework-and-using
urlpatterns = [
    # path('', index, name="index"),
    path("chat/<int:room_id>/", room,
         name="room"),
    path("chat/<int:room_id>/messages/", MessagesViewSet.as_view({'get': 'list'}),
         name='message-list'),
    path("chat/<int:room_id>/messages/create/", MessagesViewSet.as_view({'post': 'create'}),
         name='message-create'),
    path("chat/<int:room_id>/messages/<int:message_id>/", MessagesViewSet.as_view({'put': 'update'}),
         name='message-update'),
    path("chat/<int:room_id>/messages/<int:message_id>/", MessagesViewSet.as_view({'delete': 'delete'}),
         name='message-delete'),
    path("chats/", ChatsViewSet.as_view({'get': 'list'}),
         name='chat-list'),
    path("chats/create/", ChatsViewSet.as_view({'post': 'create'}),
         name='chat-create'),
    path("chats/<int:room_id>/", ChatsViewSet.as_view({'put': 'update'}),
         name='chat-update'),
    path("chats/<str:room_id>/members", ChatsViewSet.as_view({'get': 'get_chat_members'}),
         name='chat-members'),
    path("chats/<int:room_id>/", ChatsViewSet.as_view({'delete': 'delete'}),
         name='chat-delete'),
]