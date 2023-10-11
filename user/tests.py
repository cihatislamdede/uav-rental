from django.test import TestCase
from rest_framework import status
from django.contrib.auth import get_user_model


class UserRegisterAPIViewTestCase(TestCase):
    def test_user_register(self):
        data = {
            "username": "testcase",
            "email": "test@test.com",
            "password": "newpassword111",
        }
        response = self.client.post("/api/auth/register/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], data["username"])
        self.assertEqual(response.data["email"], data["email"])
        self.assertTrue("token" in response.data)

    def test_user_register_with_short_password(self):
        data = {
            "username": "testcase",
            "email": "test@test.com",
            "password": "test",
        }

        response = self.client.post("/api/auth/register/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginAPIViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testcase",
            email="test@test.com",
            password="newpassword111",
        )

    def test_user_login(self):
        data = {
            "username": "testcase",
            "password": "newpassword111",
        }
        response = self.client.post("/api/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], data["username"])
        self.assertTrue("token" in response.data)

    def test_user_login_with_wrong_password(self):
        data = {
            "username": "testcase",
            "password": "wrongpassword",
        }
        response = self.client.post("/api/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserLogoutAPIViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testcase",
            email="test@test.com",
            password="newpassword111",
        )

    def test_user_logout(self):
        data = {
            "username": "testcase",
            "password": "newpassword111",
        }
        response = self.client.post("/api/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], data["username"])
        self.assertTrue("token" in response.data)

        token = response.data["token"]
        response = self.client.post(
            "/api/auth/logout/", headers={"Authorization": f"Token {token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], "Successfully logged out")

    def test_user_logout_without_token(self):
        response = self.client.post("/api/auth/logout/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_logout_with_wrong_token(self):
        response = self.client.post(
            "/api/auth/logout/",
            headers={"Authorization": f"Token {self.user.auth_token}wrong"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
