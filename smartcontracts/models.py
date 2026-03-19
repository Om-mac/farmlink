"""Smart Contracts Models - Blockchain Integration"""

from django.db import models
from orders.models import Order
from django.core.validators import MinValueValidator


class SmartContract(models.Model):
    """Blockchain smart contract for order escrow and payment"""
    CONTRACT_TYPE = [
        ('order_escrow', 'Order Escrow'),
        ('bulk_aggregation', 'Bulk Aggregation'),
    ]
    
    CONTRACT_STATUS = [
        ('deployed', 'Deployed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='smart_contract', null=True, blank=True)
    contract_type = models.CharField(max_length=50, choices=CONTRACT_TYPE)
    status = models.CharField(max_length=20, choices=CONTRACT_STATUS, default='deployed')
    
    # Blockchain Details
    contract_address = models.CharField(max_length=255, unique=True)
    network = models.CharField(max_length=50, default='AWS_MANAGED_BLOCKCHAIN')
    chain_id = models.IntegerField(default=1)
    
    # Contract Parameters
    buyer_wallet = models.CharField(max_length=255)
    seller_wallets = models.JSONField(default=list, help_text="List of farmer wallet addresses")
    escrow_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Conditions
    delivery_deadline = models.DateTimeField()
    dispute_period_days = models.IntegerField(default=30)
    
    # Execution
    deployed_at = models.DateTimeField(null=True, blank=True)
    activated_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Auditing
    deployment_tx_hash = models.CharField(max_length=255, blank=True)
    activation_tx_hash = models.CharField(max_length=255, blank=True)
    completion_tx_hash = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"SC {self.contract_address[:16]}... - {self.contract_type} ({self.status})"


class ContractEvent(models.Model):
    """Log of all events from smart contract execution"""
    EVENT_TYPE = [
        ('created', 'Contract Created'),
        ('funded', 'Escrow Funded'),
        ('payment_released', 'Payment Released'),
        ('refund_initiated', 'Refund Initiated'),
        ('dispute_filed', 'Dispute Filed'),
        ('dispute_resolved', 'Dispute Resolved'),
    ]
    
    contract = models.ForeignKey(SmartContract, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE)
    event_hash = models.CharField(max_length=255, unique=True)
    
    # Event Data
    data = models.JSONField()  # Event parameters
    block_number = models.BigIntegerField()
    transaction_hash = models.CharField(max_length=255)
    log_index = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.event_type} - {self.event_hash[:16]}..."


class AWSManagedBlockchainConfig(models.Model):
    """Configuration for AWS Managed Blockchain integration"""
    network_name = models.CharField(max_length=255, unique=True)
    framework = models.CharField(max_length=50, choices=[('HYPERLEDGER_FABRIC', 'Hyperledger Fabric'), ('ETHEREUM', 'Ethereum')])
    network_id = models.CharField(max_length=255)
    member_id = models.CharField(max_length=255)
    
    # RPC Endpoint
    rpc_endpoint = models.CharField(max_length=255)
    rpc_username = models.CharField(max_length=255, blank=True)
    rpc_password = models.CharField(max_length=255, blank=True)
    
    # Credentials
    access_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)
    region = models.CharField(max_length=50, default='us-east-1')
    
    # Smart Contract Details
    smart_contract_arn = models.CharField(max_length=255, blank=True)
    contract_deployed_address = models.CharField(max_length=255, blank=True)
    
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "AWS Managed Blockchain Configs"
    
    def __str__(self):
        return f"AMB Config - {self.network_name}"
