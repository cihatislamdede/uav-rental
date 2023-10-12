from django.conf import settings
from django.db import models

from apps.uavs.models import Uav


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uav = models.ForeignKey(Uav, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.uav} - {self.start_time} - {self.end_time}"

    class Meta:
        verbose_name_plural = "Reservations"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self.start_time > self.end_time:
            raise ValueError("Start time must be before end time.")
        overlapping_reservations = Reservation.objects.filter(
            uav=self.uav,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(pk=self.pk)
        if overlapping_reservations.exists():
            raise ValueError("UAV is already reserved for this time.")
        super().save(*args, **kwargs)

    def get_total_hours(self):
        return round(
            (self.end_time - self.start_time).total_seconds() / 3600,
            2,
        )

    def get_total_cost(self):
        return round(self.get_total_hours() * self.uav.hourly_rate, 2)
