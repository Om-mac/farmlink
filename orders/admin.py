from django.contrib import admin
from .models import Order, OrderDispute, PaymentTransaction


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'aggregated_pool', 'quantity_kg', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'buyer__country')
    search_fields = ('buyer__company_name', 'smart_contract_id')
    fieldsets = (
        ('Order Info', {'fields': ('buyer', 'aggregated_pool', 'status')}),
        ('Quantities', {'fields': ('quantity_kg', 'unit_price', 'product_cost', 'platform_fee', 'total_amount')}),
        ('Smart Contract', {'fields': ('smart_contract_id', 'smart_contract_address')}),
        ('Delivery', {'fields': ('expected_delivery_date', 'shipping_address', 'tracking_number')}),
        ('Timeline', {'fields': ('created_at', 'payment_received_at', 'shipped_at', 'delivered_at')}),
    )
    readonly_fields = ('created_at', 'product_cost', 'platform_fee', 'total_amount')


@admin.register(OrderDispute)
class OrderDisputeAdmin(admin.ModelAdmin):
    list_display = ('order', 'initiated_by', 'reason', 'status', 'created_at')
    list_filter = ('status', 'reason', 'initiated_by')


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_hash', 'order', 'payment_type', 'amount', 'status', 'created_at')
    list_filter = ('status', 'payment_type', 'created_at')
    search_fields = ('transaction_hash',)
    readonly_fields = ('transaction_hash', 'created_at')
