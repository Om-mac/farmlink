"""Products Serializers"""

from rest_framework import serializers
from .models import AggregatedProductPool, QualityAssurance
from farmers.serializers import FarmProductSerializer


class QualityAssuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityAssurance
        fields = ['id', 'status', 'inspector_name', 'inspection_date', 'notes']


class AggregatedProductPoolSerializer(serializers.ModelSerializer):
    participating_farmers_count = serializers.SerializerMethodField()
    total_pool_value = serializers.SerializerMethodField()
    quality_assurance = QualityAssuranceSerializer(read_only=True)
    
    class Meta:
        model = AggregatedProductPool
        fields = ['id', 'product_name', 'total_available_kg', 'target_quantity_kg',
                  'average_price_per_kg', 'status', 'platform_fee_percentage',
                  'participating_farmers_count', 'total_pool_value', 'quality_assurance', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_participating_farmers_count(self, obj):
        return obj.get_participating_farmers_count()
    
    def get_total_pool_value(self, obj):
        return obj.calculate_total_value()


class AggregatedProductPoolDetailSerializer(serializers.ModelSerializer):
    source_products = FarmProductSerializer(many=True, read_only=True)
    participating_farmers_count = serializers.SerializerMethodField()
    quality_assurance = QualityAssuranceSerializer(read_only=True)
    
    class Meta:
        model = AggregatedProductPool
        fields = ['id', 'product_name', 'source_products', 'total_available_kg', 
                  'target_quantity_kg', 'average_price_per_kg', 'status',
                  'platform_fee_percentage', 'participating_farmers_count',
                  'quality_assurance', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_participating_farmers_count(self, obj):
        return obj.get_participating_farmers_count()


class BuyerRequirementSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=255)
    required_quantity_ton = serializers.FloatField(required=False, min_value=0.001)
    required_quantity_kg = serializers.FloatField(required=False, min_value=1)
    max_price_per_kg = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    product_category = serializers.ChoiceField(
        choices=[('vegetable', 'Vegetable'), ('fruit', 'Fruit')],
        required=False
    )
    minimum_quality_grade = serializers.ChoiceField(choices=['A', 'B', 'C'], required=False, default='C')
    require_quality_certificate = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs):
        if not attrs.get('required_quantity_ton') and not attrs.get('required_quantity_kg'):
            raise serializers.ValidationError(
                "Provide either required_quantity_ton or required_quantity_kg."
            )
        return attrs
