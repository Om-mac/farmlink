"""Farmer Serializers"""

from rest_framework import serializers
from .models import Farmer, FarmProduct


class FarmProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmProduct
        fields = [
            'id', 'product_name', 'product_category', 'daily_capacity_kg', 'available_quantity_kg',
            'year_round_available', 'harvest_season_start', 'harvest_season_end', 'quality_grade',
            'product_photo', 'quality_certificate', 'price_per_kg', 'verified', 'is_active'
        ]


class FarmerSerializer(serializers.ModelSerializer):
    available_products = FarmProductSerializer(many=True, read_only=True)
    email = serializers.EmailField(source='user.email', required=False)
    max_order_size_kg = serializers.FloatField(required=False)
    min_order_size_kg = serializers.FloatField(required=False)
    
    class Meta:
        model = Farmer
        fields = ['id', 'farm_name', 'location', 'country', 'phone', 'farm_size_hectares', 
                  'certification', 'years_in_business', 'daily_production_kg', 'max_order_size_kg',
                  'min_order_size_kg', 'rating', 'total_orders', 'on_time_delivery_rate',
                  'verified', 'available_products', 'email', 'wallet_address']
        read_only_fields = ['id', 'rating', 'total_orders', 'on_time_delivery_rate', 'verified']

    def create(self, validated_data):
        # Ensure min/max order sizes have defaults if not provided
        daily = validated_data.get('daily_production_kg', 0)
        validated_data.setdefault('max_order_size_kg', daily)
        validated_data.setdefault('min_order_size_kg', max(1.0, daily * 0.5))
        return super().create(validated_data)


class FarmerDetailSerializer(serializers.ModelSerializer):
    available_products = FarmProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Farmer
        fields = ['id', 'farm_name', 'location', 'latitude', 'longitude', 'country', 'phone',
                  'farm_size_hectares', 'certification', 'years_in_business', 'daily_production_kg',
                  'max_order_size_kg', 'min_order_size_kg', 'bank_name', 'account_holder',
                  'wallet_address', 'tax_id', 'rating', 'total_orders', 'on_time_delivery_rate',
                  'verified', 'available_products', 'created_at', 'updated_at']
        read_only_fields = ['id', 'rating', 'total_orders', 'verified', 'created_at', 'updated_at']
