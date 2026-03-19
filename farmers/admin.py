from django.contrib import admin
from .models import Farmer, FarmProduct


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('farm_name', 'location', 'country', 'rating', 'verified', 'created_at')
    list_filter = ('verified', 'certification', 'country')
    search_fields = ('farm_name', 'location', 'user__email')
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Farm Info', {'fields': ('farm_name', 'location', 'latitude', 'longitude', 'country', 'phone')}),
        ('Farm Details', {'fields': ('farm_size_hectares', 'certification', 'years_in_business')}),
        ('Production Capacity', {'fields': ('daily_production_kg', 'max_order_size_kg', 'min_order_size_kg')}),
        ('Banking', {'fields': ('bank_name', 'account_holder', 'account_number', 'wallet_address')}),
        ('Documentation', {'fields': ('tax_id', 'documents')}),
        ('Status', {'fields': ('rating', 'total_orders', 'on_time_delivery_rate', 'verified')}),
    )


@admin.register(FarmProduct)
class FarmProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'farmer', 'daily_capacity_kg', 'price_per_kg', 'verified')
    list_filter = ('verified', 'farmer', 'quality_grade')
    search_fields = ('product_name', 'farmer__farm_name')
