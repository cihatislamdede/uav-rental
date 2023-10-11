from django.db import models
from django.conf import settings


class UavBrand(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    company = models.CharField(max_length=50, unique=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company

    class Meta:
        verbose_name_plural = "UAV Brands"


class UavCategory(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    category = models.CharField(max_length=50, unique=True)
    class_name = models.CharField(max_length=50, blank=True, null=True)
    operating_altitude = models.FloatField(help_text="feet", blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = "UAV Categories"


class Uav(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    brand = models.ForeignKey(UavBrand, on_delete=models.CASCADE)
    model = models.CharField(max_length=50)
    category = models.ForeignKey(UavCategory, on_delete=models.CASCADE)

    payload_capacity = models.FloatField(help_text="kg", blank=True, null=True)
    maximum_speed = models.FloatField(help_text="knots", blank=True, null=True)
    wingspan = models.FloatField(help_text="meters", blank=True, null=True)
    endurance = models.FloatField(help_text="hours", blank=True, null=True)

    image = models.ImageField(upload_to="uav_images", blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("brand", "model")
        verbose_name = "UAV"
        verbose_name_plural = "UAVs"

    def __str__(self):
        return f"{self.brand} {self.model}"
