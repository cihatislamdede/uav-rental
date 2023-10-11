from django.urls import path

from .views import UserLoginAPIView, UserLogoutAPIView, UserRegisterAPIView

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("logout/", UserLogoutAPIView.as_view(), name="logout"),
]
