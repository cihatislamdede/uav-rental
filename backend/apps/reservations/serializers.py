from rest_framework import serializers

from apps.uavs.models import Uav

from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    uav = serializers.SlugRelatedField(slug_field="id", queryset=Uav.objects.all())

    class Meta:
        model = Reservation
        exclude = (
            "is_active",
            "updated_at",
        )
        read_only_fields = ("id",)
