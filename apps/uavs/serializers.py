from rest_framework import serializers
from .models import Uav, UavBrand, UavCategory


class UavBrandSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = UavBrand
        exclude = (
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id",)


class UavCategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = UavCategory
        exclude = (
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id",)


class UavSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    brand = serializers.PrimaryKeyRelatedField(queryset=UavBrand.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=UavCategory.objects.all())

    class Meta:
        model = Uav
        exclude = (
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id",)
