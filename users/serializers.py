from django.contrib.auth.base_user import BaseUserManager
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import password_validation

from .models import User


class UserSerializer(serializers.Serializer):
    model = User
    email = serializers.CharField(max_length=254)
    username = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=254, required=True)
    password = serializers.CharField(max_length=254, required=True, write_only=True)
    print(email, password)


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'auth_token')
        read_only_fields = ('id', 'is_active', 'is_staff')

    def get_auth_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'username')

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError("Email is already taken")
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def validate_username(self, value):
        user = User.objects.filter(username=value)
        if user:
            raise serializers.ValidationError("Username is already taken")
        return value
class EmptySerializer(serializers.Serializer):
    pass