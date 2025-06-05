
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Chat(models.Model):
    title = models.CharField(max_length=70, default='None')
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserChat(models.Model):
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False) # показывает что у тебя не прочитано сообщение
    is_creator = models.BooleanField(default=False)

class Message(models.Model):
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False) # прочитал ли кто-то твое сообщение

    class Meta:
        ordering = ['-time_create']

    def __str__(self):
        return self.text