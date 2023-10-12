from django.urls import path

from .views import (CreateUavBrandView, CreateUavCategoryView, CreateUavView,
                    DeleteOrUpdateUavAPIView, DeleteOrUpdateUavBrandAPIView,
                    DeleteOrUpdateUavCategoryAPIView, DetailUavBrandView,
                    DetailUavCategoryView, DetailUavView, ListUavBrandView,
                    ListUavCategoryView, ListUavView)

urlpatterns = [
    # Uavs
    path("uavs/", ListUavView.as_view(), name="uavs"),
    path("uav/<int:pk>/", DetailUavView.as_view(), name="detail-uav"),
    path("create-uav/", CreateUavView.as_view(), name="create-uav"),
    path("update-uav/<int:pk>/", DeleteOrUpdateUavAPIView.as_view(), name="update-uav"),
    # Uav Categories
    path("categories/", ListUavCategoryView.as_view(), name="uav-categories"),
    path(
        "category/<int:pk>/",
        DetailUavCategoryView.as_view(),
        name="detail-uav-category",
    ),
    path(
        "create-category/", CreateUavCategoryView.as_view(), name="create-uav-category"
    ),
    path(
        "update-category/<int:pk>/",
        DeleteOrUpdateUavCategoryAPIView.as_view(),
        name="update-uav-category",
    ),
    # Uav Brands
    path("brands/", ListUavBrandView.as_view(), name="uav-brands"),
    path("brand/<int:pk>/", DetailUavBrandView.as_view(), name="detail-uav-brand"),
    path("create-brand/", CreateUavBrandView.as_view(), name="create-uav-brand"),
    path(
        "update-brand/<int:pk>/",
        DeleteOrUpdateUavBrandAPIView.as_view(),
        name="update-uav-brand",
    ),
]
