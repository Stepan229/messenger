from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class MessengerTests(TestCase):
    create_chat_url = reverse('chat-create')
    register_url = reverse('user-register')
    login_url = reverse('user-login')
    test_users = [
        {
            "email": "test1@mail.ru",
            "password": "testpass123",
            "first_name": "Иван",
            "last_name": "Петров",
            "username": "ivan_petrov"
        },
        {
            "email": "test2@mail.ru",
            "password": "testpass456",
            "first_name": "Мария",
            "last_name": "Сидорова",
            "username": "maria_sid"
        },
        {
            "email": "test3@mail.ru",
            "password": "testpass789",
            "first_name": "Алексей",
            "last_name": "Иванов",
            "username": "alex_ivanov"
        },
        {
            "email": "test4@mail.ru",
            "password": "securepass1",
            "first_name": "Елена",
            "last_name": "Смирнова",
            "username": "elena_smir"
        },
        {
            "email": "test5@mail.ru",
            "password": "strongpass2",
            "first_name": "Дмитрий",
            "last_name": "Козлов",
            "username": "dima_koz"
        }
    ]

    def test_create_chat(self):
        data_users = self.register_user()
        creator_chat = data_users[0]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {creator_chat["auth_token"]}')
        with self.subTest(user=creator_chat['username']):
            users_in_email = ([user['email'] for user in self.test_users])
            data = {
                'users_email': users_in_email[1:],
                'title': 'Chat test 1',
            }
            response = client.post(self.create_chat_url, data, format='json')
            title_chat = Chat.objects.all().values()[0].get('title', '')
            users_in_chat_query = UserChat.objects.select_related('user_id').all()
            users_in_chat = [user.user_id.email for user in users_in_chat_query]
            print(response.json())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                f"Ошибка. {creator_chat['username']}. Ответ: {response.json()}")

            self.assertEqual(
                title_chat,
                data['title'],
                f"Нет чата. Ответ: {response.json()}")

            self.assertSetEqual(set(users_in_chat), set(users_in_email),
                                 f"Пользователи не найдены. ожидание: "
                                 f"{users_in_email}. факт: {users_in_chat}")

            

    def register_user(self) -> list[dict[str, str]]:
        users_data = []
        for i, data_user in enumerate(self.test_users, 1):
            with self.subTest(user=data_user['username']):
                response = self.client.post(self.register_url, data_user)
                data_user['auth_token'] = response.json().get('auth_token')
                users_data.append(data_user)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_201_CREATED,
                    f"Ошибка. {data_user['username']}. Ответ: {response.json()}"
                )
        return users_data
