"""Buyer Models"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Buyer(models.Model):
    """Buyer/Purchaser Profile"""
    BUYER_TYPE_CHOICES = [
        ('factory', 'Food Factory'),
        ('distributor', 'Distributor'),
        ('retailer', 'Retailer'),
        ('individual', 'Individual'),
        ('exporter', 'Exporter'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    company_name = models.CharField(max_length=255)
    buyer_type = models.CharField(max_length=20, choices=BUYER_TYPE_CHOICES)
    location = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    
    # Order Details
    avg_monthly_orders = models.IntegerField(validators=[MinValueValidator(0)])
    payment_method = models.CharField(
        max_length=50,
        choices=[('credit', 'Credit Transfer'), ('prepay', 'Prepayment'), ('escrow', 'Smart Contract Escrow')]
    )
    
    # Financial
    annual_purchase_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    wallet_address = models.CharField(max_length=255, blank=True, help_text="Blockchain wallet for payments")
    bank_name = models.CharField(max_length=255, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    
    # Verification
    verified = models.BooleanField(default=False)
    documents = models.FileField(upload_to='buyer_docs/', blank=True)
    
    # Rating & History
    rating = models.FloatField(default=5.0, validators=[MinValueValidator(0)])
    total_purchases = models.IntegerField(default=0)
    successful_deliveries = models.IntegerField(default=0)
    dispute_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-rating', '-created_at']
    
    def __str__(self):
        return f"{self.company_name} ({self.country})"
    
    @property
    def payment_success_rate(self):
        if self.total_purchases == 0:
            return 100.0
        return (self.successful_deliveries / self.total_purchases) * 100
