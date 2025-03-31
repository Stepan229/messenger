from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)  # Делаем поле email уникальным

    def __str__(self):
        return self.username





