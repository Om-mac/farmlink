"""
Tests for Buyers App
"""

from django.test import TestCase
from django.contrib.auth.models import User
from buyers.models import Buyer


class BuyerModelTest(TestCase):
    """Test Buyer model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testbuyer',
            email='buyer@test.local',
            password='testpass123'
        )
    
    def test_buyer_creation(self):
        """Test creating a buyer"""
        buyer = Buyer.objects.create(
            user=self.user,
            company_name='Test Company',
            buyer_type='factory',
            location='Test Location',
            country='TestCountry',
            phone='1234567890',
            avg_monthly_orders=10,
            payment_method='escrow'
        )
        
        self.assertEqual(buyer.company_name, 'Test Company')
        self.assertEqual(buyer.buyer_type, 'factory')
        self.assertFalse(buyer.verified)
    
    def test_buyer_payment_success_rate(self):
        """Test payment success rate calculation"""
        buyer = Buyer.objects.create(
            user=self.user,
            company_name='Test Company',
            buyer_type='factory',
            location='Location',
            country='Country',
            phone='1234567890',
            avg_monthly_orders=10,
            payment_method='escrow'
        )
        
        buyer.total_purchases = 10
        buyer.successful_deliveries = 9
        
        self.assertAlmostEqual(buyer.payment_success_rate, 90.0)
    
    def test_buyer_string_representation(self):
        """Test buyer __str__"""
        buyer = Buyer.objects.create(
            user=self.user,
            company_name='Global Foods',
            buyer_type='factory',
            location='Dubai',
            country='UAE',
            phone='1234567890',
            avg_monthly_orders=10,
            payment_method='escrow'
        )
        
        self.assertEqual(str(buyer), 'Global Foods (UAE)')
