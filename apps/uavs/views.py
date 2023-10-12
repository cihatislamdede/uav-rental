from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import UavBrandSerializer, UavCategorySerializer, UavSerializer
from .models import Uav, UavBrand, UavCategory
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


# Custom Permissions
class UserIsRenterPermission(BasePermission):
    message = "You are not a renter."

    def has_permission(self, request, view):
        if request.user.is_renter or request.user.is_superuser:
            return True
        return False


class UserCanModifyUavBrandPermission(BasePermission):
    message = "You do not have permission to modify or delete this brand."

    def has_permission(self, request, view):
        brand = UavBrand.objects.get(pk=view.kwargs["pk"])
        if brand.owner == request.user:
            return True


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
    permission_classes = [IsAuthenticated & UserIsRenterPermission]
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
        uav = Uav.objects.get(pk=pk)
        serializer = UavSerializer(uav)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteOrUpdateUavAPIView(APIView):
    permission_classes = [IsAuthenticated & UserIsRenterPermission]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def put(self, request, pk):
        uav = Uav.objects.get(pk=pk)
        serializer = UavSerializer(uav, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        Uav.objects.filter(pk=pk).update(is_active=False)
        return Response(status=status.HTTP_204_NO_CONTENT)


# Uav Category Views
class ListUavCategoryView(ListAPIView):
    queryset = UavCategory.objects.filter(is_active=True).order_by("id")
    serializer_class = UavCategorySerializer
    filterset_fields = ["owner", "category", "class_name", "operating_altitude"]


class CreateUavCategoryView(APIView):
    permission_classes = [IsAuthenticated & UserIsRenterPermission]

    def post(self, request):
        serializer = UavCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailUavCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        category = UavCategory.objects.get(pk=pk)
        serializer = UavCategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteOrUpdateUavCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated & UserIsRenterPermission]

    def put(self, request, pk):
        category = UavCategory.objects.get(pk=pk)
        serializer = UavCategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        UavCategory.objects.filter(pk=pk).update(is_active=False)
        return Response(status=status.HTTP_204_NO_CONTENT)


# Uav Brand Views
class ListUavBrandView(ListAPIView):
    queryset = UavBrand.objects.filter(is_active=True).order_by("id")
    serializer_class = UavBrandSerializer
    filterset_fields = ["owner", "company", "country", "website"]


class CreateUavBrandView(APIView):
    permission_classes = [IsAuthenticated & UserIsRenterPermission]

    def post(self, request):
        serializer = UavBrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailUavBrandView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        brand = UavBrand.objects.get(pk=pk)
        serializer = UavBrandSerializer(brand)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteOrUpdateUavBrandAPIView(APIView):
    permission_classes = [IsAuthenticated & UserCanModifyUavBrandPermission]

    def put(self, request, pk):
        brand = UavBrand.objects.get(pk=pk)
        serializer = UavBrandSerializer(brand, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        UavBrand.objects.filter(pk=pk).update(is_active=False)
        return Response(status=status.HTTP_204_NO_CONTENT)
