from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Reservation
from .serializers import ReservationSerializer


# Custom permission to check if the user is the owner of the reservation
class UserIsOwnerOfReservationPermission(BasePermission):
    message = "You are not the owner of this reservation."

    def has_permission(self, request, view):
        reservation = Reservation.objects.get(pk=view.kwargs["pk"])
        return request.user == reservation.user


class ListReservationsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.filter(is_active=True).order_by("-created_at")
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer
    filterset_fields = ["user", "uav", "start_time", "end_time"]
    search_fields = ["user__username", "uav__model", "start_time", "end_time"]


class CreateReservationView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        try:
            serializer = ReservationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateDestroyReservationView(APIView):
    permission_classes = [IsAuthenticated, UserIsOwnerOfReservationPermission]

    def get_object(self, pk):
        return get_object_or_404(Reservation, pk=pk)

    def get(self, request, pk):
        reservation = self.get_object(pk)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    @transaction.atomic
    def put(self, request, pk):
        reservation = self.get_object(pk)
        serializer = ReservationSerializer(reservation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reservation = self.get_object(pk)
        reservation.is_active = False
        reservation.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
