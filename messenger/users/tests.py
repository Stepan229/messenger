
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class UserTests(TestCase):
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

    def test_register(self):
        for i, data_user in enumerate(self.test_users, 1):
            with self.subTest(user=data_user['username']):
                response = self.client.post(self.register_url, data_user)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_201_CREATED,
                    f"Ошибка. {data_user['username']}. Ответ: {response.json()}"
                )
                print(f"Пользователь {i} зарегистрирован: {data_user['username']}")

        for i, data_user in enumerate(self.test_users, 1):
            with self.subTest(user=data_user['username']):
                login_data = {
                    "email": data_user['email'],
                    "password": data_user['password']
                }
                response = self.client.post(self.login_url, login_data)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_200_OK,
                    f"Ошибка при входе {data_user['username']}. Ответ: {response.json()}"
                )

                self.assertIn("auth_token", response.json(), "Токен не получен")
                print(f"Пользователь {data_user['username']} аутентифицирован")
