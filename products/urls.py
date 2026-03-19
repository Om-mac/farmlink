"""Products URLs"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AggregatedProductPoolViewSet

router = DefaultRouter()
router.register(r'pools', AggregatedProductPoolViewSet, basename='aggregated-pool')

urlpatterns = [
    path('', include(router.urls)),
]
