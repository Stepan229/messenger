from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *
#
# app_name = "mess"

# router = DefaultRouter()
# router.register(r'api/chat/', MessagesViewSet, basename='message')
# urlpatterns = router.urls
# print(MessagesViewSet.reverse_action(MessagesViewSet.list, args=['1'], url_name='list'))

# UUID https://stackoverflow.com/questions/31687423/create-uuid-on-client-and-save-primary-key-with-django-rest-framework-and-using
urlpatterns = [
    path("chat/<int:room_id>/", room,
         name="room"),
    path("chats/", chats,
         name="chats"),
    path("api/chat/<int:room_id>/messages/", MessagesViewSet.as_view({'get': 'list'}),
         name='message-list'),
    path("api/chat/<int:room_id>/messages/create/", MessagesViewSet.as_view({'post': 'create'}),
         name='message-create'),
    path("api/chat/<int:room_id>/messages/<int:message_id>/", MessagesViewSet.as_view({'put': 'update'}),
         name='message-update'),
    path("api/chat/<int:room_id>/messages/<int:message_id>/", MessagesViewSet.as_view({'delete': 'delete'}),
         name='message-delete'),
    path("api/chats/", ChatsViewSet.as_view({'get': 'list'}),
         name='chat-list'),
    path("api/chats/<int:room_id>/", ChatsViewSet.as_view({'get': 'get_chat_info'}),
         name='chat-list'),
    path("api/chats/create/", ChatsViewSet.as_view({'post': 'create'}),
         name='chat-create'),
    path("api/chats/<int:room_id>/", ChatsViewSet.as_view({'put': 'update'}),
         name='chat-update'),
    path("api/chats/<str:room_id>/members/", ChatsViewSet.as_view({'get': 'get_chat_members'}),
         name='chat-members'),
    path("api/chats/<int:room_id>/", ChatsViewSet.as_view({'delete': 'delete'}),
         name='chat-delete'),
]