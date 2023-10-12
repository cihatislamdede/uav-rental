from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Uav, UavBrand, UavCategory
from .serializers import UavBrandSerializer, UavCategorySerializer, UavSerializer


# Custom Permissions
class IsUserRenterPermission(BasePermission):
    message = "You are not a renter."

    def has_permission(self, request, view):
        return request.user.is_renter or request.user.is_superuser


# Uav Views
class ListUavView(ListAPIView):
    queryset = Uav.objects.filter(is_active=True).order_by("id")
    serializer_class = UavSerializer
    filterset_fields = [
        "owner",
        "brand",
        "model",
        "category",
        "payload_capacity",
        "maximum_speed",
        "wingspan",
        "endurance",
    ]
    search_fields = [
        "owner__username",
        "brand__company",
        "model",
        "category__class_name",
    ]


class CreateUavView(APIView):
    permission_classes = [IsAuthenticated & IsUserRenterPermission]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        serializer = UavSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailUavView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        uav = get_object_or_404(Uav, pk=pk)
        serializer = UavSerializer(uav)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteOrUpdateUavAPIView(APIView):
    permission_classes = [IsAuthenticated & IsUserRenterPermission]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def put(self, request, pk):
        uav = get_object_or_404(Uav, pk=pk)
        if request.user != uav.owner:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = UavSerializer(uav, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        uav = get_object_or_404(Uav, pk=pk)
        if request.user != uav.owner:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        uav.is_active = False
        uav.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Uav Category Views
class ListUavCategoryView(ListAPIView):
    queryset = UavCategory.objects.filter(is_active=True).order_by("id")
    serializer_class = UavCategorySerializer
    filterset_fields = ["owner", "category", "class_name", "operating_altitude"]


class CreateUavCategoryView(APIView):
    permission_classes = [IsAuthenticated & IsUserRenterPermission]

    def post(self, request):
        serializer = UavCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailUavCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        category = get_object_or_404(UavCategory, pk=pk)
        serializer = UavCategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteOrUpdateUavCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        category = get_object_or_404(UavCategory, pk=pk)
        if request.user != category.owner:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = UavCategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = get_object_or_404(UavCategory, pk=pk)
        if request.user != category.owner:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        category.is_active = False
        category.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Uav Brand Views
class ListUavBrandView(ListAPIView):
    queryset = UavBrand.objects.filter(is_active=True).order_by("id")
    serializer_class = UavBrandSerializer
    filterset_fields = ["owner", "company", "country", "website"]


class CreateUavBrandView(APIView):
    permission_classes = [IsAuthenticated & IsUserRenterPermission]

    def post(self, request):
        serializer = UavBrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailUavBrandView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        brand = get_object_or_404(UavBrand, pk=pk)
        serializer = UavBrandSerializer(brand)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteOrUpdateUavBrandAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        brand = get_object_or_404(UavBrand, pk=pk)
        if request.user != brand.owner:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = UavBrandSerializer(brand, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        brand = get_object_or_404(UavBrand, pk=pk)
        if request.user != brand.owner:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        brand.is_active = False
        brand.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
