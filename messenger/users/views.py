from django.contrib.auth import logout, login

from rest_framework.authentication import TokenAuthentication

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers

from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.shortcuts import render
from .utils import (get_and_authenticate_user,
                    create_user_account, generate_otp,
                    send_mail_otp)

from .models import User
from rest_framework.authtoken.models import Token


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny,]
    serializer_class = serializers.EmptySerializer
    serializer_classes = {
        'login': serializers.UserLoginSerializer,
        'register': serializers.UserRegisterSerializer
    }

    def get_queryset(self):
        return None

    @action(methods=['POST', ], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = generate_otp()
        user = create_user_account(**serializer.validated_data, otp=otp)
        send_mail_otp(user.email, otp)
        data = serializers.AuthUserSerializer(user).data

        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        login(request, user)
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

class UserViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.EmptySerializer
    serializer_classes = {
        'get_user': serializers.UserSerializer
    }

    @action(methods=['GET', ], detail=False)
    def get_user(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


class ValidateOTP(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = serializers.ValidateOptSerializer

    @action(methods=['POST', ], detail=False)
    def confirm_email(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.validated_data['email'])

        user.otp = None
        user.is_verified = True
        user.save()

        token, _ = Token.objects.get_or_create(user=user)
        user_data = serializers.UserSerializer(user).data

        return Response({
            'token': token.key,
            'user': user_data
        },
            status=status.HTTP_200_OK)




def login1(request):
    return render(request, 'users/login.html')