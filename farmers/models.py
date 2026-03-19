"""Farmer Models"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Farmer(models.Model):
    """Farmer Profile"""
    CERTIFICATION_CHOICES = [
        ('organic', 'Organic Certified'),
        ('fair_trade', 'Fair Trade Certified'),
        ('conventional', 'Conventional'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    farm_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    
    # Farm Details
    farm_size_hectares = models.FloatField(validators=[MinValueValidator(0)])
    certification = models.CharField(max_length=20, choices=CERTIFICATION_CHOICES)
    years_in_business = models.IntegerField(validators=[MinValueValidator(0)])
    
    # Capacity
    daily_production_kg = models.FloatField(validators=[MinValueValidator(0)])
    max_order_size_kg = models.FloatField(validators=[MinValueValidator(0)])
    min_order_size_kg = models.FloatField(validators=[MinValueValidator(0)])
    
    # Banking/Payment
    bank_name = models.CharField(max_length=255, blank=True)
    account_holder = models.CharField(max_length=255, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    wallet_address = models.CharField(max_length=255, blank=True, help_text="Blockchain wallet address for smart contract")
    
    # Documentation
    tax_id = models.CharField(max_length=50, blank=True)
    documents = models.FileField(upload_to='farmer_docs/', blank=True, help_text="Certificates, licenses, etc.")
    
    # Rating & Reputation
    rating = models.FloatField(default=5.0, validators=[MinValueValidator(0), ])
    total_orders = models.IntegerField(default=0)
    on_time_delivery_rate = models.FloatField(default=100.0)  # percentage
    
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-rating', '-created_at']
    
    def __str__(self):
        return f"{self.farm_name} ({self.location}, {self.country})"


class FarmProduct(models.Model):
    """Products a Farmer Produces"""
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='available_products')
    product_name = models.CharField(max_length=255)
    product_category = models.CharField(
        max_length=20,
        choices=[('vegetable', 'Vegetable'), ('fruit', 'Fruit')],
        default='vegetable'
    )
    
    # Capacity Info
    daily_capacity_kg = models.FloatField(validators=[MinValueValidator(0)])
    year_round_available = models.BooleanField(default=False)
    harvest_season_start = models.DateField(null=True, blank=True)
    harvest_season_end = models.DateField(null=True, blank=True)
    
    quality_grade = models.CharField(
        max_length=10,
        choices=[('A', 'Grade A'), ('B', 'Grade B'), ('C', 'Grade C')],
        default='A'
    )
    product_photo = models.ImageField(upload_to='product_photos/', blank=True, null=True)
    quality_certificate = models.FileField(upload_to='product_certificates/', blank=True, null=True)
    
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    available_quantity_kg = models.FloatField(validators=[MinValueValidator(0)], default=0)
    
    verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product_name} - {self.farmer.farm_name}"
