from django.contrib.auth import logout, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from .models import User
from .utils import get_and_authenticate_user, create_user_account
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from rest_framework.permissions import AllowAny

from django.shortcuts import render


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
        user = create_user_account(**serializer.validated_data)
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
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

# def login(request):
#     return render(request, 'users/login.html')