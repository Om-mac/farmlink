from django.contrib import admin
from .models import Buyer


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'buyer_type', 'country', 'rating', 'verified', 'created_at')
    list_filter = ('verified', 'buyer_type', 'country')
    search_fields = ('company_name', 'location', 'user__email')
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Company Info', {'fields': ('company_name', 'buyer_type', 'location', 'country', 'phone')}),
        ('Order Details', {'fields': ('avg_monthly_orders', 'payment_method')}),
        ('Financial', {'fields': ('annual_purchase_value', 'wallet_address', 'bank_name', 'account_number')}),
        ('Status', {'fields': ('rating', 'total_purchases', 'successful_deliveries', 'dispute_count', 'verified')}),
    )
