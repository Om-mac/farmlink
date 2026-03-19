"""Farmer Views"""

from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Farmer, FarmProduct
from .serializers import FarmerSerializer, FarmerDetailSerializer, FarmProductSerializer


import random
import string

from django.contrib.auth.models import User


class FarmerViewSet(viewsets.ModelViewSet):
    """ViewSet for Farmers"""
    queryset = Farmer.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['farm_name', 'location', 'country', 'certification']
    ordering_fields = ['rating', 'created_at', 'daily_production_kg']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FarmerDetailSerializer
        return FarmerSerializer
    
    def _create_placeholder_user(self, email=None):
        username_base = (email.split('@')[0] if email else 'farmer').replace(' ', '_')
        username = username_base[:20]
        while User.objects.filter(username=username).exists():
            username = f"{username_base[:18]}_{random.choice(string.ascii_lowercase)}"
        password = User.objects.make_random_password()
        return User.objects.create_user(username=username, email=email or '', password=password)
    
    def perform_create(self, serializer):
        user_data = serializer.validated_data.get('user', {})
        email = None
        if isinstance(user_data, dict):
            email = user_data.get('email')
        user = self._create_placeholder_user(email=email)
        serializer.save(user=user)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Get current farmer profile"""
        try:
            farmer = Farmer.objects.get(user=request.user)
            serializer = FarmerDetailSerializer(farmer)
            return Response(serializer.data)
        except Farmer.DoesNotExist:
            return Response({'error': 'No farmer profile found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def verify_farmer(self, request, pk=None):
        """Admin action to verify farmer (demo only)"""
        farmer = self.get_object()
        farmer.verified = True
        farmer.save()
        return Response({'status': 'farmer verified'})
    
    @action(detail=False, methods=['get'])
    def verified(self, request):
        """Get only verified farmers"""
        serializer = self.get_serializer(self.queryset.filter(verified=True), many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search_by_product(self, request):
        """Search farmers by product type"""
        product_name = request.query_params.get('product', '')
        if not product_name:
            return Response({'error': 'product query parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        farmers = Farmer.objects.filter(
            available_products__product_name__icontains=product_name
        ).distinct()
        serializer = self.get_serializer(farmers, many=True)
        return Response(serializer.data)


class FarmProductViewSet(viewsets.ModelViewSet):
    """ViewSet for Farm Products"""
    queryset = FarmProduct.objects.all()
    serializer_class = FarmProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product_name', 'farmer__farm_name']
    ordering_fields = ['price_per_kg', 'daily_capacity_kg']
    
    @action(detail=False, methods=['get'])
    def by_farmer(self, request):
        """Get products by farmer ID"""
        farmer_id = request.query_params.get('farmer_id')
        if not farmer_id:
            return Response({'error': 'farmer_id query parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        products = FarmProduct.objects.filter(farmer_id=farmer_id)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
