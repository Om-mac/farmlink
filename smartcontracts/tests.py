"""
Tests for Smart Contracts
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from farmers.models import Farmer, FarmProduct
from buyers.models import Buyer
from products.models import AggregatedProductPool
from orders.models import Order
from smartcontracts.models import SmartContract, ContractEvent
from smartcontracts.blockchain_service import AWSManagedBlockchainService


class SmartContractModelTest(TestCase):
    """Test SmartContract model"""
    
    def setUp(self):
        # Setup buyer and order
        buyer_user = User.objects.create_user(
            username='testbuyer',
            email='buyer@test.local',
            password='testpass123'
        )
        self.buyer = Buyer.objects.create(
            user=buyer_user,
            company_name='Test Company',
            buyer_type='factory',
            location='Loc',
            country='Country',
            phone='1234567890',
            avg_monthly_orders=5,
            payment_method='escrow',
            wallet_address='0x123456789'
        )
        
        farmer_user = User.objects.create_user(
            username='testfarmer',
            email='farmer@test.local',
            password='testpass123'
        )
        farmer = Farmer.objects.create(
            user=farmer_user,
            farm_name='Test Farm',
            location='Location',
            country='Country',
            phone='1234567890',
            farm_size_hectares=5.0,
            certification='organic',
            years_in_business=5,
            daily_production_kg=500,
            max_order_size_kg=2000,
            min_order_size_kg=250,
            wallet_address='0x987654321'
        )
        
        product = FarmProduct.objects.create(
            farmer=farmer,
            product_name='Rice',
            daily_capacity_kg=500,
            price_per_kg=Decimal('45.50')
        )
        
        pool = AggregatedProductPool.objects.create(
            product_name='Rice',
            total_available_kg=5000,
            target_quantity_kg=10000,
            average_price_per_kg=Decimal('45.50'),
            status='open'
        )
        pool.source_products.add(product)
        
        self.order = Order.objects.create(
            buyer=self.buyer,
            aggregated_pool=pool,
            quantity_kg=1000,
            unit_price=Decimal('45.50'),
            expected_delivery_date=timezone.now().date()
        )
        self.order.calculate_costs()
        self.order.save()
    
    def test_smart_contract_creation(self):
        """Test creating a smart contract"""
        contract = SmartContract.objects.create(
            order=self.order,
            contract_type='order_escrow',
            status='deployed',
            contract_address='0xabcd1234',
            buyer_wallet='0x123456789',
            seller_wallets=['0x987654321'],
            escrow_amount=Decimal('1000'),
            delivery_deadline=timezone.now() + timedelta(days=30),
            deployment_tx_hash='0xtx123'
        )
        
        self.assertEqual(contract.contract_type, 'order_escrow')
        self.assertEqual(contract.status, 'deployed')
        self.assertEqual(contract.escrow_amount, Decimal('1000'))


class BlockchainServiceTest(TestCase):
    """Test blockchain service"""
    
    def setUp(self):
        self.service = AWSManagedBlockchainService()
    
    def test_contract_address_generation(self):
        """Test contract address generation"""
        addr = self.service._generate_contract_address()
        self.assertTrue(addr.startswith('0x'))
        self.assertEqual(len(addr), 42)  # 0x + 40 hex chars
    
    def test_tx_hash_generation(self):
        """Test transaction hash generation"""
        tx_hash = self.service._generate_tx_hash()
        self.assertTrue(tx_hash.startswith('0x'))
        self.assertEqual(len(tx_hash), 66)  # 0x + 64 hex chars
