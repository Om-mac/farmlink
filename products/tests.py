"""
Tests for Products App
"""

from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from farmers.models import Farmer, FarmProduct
from products.models import AggregatedProductPool, QualityAssurance


class AggregatedProductPoolTest(TestCase):
    """Test Aggregation Engine"""
    
    def setUp(self):
        # Create farmers
        self.farmers = []
        for i in range(3):
            user = User.objects.create_user(
                username=f'farmer{i}',
                email=f'farmer{i}@test.local',
                password='testpass123'
            )
            farmer = Farmer.objects.create(
                user=user,
                farm_name=f'Farm {i}',
                location=f'Location {i}',
                country='Country',
                phone=f'123456789{i}',
                farm_size_hectares=5.0 + i,
                certification='organic',
                years_in_business=5 + i,
                daily_production_kg=500 + (i * 100),
                max_order_size_kg=3000,
                min_order_size_kg=250,
                verified=True
            )
            self.farmers.append(farmer)
            
            # Add products
            FarmProduct.objects.create(
                farmer=farmer,
                product_name='Rice',
                daily_capacity_kg=500 + (i * 100),
                quality_grade='A',
                price_per_kg=Decimal('45.50'),
                verified=True
            )
    
    def test_pool_creation(self):
        """Test creating aggregated pool"""
        products = FarmProduct.objects.filter(product_name='Rice')
        
        pool = AggregatedProductPool.objects.create(
            product_name='Rice',
            total_available_kg=2500,
            target_quantity_kg=10000,
            average_price_per_kg=Decimal('45.50'),
            status='open'
        )
        pool.source_products.set(products)
        
        self.assertEqual(pool.get_participating_farmers_count(), 3)
        self.assertGreater(pool.calculate_total_value(), 0)
    
    def test_pool_farmer_count(self):
        """Test participating farmers count"""
        products = FarmProduct.objects.filter(product_name='Rice')
        
        pool = AggregatedProductPool.objects.create(
            product_name='Rice',
            total_available_kg=2500,
            target_quantity_kg=5000,
            average_price_per_kg=Decimal('45.50')
        )
        pool.source_products.set(products)
        
        self.assertEqual(pool.get_participating_farmers_count(), 3)


class QualityAssuranceTest(TestCase):
    """Test Quality Assurance"""
    
    def setUp(self):
        user = User.objects.create_user(
            username='farmer1',
            email='farmer@test.local',
            password='testpass123'
        )
        farmer = Farmer.objects.create(
            user=user,
            farm_name='Test Farm',
            location='Location',
            country='Country',
            phone='1234567890',
            farm_size_hectares=5.0,
            certification='organic',
            years_in_business=5,
            daily_production_kg=500,
            max_order_size_kg=3000,
            min_order_size_kg=250
        )
        
        product = FarmProduct.objects.create(
            farmer=farmer,
            product_name='Rice',
            daily_capacity_kg=500,
            price_per_kg=Decimal('45.50'),
            verified=True
        )
        
        self.pool = AggregatedProductPool.objects.create(
            product_name='Rice',
            total_available_kg=5000,
            target_quantity_kg=10000,
            average_price_per_kg=Decimal('45.50')
        )
        self.pool.source_products.add(product)
    
    def test_qa_creation(self):
        """Test creating QA record"""
        qa = QualityAssurance.objects.create(
            pool=self.pool,
            status='pending'
        )
        
        self.assertEqual(qa.status, 'pending')
        self.assertEqual(qa.pool, self.pool)
