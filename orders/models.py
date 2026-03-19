"""Orders Models - Smart Contract Escrow"""

from django.db import models
from buyers.models import Buyer
from products.models import AggregatedProductPool
from django.core.validators import MinValueValidator
from decimal import Decimal


class Order(models.Model):
    """
    Order created by buyer from aggregated pool.
    Uses smart contract for trust and payment handling.
    """
    ORDER_STATUS = [
        ('pending', 'Pending - Awaiting Payment'),
        ('escrow_locked', 'Escrow Locked - Payment Received'),
        ('processing', 'Processing - Quality Check'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed - Payment Released'),
        ('disputed', 'Disputed'),
        ('cancelled', 'Cancelled'),
    ]
    
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='orders')
    aggregated_pool = models.ForeignKey(AggregatedProductPool, on_delete=models.CASCADE, related_name='orders')
    
    # Order Details
    quantity_kg = models.FloatField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Pricing Breakdown
    product_cost = models.DecimalField(max_digits=15, decimal_places=2)  # quantity * unit_price
    platform_fee = models.DecimalField(max_digits=15, decimal_places=2)  # 2% of product_cost
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)  # product_cost + platform_fee
    
    # Payment & Smart Contract
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    smart_contract_id = models.CharField(max_length=255, blank=True, help_text="Blockchain transaction hash")
    smart_contract_address = models.CharField(max_length=255, blank=True)
    
    # Delivery
    expected_delivery_date = models.DateField()
    shipping_address = models.TextField()
    tracking_number = models.CharField(max_length=255, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    payment_received_at = models.DateTimeField(null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.buyer.company_name} - {self.aggregated_pool.product_name}"
    
    def calculate_costs(self):
        """Calculate all costs"""
        self.product_cost = Decimal(str(self.quantity_kg)) * self.unit_price
        self.platform_fee = self.product_cost * Decimal('0.02')  # 2% platform fee
        self.total_amount = self.product_cost + self.platform_fee
        return self


class OrderDispute(models.Model):
    """Handle disputes between buyer and farmers"""
    DISPUTE_STATUS = [
        ('open', 'Open'),
        ('investigating', 'Under Investigation'),
        ('resolved', 'Resolved'),
        ('escalated', 'Escalated to Admin'),
    ]
    
    DISPUTE_REASON = [
        ('quality', 'Quality Issue'),
        ('quantity_short', 'Quantity Shortage'),
        ('late_delivery', 'Late Delivery'),
        ('non_delivery', 'Non-Delivery'),
        ('payment_issue', 'Payment Issue'),
        ('other', 'Other'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='dispute')
    initiated_by = models.CharField(max_length=20, choices=[('buyer', 'Buyer'), ('farmer', 'Farmer')])
    reason = models.CharField(max_length=50, choices=DISPUTE_REASON)
    description = models.TextField()
    evidence = models.FileField(upload_to='dispute_evidence/', blank=True)
    
    status = models.CharField(max_length=20, choices=DISPUTE_STATUS, default='open')
    proposed_resolution = models.TextField(blank=True)
    final_resolution = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dispute Order #{self.order.id} - {self.reason}"


class PaymentTransaction(models.Model):
    """Track all payment transactions via smart contracts"""
    PAYMENT_STATUS = [
        ('initiated', 'Initiated'),
        ('pending_confirmation', 'Pending Blockchain Confirmation'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_TYPE = [
        ('order_payment', 'Order Payment'),
        ('refund', 'Refund'),
        ('settlement', 'Farmer Settlement'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment_transactions')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Blockchain Details
    transaction_hash = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    blockchain_timestamp = models.DateTimeField(null=True, blank=True)
    block_number = models.BigIntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment {self.transaction_hash[:16]}... - {self.amount} ({self.status})"
