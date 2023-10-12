from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserRegisterSerializer


class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.get(user=user).key
                response = {
                    "token": token,
                    "id": user.id,
                    "username": user.username,
                    "is_renter": user.is_renter,
                }
                return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
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
        if not user:
            return Response(
                {"error": "Invalid Credentials"},
                status=status.HTTP_404_NOT_FOUND,
            )
        user.last_login = timezone.now()
        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        response = {
            "token": token.key,
            "id": user.id,
            "username": user.username,
            "is_renter": user.is_renter,
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
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Something went wrong"},
            )
