from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status

from apps.uavs.models import Uav, UavBrand, UavCategory


class UavTestCase(TestCase):
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

    def test_renter_uav_create(self):
        data = {
            "brand": self.brand.id,
            "model": "Test Model 2",
            "category": self.category.id,
        }
        response = self.client.post(
            "/api/create-uav/",
            data,
            content_type="application/json",
            headers={"Authorization": f"Token {self.renter_user.auth_token.key}"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["model"], data["model"])

    def test_customer_uav_create(self):
        data = {
            "brand": self.brand.id,
            "model": "Test Model 2",
            "category": self.category.id,
        }
        response = self.client.post(
            "/api/create-uav/",
            data,
            content_type="application/json",
            headers={"Authorization": f"Token {self.customer_user.auth_token.key}"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_renter_uav_update(self):
        data = {
            "brand": self.brand.id,
            "model": "Test Model 2",
            "category": self.category.id,
        }
        response = self.client.put(
            f"/api/update-uav/{self.uav.id}/",
            data,
            content_type="application/json",
            headers={"Authorization": f"Token {self.renter_user.auth_token.key}"},
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data["model"], data["model"])

    def test_renter_uav_delete(self):
        response = self.client.delete(
            f"/api/update-uav/{self.uav.id}/",
            content_type="application/json",
            headers={"Authorization": f"Token {self.renter_user.auth_token.key}"},
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_customer_uav_delete(self):
        response = self.client.delete(
            f"/api/update-uav/{self.uav.id}/",
            content_type="application/json",
            headers={"Authorization": f"Token {self.customer_user.auth_token.key}"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
