from django.contrib import admin
from .models import AggregatedProductPool, QualityAssurance


@admin.register(AggregatedProductPool)
class AggregatedProductPoolAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'status', 'total_available_kg', 'average_price_per_kg', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('product_name',)
    fieldsets = (
        ('Product Info', {'fields': ('product_name', 'source_products', 'status')}),
        ('Pool Capacities', {'fields': ('total_available_kg', 'target_quantity_kg')}),
        ('Pricing', {'fields': ('average_price_per_kg', 'platform_fee_percentage')}),
    )
    filter_horizontal = ('source_products',)


@admin.register(QualityAssurance)
class QualityAssuranceAdmin(admin.ModelAdmin):
    list_display = ('pool', 'status', 'inspection_date')
    list_filter = ('status', 'inspection_date')
    search_fields = ('pool__product_name',)
