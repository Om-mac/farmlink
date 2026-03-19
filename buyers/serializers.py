"""Buyer Serializers"""

from rest_framework import serializers
from .models import Buyer


class BuyerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', required=False)
    payment_success_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = Buyer
        fields = ['id', 'company_name', 'buyer_type', 'location', 'country', 'phone',
                  'avg_monthly_orders', 'payment_method', 'rating', 'total_purchases',
                  'successful_deliveries', 'verified', 'email', 'wallet_address', 'payment_success_rate']
        read_only_fields = ['id', 'rating', 'total_purchases', 'successful_deliveries', 'verified']


class BuyerDetailSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    payment_success_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = Buyer
        fields = ['id', 'company_name', 'buyer_type', 'location', 'country', 'phone',
                  'avg_monthly_orders', 'payment_method', 'annual_purchase_value',
                  'wallet_address', 'bank_name', 'account_number', 'rating', 'total_purchases',
                  'successful_deliveries', 'dispute_count', 'verified', 'email', 'payment_success_rate',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'rating', 'total_purchases', 'successful_deliveries', 'verified', 'created_at', 'updated_at']
    
    def get_email(self, obj):
        return obj.user.email
