"""Products Models"""

from django.db import models
from farmers.models import FarmProduct
from django.core.validators import MinValueValidator


class AggregatedProductPool(models.Model):
    """
    Aggregates multiple farmers' products to meet bulk buyer requirements.
    This solves the "Scale Mismatch" problem by bundling smaller farms.
    """
    product_name = models.CharField(max_length=255)
    source_products = models.ManyToManyField(FarmProduct, related_name='aggregated_pools')
    
    # Pool Characteristics
    total_available_kg = models.FloatField(validators=[MinValueValidator(0)])
    target_quantity_kg = models.FloatField(validators=[MinValueValidator(0)])
    
    # Pricing
    average_price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee_percentage = models.FloatField(default=2.0)  # 2% fee
    
    # Status
    POOL_STATUS = [
        ('open', 'Open - Accepting Orders'),
        ('active', 'Active - Fulfilling Order'),
        ('closed', 'Closed - Fulfilled'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=POOL_STATUS, default='open')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product_name} (Pool: {self.total_available_kg}kg)"
    
    def get_participating_farmers_count(self):
        return self.source_products.values('farmer').distinct().count()
    
    def calculate_total_value(self):
        """Calculate total pool value"""
        return float(self.total_available_kg) * float(self.average_price_per_kg)


class QualityAssurance(models.Model):
    """Quality certification for aggregated products"""
    pool = models.OneToOneField(AggregatedProductPool, on_delete=models.CASCADE, related_name='quality_assurance')
    
    QUALITY_STATUS = [
        ('pending', 'Pending Inspection'),
        ('inspected', 'Inspected & Passed'),
        ('rejected', 'Rejected'),
    ]
    
    status = models.CharField(max_length=20, choices=QUALITY_STATUS, default='pending')
    inspector_name = models.CharField(max_length=255, blank=True)
    inspection_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    certificate = models.FileField(upload_to='qa_certificates/', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"QA for {self.pool.product_name}"
