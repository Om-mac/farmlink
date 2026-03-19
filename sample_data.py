"""
Sample Data Generation for FarmLink Hackathon Demo
Creates minimal but complete data for demonstration
Run: python sample_data.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.contrib.auth.models import User
from farmers.models import Farmer, FarmProduct
from buyers.models import Buyer
from products.models import AggregatedProductPool
from orders.models import Order
from smartcontracts.models import SmartContract
from datetime import datetime


def clear_data():
    """Clear existing data (optional)"""
    print("Clearing existing data...")
    User.objects.all().delete()
    print("✓ Data cleared")


def create_farmers():
    """Create 3 sample farmers with different capacities"""
    print("\n📍 Creating Farmers...")
    
    farmers_data = [
        {
            'username': 'farmer_green_valley',
            'password': 'demo123',
            'farm_name': 'Green Valley Farm',
            'location': 'Bangalore',
            'country': 'India',
            'phone': '9876543210',
            'daily_production_kg': 500,
            'farm_size_hectares': 5,
            'certification': 'organic',
            'years_in_business': 8,
            'min_order_size_kg': 100,
            'max_order_size_kg': 500,
            'wallet_address': '0x1234567890123456789012345678901234567890',
        },
        {
            'username': 'farmer_sunrise',
            'password': 'demo123',
            'farm_name': 'Sunrise Organic Farm',
            'location': 'Pune',
            'country': 'India',
            'phone': '9876543211',
            'daily_production_kg': 600,
            'farm_size_hectares': 6,
            'certification': 'organic',
            'years_in_business': 10,
            'min_order_size_kg': 100,
            'max_order_size_kg': 600,
            'wallet_address': '0x2234567890123456789012345678901234567891',
        },
        {
            'username': 'farmer_golden_harvest',
            'password': 'demo123',
            'farm_name': 'Golden Harvest Farm',
            'location': 'Indore',
            'country': 'India',
            'phone': '9876543212',
            'daily_production_kg': 550,
            'farm_size_hectares': 5.5,
            'certification': 'fair_trade',
            'years_in_business': 12,
            'min_order_size_kg': 100,
            'max_order_size_kg': 550,
            'wallet_address': '0x3234567890123456789012345678901234567892',
        },
    ]
    
    farmers = []
    for farmer_data in farmers_data:
        username = farmer_data.pop('username')
        password = farmer_data.pop('password')
        
        # Create user
        user = User.objects.create_user(username=username, password=password)
        
        # Create farmer profile
        farmer = Farmer.objects.create(user=user, verified=True, **farmer_data)
        farmers.append(farmer)
        print(f"✓ {farmer.farm_name} ({farmer.daily_production_kg}kg/day)")
    
    return farmers


def create_farm_products(farmers):
    """Create products for each farmer"""
    print("\n📦 Creating Farm Products...")
    
    products = []
    product_specs = [
        {
            'product_name': 'Tomatoes',
            'price_per_kg': 50,
            'daily_capacity_kg': 500,
            'quality_grade': 'A',
        },
        {
            'product_name': 'Tomatoes',
            'price_per_kg': 48,
            'daily_capacity_kg': 600,
            'quality_grade': 'A',
        },
        {
            'product_name': 'Tomatoes',
            'price_per_kg': 49,
            'daily_capacity_kg': 550,
            'quality_grade': 'A',
        },
    ]
    
    for farmer, spec in zip(farmers, product_specs):
        product = FarmProduct.objects.create(
            farmer=farmer,
            product_name=spec['product_name'],
            price_per_kg=spec['price_per_kg'],
            daily_capacity_kg=spec['daily_capacity_kg'],
            quality_grade=spec['quality_grade'],
            verified=True,
        )
        products.append(product)
        print(f"✓ {farmer.farm_name}: {spec['daily_capacity_kg']}kg {spec['product_name']} @ ₹{spec['price_per_kg']}/kg")
    
    return products


def create_buyer():
    """Create a sample buyer"""
    print("\n🏭 Creating Buyer...")
    
    user = User.objects.create_user(
        username='buyer_nestle',
        password='demo123'
    )
    
    buyer = Buyer.objects.create(
        user=user,
        company_name='Nestle India Ltd',
        buyer_type='factory',
        location='Mumbai',
        country='India',
        phone='9876543220',
        wallet_address='0x0234567890123456789012345678901234567890',
        verified=True,
        avg_monthly_orders=10,
        payment_method='escrow',
    )
    
    print(f"✓ {buyer.company_name} ({buyer.location})")
    return buyer


def create_aggregated_pool(products):
    """Create aggregated pool from multiple products"""
    print("\n♻️  Creating Aggregated Product Pool...")
    
    from decimal import Decimal
    
    pool = AggregatedProductPool.objects.create(
        product_name='Tomatoes Bundle',
        total_available_kg=1650,  # Sum of 3 farmers
        target_quantity_kg=2000,
        average_price_per_kg=Decimal('49'),
        platform_fee_percentage=2,
        status='open'
    )
    
    # Add all products to pool
    pool.source_products.set(products)
    pool.save()
    
    num_farmers = pool.get_participating_farmers_count()
    print(f"✓ Pool created: {pool.total_available_kg}kg from {num_farmers} farmers")
    print(f"  Average price: ₹{pool.average_price_per_kg}/kg (2% platform fee)")
    
    return pool


def create_order(buyer, pool):
    """Create an order from the aggregated pool"""
    print("\n📋 Creating Order...")
    
    from decimal import Decimal
    from datetime import datetime, timedelta
    
    # Calculate costs first
    quantity_kg = 1500
    unit_price = pool.average_price_per_kg
    product_cost = Decimal(str(quantity_kg)) * unit_price
    platform_fee = product_cost * Decimal('0.02')  # 2% fee
    total_amount = product_cost + platform_fee
    
    order = Order.objects.create(
        buyer=buyer,
        aggregated_pool=pool,
        quantity_kg=quantity_kg,
        unit_price=unit_price,
        product_cost=product_cost,
        platform_fee=platform_fee,
        total_amount=total_amount,
        shipping_address='Mumbai Port Terminal, Mumbai, India',
        expected_delivery_date=(datetime.now() + timedelta(days=7)).date(),
        status='pending',
    )
    
    print(f"✓ Order created: {order.quantity_kg}kg from {buyer.company_name}")
    print(f"  Product Cost: ₹{order.product_cost:,.0f}")
    print(f"  Platform Fee (2%): ₹{order.platform_fee:,.0f}")
    print(f"  Total: ₹{order.total_amount:,.0f}")
    
    return order


def create_smart_contract(order, pool, farmers):
    """Create smart contract for payment escrow"""
    print("\n⛓️  Creating Smart Contract (Escrow)...")
    
    from datetime import datetime, timedelta
    import random
    
    # Calculate farmer payments proportionally
    seller_wallets = []
    total_amount = float(order.total_amount)
    
    for product in pool.source_products.all():
        farmer = product.farmer
        farmer_share_pct = (product.daily_capacity_kg / pool.total_available_kg) * 100
        farmer_share_amt = (product.daily_capacity_kg / pool.total_available_kg) * total_amount
        
        seller_wallets.append({
            'name': farmer.farm_name,
            'wallet': farmer.wallet_address,
            'amount': round(farmer_share_amt, 2),
            'percentage': round(farmer_share_pct, 1)
        })
    
    # Create smart contract
    contract_address = f"0x{random.randint(1000000000, 9999999999)}{random.randint(1000000000, 9999999999)}"
    
    contract = SmartContract.objects.create(
        order=order,
        contract_type='order_escrow',
        status='active',
        contract_address=contract_address,
        buyer_wallet=order.buyer.wallet_address,
        seller_wallets=[w['wallet'] for w in seller_wallets],
        escrow_amount=order.total_amount,
        delivery_deadline=(datetime.now() + timedelta(days=7)),
    )
    
    print(f"✓ Smart contract created (Status: {contract.status})")
    print(f"  Contract Address: {contract_address}")
    print(f"  Escrow Amount: ₹{contract.escrow_amount:,.0f}")
    print(f"  Recipients:")
    for wallet_data in seller_wallets:
        print(f"    - {wallet_data['name']}: ₹{wallet_data['amount']:,.0f} ({wallet_data['percentage']}%)")
    
    return contract


def create_all_sample_data():
    """Main function to create all sample data"""
    print("=" * 60)
    print("🌾 FarmLink Hackathon Demo - Sample Data Generation")
    print("=" * 60)
    
    try:
        # Check if data already exists
        if Farmer.objects.exists():
            print("⚠️  Sample data already exists!")
            print("\nTo reset, run: python manage.py flush")
            return
        
        # Create data in order
        farmers = create_farmers()
        products = create_farm_products(farmers)
        buyer = create_buyer()
        pool = create_aggregated_pool(products)
        order = create_order(buyer, pool)
        contract = create_smart_contract(order, pool, farmers)
        
        print("\n" + "=" * 60)
        print("✅ Sample Data Created Successfully!")
        print("=" * 60)
        print("\n📍 Test the API:")
        print("  • Farmers: http://127.0.0.1:8000/api/farmers/")
        print("  • Buyers: http://127.0.0.1:8000/api/buyers/")
        print("  • Products: http://127.0.0.1:8000/api/products/")
        print("  • Orders: http://127.0.0.1:8000/api/orders/")
        print("  • Smart Contracts: http://127.0.0.1:8000/api/smartcontracts/")
        print("\n📋 See BASIC_WORKFLOW.md for complete flow documentation")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error creating sample data: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    create_all_sample_data()
