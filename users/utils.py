from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import User


def get_and_authenticate_user(email, password):
    user = None
    if '@' in email:
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            pass
    else:
        user = authenticate(username=email, password=password)
    if user is None:
        raise serializers.ValidationError("Invalid username/password. Please try again!")
    else:
        return user

def create_user_account(email, password, username, first_name="",
    last_name="",  **extra_fields):

    user = User.objects.create_user(
     email=email, password=password, username=username,
     first_name=first_name, last_name=last_name, **extra_fields)

    return user