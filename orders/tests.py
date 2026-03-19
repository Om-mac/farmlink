"""
Tests for Orders App
"""

from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from farmers.models import Farmer, FarmProduct
from buyers.models import Buyer
from products.models import AggregatedProductPool
from orders.models import Order


class OrderModelTest(TestCase):
    """Test Order model"""
    
    def setUp(self):
        # Create farmer
        farmer_user = User.objects.create_user(
            username='testfarmer',
            email='farmer@test.local',
            password='testpass123'
        )
        self.farmer = Farmer.objects.create(
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
            min_order_size_kg=250
        )
        
        # Create product
        self.product = FarmProduct.objects.create(
            farmer=self.farmer,
            product_name='Rice',
            daily_capacity_kg=500,
            quality_grade='A',
            price_per_kg=Decimal('45.50')
        )
        
        # Create aggregated pool
        self.pool = AggregatedProductPool.objects.create(
            product_name='Rice',
            total_available_kg=5000,
            target_quantity_kg=10000,
            average_price_per_kg=Decimal('45.50'),
            status='open'
        )
        self.pool.source_products.add(self.product)
        
        # Create buyer
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
            payment_method='escrow'
        )
    
    def test_order_creation(self):
        """Test creating an order"""
        order = Order.objects.create(
            buyer=self.buyer,
            aggregated_pool=self.pool,
            quantity_kg=1000,
            unit_price=Decimal('45.50'),
            expected_delivery_date='2026-04-20'
        )
        order.calculate_costs()
        order.save()
        
        self.assertEqual(order.quantity_kg, 1000)
        self.assertEqual(order.status, 'pending')
        self.assertGreater(order.total_amount, 0)
    
    def test_order_cost_calculation(self):
        """Test cost calculation"""
        order = Order.objects.create(
            buyer=self.buyer,
            aggregated_pool=self.pool,
            quantity_kg=1000,
            unit_price=Decimal('45.50'),
            expected_delivery_date='2026-04-20'
        )
        order.calculate_costs()
        
        expected_product_cost = Decimal('1000') * Decimal('45.50')
        expected_fee = expected_product_cost * Decimal('0.02')
        
        self.assertEqual(order.product_cost, expected_product_cost)
        self.assertEqual(order.platform_fee, expected_fee)
