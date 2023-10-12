from django.urls import path

from .views import (
    ListReservationsView,
    CreateReservationView,
    RetrieveUpdateDestroyReservationView,
)


urlpatterns = [
    path("", ListReservationsView.as_view(), name="reservations"),
    path("create/", CreateReservationView.as_view(), name="create_reservation"),
    path(
        "<int:pk>/",
        RetrieveUpdateDestroyReservationView.as_view(),
        name="reservation",
    ),
]
