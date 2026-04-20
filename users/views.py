from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random

from .serializers import RegisterSerializer, ConfirmSerializer
from .models import UserConfirmation

class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = User.objects.create_user(
            username=username,
            password=password,
            is_active=False  # ❗ не активен
        )

        code = str(random.randint(100000, 999999))

        UserConfirmation.objects.create(
            user=user,
            code=code
        )

        return Response({
            "user_id": user.id,
            "code": code
        }, status=201)


class ConfirmAPIView(APIView):
    def post(self, request):
        serializer = ConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        code = serializer.validated_data['code']

        try:
            user = User.objects.get(id=user_id)
            confirm = UserConfirmation.objects.get(user=user)
        except:
            return Response({"error": "not found"}, status=404)

        if confirm.code == code:
            user.is_active = True
            user.save()
            return Response({"message": "confirmed"})

        return Response({"error": "wrong code"}, status=400)


class AuthorizationAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(status=401)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key
        })
