"""
Tests for Farmers App
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Farmer, FarmProduct


class FarmerModelTest(TestCase):
    """Test Farmer model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testfarmer',
            email='farmer@test.local',
            password='testpass123'
        )
    
    def test_farmer_creation(self):
        """Test creating a farmer"""
        farmer = Farmer.objects.create(
            user=self.user,
            farm_name='Test Farm',
            location='Test Location',
            country='TestCountry',
            phone='1234567890',
            farm_size_hectares=5.0,
            certification='organic',
            years_in_business=5,
            daily_production_kg=500,
            max_order_size_kg=2000,
            min_order_size_kg=250
        )
        
        self.assertEqual(farmer.farm_name, 'Test Farm')
        self.assertEqual(farmer.daily_production_kg, 500)
        self.assertFalse(farmer.verified)
    
    def test_farmer_string_representation(self):
        """Test farmer __str__"""
        farmer = Farmer.objects.create(
            user=self.user,
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
        
        self.assertEqual(str(farmer), 'Test Farm (Location, Country)')


class FarmProductTest(TestCase):
    """Test FarmProduct model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testfarmer',
            email='farmer@test.local',
            password='testpass123'
        )
        self.farmer = Farmer.objects.create(
            user=self.user,
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
    
    def test_farm_product_creation(self):
        """Test creating a farm product"""
        product = FarmProduct.objects.create(
            farmer=self.farmer,
            product_name='Rice',
            daily_capacity_kg=500,
            quality_grade='A',
            price_per_kg=45.50
        )
        
        self.assertEqual(product.product_name, 'Rice')
        self.assertEqual(product.daily_capacity_kg, 500)
        self.assertEqual(str(product.price_per_kg), '45.50')


class FarmerAPITest(TestCase):
    """Test Farmer API endpoints"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testfarmer',
            email='farmer@test.local',
            password='testpass123'
        )
    
    def test_farmer_list_api(self):
        """Test GET /farmers/"""
        response = self.client.get('/api/farmers/')
        self.assertEqual(response.status_code, 200)
