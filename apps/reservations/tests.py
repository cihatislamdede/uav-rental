from django.test import TestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.uavs.models import Uav, UavBrand, UavCategory


class ReservationTestCase(TestCase):
    def setUp(self):
        self.customer_user = get_user_model().objects.create_user(
            username="customeruser",
            email="customer@test.com",
            password="customerpassword111",
            is_renter=False,
        )
        self.renter_user = get_user_model().objects.create_user(
            username="renteruser",
            email="renter@test.com",
            password="renterpassword111",
            is_renter=True,
        )
        self.brand = UavBrand.objects.create(
            owner=self.renter_user, company="testcompany"
        )
        self.category = UavCategory.objects.create(
            owner=self.renter_user, category="testcategory"
        )
        self.uav = Uav.objects.create(
            owner=self.renter_user,
            brand=self.brand,
            model="Test Model",
            category=self.category,
        )

    def test_reservation_create(self):
        data = {
            "uav": self.uav.id,
            "start_time": "2023-10-12 11:00",
            "end_time": "2023-10-12 12:00",
        }
        response = self.client.post(
            "/api/reservations/create/",
            data,
            content_type="application/json",
            headers={"Authorization": f"Token {self.customer_user.auth_token.key}"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["uav"], self.uav.id)

    def test_reservation_update(self):
        data = {
            "uav": self.uav.id,
            "start_time": "2023-10-12 11:00",
            "end_time": "2023-10-12 12:00",
        }
        response = self.client.post(
            "/api/reservations/create/",
            data,
            content_type="application/json",
            headers={"Authorization": f"Token {self.customer_user.auth_token.key}"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["uav"], self.uav.id)
        reservation_id = response.data["id"]
        data = {
            "uav": self.uav.id,
            "start_time": "2023-10-12 12:00",
            "end_time": "2023-10-12 13:00",
        }
        response = self.client.put(
            f"/api/reservations/{reservation_id}/",
            data,
            content_type="application/json",
            headers={"Authorization": f"Token {self.customer_user.auth_token.key}"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uav"], self.uav.id)

    def test_reservation_delete(self):
        data = {
            "uav": self.uav.id,
            "start_time": "2023-10-12 11:00",
            "end_time": "2023-10-12 12:00",
        }
        response = self.client.post(
            "/api/reservations/create/",
            data,
            content_type="application/json",
            headers={"Authorization": f"Token {self.customer_user.auth_token.key}"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["uav"], self.uav.id)
        reservation_id = response.data["id"]
        response = self.client.delete(
            f"/api/reservations/{reservation_id}/",
            content_type="application/json",
            headers={"Authorization": f"Token {self.customer_user.auth_token.key}"},
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_another_user_reservation_update_and_delete(self):
        data = {
            "uav": self.uav.id,
            "start_time": "2023-10-12 11:00",
            "end_time": "2023-10-12 12:00",
        }
        response = self.client.post(
            "/api/reservations/create/",
            data,
            content_type="application/json",
            headers={"Authorization": f"Token {self.customer_user.auth_token.key}"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["uav"], self.uav.id)
        reservation_id = response.data["id"]
        data = {
            "uav": self.uav.id,
            "start_time": "2023-10-12 12:00",
            "end_time": "2023-10-12 13:00",
        }
        response = self.client.put(
            f"/api/reservations/{reservation_id}/",
            data,
            content_type="application/json",
            headers={"Authorization": f"Token {self.renter_user.auth_token.key}"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(
            f"/api/reservations/{reservation_id}/",
            content_type="application/json",
            headers={"Authorization": f"Token {self.renter_user.auth_token.key}"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reservation_create_with_invalid_time(self):
        data = {
            "uav": self.uav.id,
            "start_time": "2023-10-12 11:00",
            "end_time": "2023-10-12 10:00",
        }
        response = self.client.post(
            "/api/reservations/create/",
            data,
            content_type="application/json",
            headers={"Authorization": f"Token {self.customer_user.auth_token.key}"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Start time must be before end time.")

    def test_reservation_create_with_overlap(self):
        data = {
            "uav": self.uav.id,
            "start_time": "2023-10-12 11:00",
            "end_time": "2023-10-12 12:00",
        }
        response = self.client.post(
            "/api/reservations/create/",
            data,
            content_type="application/json",
            headers={"Authorization": f"Token {self.customer_user.auth_token.key}"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["uav"], self.uav.id)
        data = {
            "uav": self.uav.id,
            "start_time": "2023-10-12 11:00",
            "end_time": "2023-10-12 13:00",
        }
        response = self.client.post(
            "/api/reservations/create/",
            data,
            content_type="application/json",
            headers={"Authorization": f"Token {self.customer_user.auth_token.key}"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "UAV is already reserved for this time.")
