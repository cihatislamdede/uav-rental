from datetime import datetime

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserRegisterSerializer


class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.get(user=user).key
                response = {
                    "token": token,
                    "email": user.email,
                    "username": user.username,
                }
                return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data.get("username", None)
        password = data.get("password", None)
        if username is None or password is None:
            return Response(
                {"error": "Please provide both username and password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(username=username, password=password)
        user.last_login = datetime.now()
        user.save()
        if not user:
            return Response(
                {"error": "Invalid Credentials"},
                status=status.HTTP_404_NOT_FOUND,
            )
        token, _ = Token.objects.get_or_create(user=user)
        response = {
            "token": token.key,
            "email": user.email,
            "username": user.username,
        }
        return Response(response, status=status.HTTP_200_OK)


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(
                status=status.HTTP_200_OK, data={"success": "Successfully logged out"}
            )
        except Exception:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"error": "Bad request"}
            )
