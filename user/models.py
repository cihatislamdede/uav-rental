from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    country = models.CharField(max_length=50, null=True, blank=True)
    company = models.CharField(max_length=50, null=True, blank=True)
    is_renter = models.BooleanField(
        default=False, help_text="Check if user is a UAV owner so renter."
    )
