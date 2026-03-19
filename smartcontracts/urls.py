"""Smart Contracts URLs"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SmartContractViewSet, AWSBlockchainConfigViewSet

router = DefaultRouter()
router.register(r'contracts', SmartContractViewSet, basename='smart-contract')
router.register(r'configs', AWSBlockchainConfigViewSet, basename='blockchain-config')

urlpatterns = [
    path('', include(router.urls)),
]
