from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


fields = list(UserAdmin.fieldsets)
fields[1] = (
    "Personal info",
    {"fields": ("first_name", "last_name", "email", "country", "company", "is_renter")},
)
UserAdmin.fieldsets = tuple(fields)

admin.site.register(CustomUser, UserAdmin)
