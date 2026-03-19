"""Farmer URLs"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FarmerViewSet, FarmProductViewSet

router = DefaultRouter()
router.register(r'', FarmerViewSet, basename='farmer')
router.register(r'products', FarmProductViewSet, basename='farm-product')

urlpatterns = [
    path('', include(router.urls)),
]
