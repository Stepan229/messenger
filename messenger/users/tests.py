from django.test import TestCase

import requests

url = "http://127.0.0.1:8000/api/chats/create/"
data = {
    "title": "Мой чат",
    "users_id": [2,2,1000, 2]  # ID пользователей
}

headers = {
    'X-CSRFToken': '97ceb2b87c10753d1ae1ca1a3eae6ec738ca1718',
    'Content-Type': 'application/json',
    'Authorization': 'Token 97ceb2b87c10753d1ae1ca1a3eae6ec738ca1718'
}
response = requests.post(url, json=data, headers=headers)
print(response)
print(response.json())
