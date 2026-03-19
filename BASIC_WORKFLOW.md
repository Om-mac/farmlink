# FarmLink - Basic Hackathon Prototype Workflow

## 🎯 Core Problem
Small farmers (500kg/day) can't supply factories needing 10 tonnes/day. **Smart contracts solve trust issues and aggregate supply automatically.**

## 📊 5-Step Demo Workflow

### Step 1: Register Farmers
```bash
POST /api/farmers/
{
  "user": {"username": "farmer1", "password": "pass123"},
  "farm_name": "Green Valley Farm",
  "location": "Bangalore",
  "country": "India",
  "phone": "9876543210",
  "daily_production_kg": 500,
  "certification": "organic"
}
```

### Step 2: Register Buyer
```bash
POST /api/buyers/
{
  "user": {"username": "buyer1", "password": "pass123"},
  "company_name": "Nestle India",
  "location": "Mumbai",
  "country": "India",
  "phone": "9876543211"
}
```

### Step 3: Add Farm Products
```bash
POST /api/products/farm-products/
{
  "farmer": 1,
  "product_name": "Tomatoes",
  "price_per_kg": 50,
  "available_quantity_kg": 500,
  "quality_grade": "A"
}
```

### Step 4: Create Aggregated Pool (System Auto)
```bash
POST /api/products/aggregated-pools/
{
  "product_name": "Tomatoes",
  "source_products": [1, 2, 3],  // Multiple farmers
  "total_available_kg": 1500,
  "target_quantity_kg": 2000,
  "average_price_per_kg": 50,
  "platform_fee_percentage": 2
}
```

### Step 5: Create Order & Process Payment
```bash
POST /api/orders/
{
  "buyer": 1,
  "aggregated_pool": 1,
  "quantity_kg": 1500,
  "delivery_location": "Mumbai"
}

// Smart contract automatically:
// - Locks funds on blockchain
// - Creates escrow
// - Distributes to multiple farmers
// - Releases on delivery confirmation
```

---

## 🔄 Data Flow

```
FARMER REGISTRATION
        ↓
   CREATE PRODUCTS
        ↓
  AUTOMATIC AGGREGATION (Multiple Farmers → 1 Pool)
        ↓
   BUYER REGISTRATION
        ↓
   BUYER CREATES ORDER (from pool)
        ↓
  SMART CONTRACT ESCROW (funds locked on blockchain)
        ↓
   DELIVERY CONFIRMATION
        ↓
  AUTOMATIC PAYMENT DISTRIBUTION (to all farmers)
```

---

## 🚀 Quick Start Commands

### 1. Load Sample Data
```bash
python manage.py migrate
python sample_data.py  # Creates 3 farmers, 1 buyer, products, pool, order
```

### 2. Start Server
```bash
python manage.py runserver
```

### 3. Test Endpoints
```bash
# Get all farmers
curl http://127.0.0.1:8000/api/farmers/

# Get all buyers  
curl http://127.0.0.1:8000/api/buyers/

# Get all products
curl http://127.0.0.1:8000/api/products/

# Get all orders
curl http://127.0.0.1:8000/api/orders/

# Get smart contracts
curl http://127.0.0.1:8000/api/smartcontracts/
```

---

## 📱 API Endpoints (Simplified for Hackathon)

### Farmers
- `GET /api/farmers/` - List all farmers
- `POST /api/farmers/` - Register new farmer
- `GET /api/farmers/{id}/` - Get farmer details

### Buyers
- `GET /api/buyers/` - List all buyers
- `POST /api/buyers/` - Register new buyer
- `GET /api/buyers/{id}/` - Get buyer details

### Products
- `GET /api/products/farm-products/` - List all farm products
- `POST /api/products/farm-products/` - Add new product
- `GET /api/products/aggregated-pools/` - List aggregated pools
- `POST /api/products/aggregated-pools/` - Create pool

### Orders
- `GET /api/orders/` - List all orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/{id}/` - Get order details

### Smart Contracts
- `GET /api/smartcontracts/` - List contracts
- `POST /api/smartcontracts/` - Create escrow contract
- `POST /api/smartcontracts/{id}/release-payment/` - Release funds after delivery

---

## ✅ Demonstrated Features

1. ✅ **Farmer Registration & Profiles** - Multiple farmers with different capacities
2. ✅ **Buyer Registration** - Company portal
3. ✅ **Product Listing** - Individual farm products
4. ✅ **Automatic Aggregation** - Multiple 500kg farms → 2000kg pool
5. ✅ **Order Creation** - From aggregated pools
6. ✅ **Smart Contract Escrow** - Funds locked on blockchain
7. ✅ **Payment Distribution** - Automatic split to multiple farmers
8. ✅ **Transparent Pricing** - 2% platform fee included

---

## 🎬 Demo Script (2 minutes)

1. Show registered farmers on `/api/farmers/`
2. Show aggregated pool combining 3 farmers on `/api/products/aggregated-pools/`
3. Show completed order on `/api/orders/`
4. Show smart contract with locked funds on `/api/smartcontracts/`
5. Explain: "Factory gets 2000kg from 3 farmers, farmers get paid immediately via blockchain"

---

## 🔒 Scale Mismatch Solution Proven

| Problem | Before | FarmLink Solution |
|---------|--------|------------------|
| Supply | 3 × 500kg farms | → 1500kg pool ✅ |
| Trust | Separate contracts | → Single smart contract ✅ |
| Payment | 2-4 weeks | → Instant blockchain ✅ |
| Cost | 1.5-3% fee | → 2% platform fee ✅ |
