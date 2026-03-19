"""Orders Serializers"""

from rest_framework import serializers
from .models import Order, OrderDispute, PaymentTransaction


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = ['id', 'payment_type', 'amount', 'transaction_hash', 'status', 'block_number', 'created_at']


class OrderDisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDispute
        fields = ['id', 'reason', 'description', 'status', 'proposed_resolution', 'final_resolution', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    payment_transactions = PaymentTransactionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'buyer', 'aggregated_pool', 'quantity_kg', 'unit_price', 'total_amount',
                  'status', 'smart_contract_id', 'expected_delivery_date', 'created_at',
                  'payment_transactions']
        read_only_fields = ['id', 'total_amount', 'smart_contract_id', 'created_at']


class OrderDetailSerializer(serializers.ModelSerializer):
    payment_transactions = PaymentTransactionSerializer(many=True, read_only=True)
    dispute = OrderDisputeSerializer(read_only=True)
    buyer_company = serializers.SerializerMethodField()
    pool_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'buyer', 'buyer_company', 'aggregated_pool', 'pool_info', 'quantity_kg',
                  'unit_price', 'product_cost', 'platform_fee', 'total_amount', 'status',
                  'smart_contract_id', 'smart_contract_address', 'expected_delivery_date',
                  'shipping_address', 'tracking_number', 'payment_received_at', 'shipped_at',
                  'delivered_at', 'payment_transactions', 'dispute', 'created_at']
        read_only_fields = ['id', 'product_cost', 'platform_fee', 'total_amount', 'created_at']
    
    def get_buyer_company(self, obj):
        return obj.buyer.company_name
    
    def get_pool_info(self, obj):
        return {
            'product_name': obj.aggregated_pool.product_name,
            'available_kg': obj.aggregated_pool.total_available_kg,
        }
