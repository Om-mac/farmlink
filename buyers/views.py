"""Buyer Views"""

import random
import string

from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import Buyer
from .serializers import BuyerSerializer, BuyerDetailSerializer


class BuyerViewSet(viewsets.ModelViewSet):
    """ViewSet for Buyers"""
    queryset = Buyer.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['company_name', 'location', 'country', 'buyer_type']
    ordering_fields = ['rating', 'created_at', 'total_purchases']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BuyerDetailSerializer
        return BuyerSerializer
    
    def _create_placeholder_user(self, email=None):
        username_base = (email.split('@')[0] if email else 'buyer').replace(' ', '_')
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
        """Get current buyer profile"""
        try:
            buyer = Buyer.objects.get(user=request.user)
            serializer = BuyerDetailSerializer(buyer)
            return Response(serializer.data)
        except Buyer.DoesNotExist:
            return Response({'error': 'No buyer profile found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def verified(self, request):
        """Get only verified buyers"""
        serializer = self.get_serializer(self.queryset.filter(verified=True), many=True)
        return Response(serializer.data)
