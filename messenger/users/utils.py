from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import User

from django.conf import settings
from django.core.mail import send_mail
import random
import string


def get_and_authenticate_user(email, password):
    user = None
    if '@' in email:
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            pass
    else:

        user = authenticate(username=email, password=password,)
    if user is None:
        raise serializers.ValidationError("Invalid username/password. Please try again!")
    else:
        if user.is_verified:
            return user
        else:
            raise serializers.ValidationError("Confirm your email address!")

def create_user_account(email, password, username, otp=None, first_name="",
    last_name="",  **extra_fields):

    user = User.objects.create_user(
        email=email,
        password=password,
        username=username,
        first_name=first_name,
        last_name=last_name,
        otp=otp,
        **extra_fields)

    return user


def generate_otp(length=6):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp

def send_email(email, subject, message):
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    print(subject, message, from_email, recipient_list)
    # send_mail(subject, message, from_email, recipient_list)

def send_mail_otp(email, otp):
    subject = 'Your OTP for register'
    message = f'Your OTP is: {otp}'
    send_email(email, subject, message)
    print('EMAIL: ', email)

