# FarmLink Hackathon - Demo Guide

## ⚡ Quick Setup (3 minutes)

### 1. Database Setup
```bash
python manage.py migrate
```

### 2. Load Sample Data
```bash
python sample_data.py
```

Expected output:
```
============================================================
🌾 FarmLink Hackathon Demo - Sample Data Generation
============================================================

📍 Creating Farmers...
✓ Green Valley Farm (500kg/day)
✓ Sunrise Organic Farm (600kg/day)
✓ Golden Harvest Farm (550kg/day)

📦 Creating Farm Products...
✓ Green Valley Farm: 500kg Tomatoes @ ₹50/kg
✓ Sunrise Organic Farm: 600kg Tomatoes @ ₹48/kg
✓ Golden Harvest Farm: 550kg Tomatoes @ ₹49/kg

🏭 Creating Buyer...
✓ Nestle India Ltd (Mumbai)

♻️  Creating Aggregated Product Pool...
✓ Pool created: 1650kg from 3 farmers

📋 Creating Order...
✓ Order created: 1500kg from Nestle India Ltd
  Amount: ₹73,500
  Platform Fee (2%): ₹1,470
  Total: ₹74,970

⛓️  Creating Smart Contract (Escrow)...
✓ Smart contract created (Status: active)
  Escrow Amount: ₹74,970
  Recipients:
    - Green Valley Farm: ₹22,727 (30.3%)
    - Sunrise Organic Farm: ₹27,273 (36.4%)
    - Golden Harvest Farm: ₹24,970 (33.3%)

============================================================
✅ Sample Data Created Successfully!
============================================================
```

### 3. Start Django Server
```bash
python manage.py runserver
```

Server runs at: **http://127.0.0.1:8000/**

---

## 🎬 Demo Flow (5 minutes)

### **Scene 1: Show the Problem** (30 seconds)
**Narrator says:**
> "Small Indian farmers produce 500kg/day, but factories need 10 tonnes/day. They can't sign contracts with 20 different farmers. Plus, factories worry about non-payment, farmers worry about getting paid."

**Show these API responses:**

#### Get All Farmers
```bash
curl http://127.0.0.1:8000/api/farmers/
```

**Highlight:**
- 3 farmers: Green Valley (500kg), Sunrise (600kg), Golden Harvest (550kg)
- All "verified"
- Individual wallet addresses

---

### **Scene 2: Show Automatic Aggregation** (1 minute)
**Narrator says:**
> "Our platform automatically bundles products from multiple small farmers into one pool that meets buyer requirements."

#### Get Aggregated Pool
```bash
curl http://127.0.0.1:8000/api/products/aggregated-pools/
```

**Point out:**
```json
{
  "product_name": "Tomatoes Bundle",
  "total_available_kg": 1650,      // 500+600+550 from 3 farms
  "source_products": [1, 2, 3],    // All 3 farmers
  "average_price_per_kg": 49,
  "status": "open"
}
```

---

### **Scene 3: Buyer Creates Order** (30 seconds)
**Narrator says:**
> "Buyer (Nestle) needs 1500kg. Instead of signing 3 contracts, they place one order from the pool."

#### Get Buyer
```bash
curl http://127.0.0.1:8000/api/buyers/
```

**Show:**
- Nestle India Ltd
- Located in Mumbai
- Verified buyer

#### Get Order
```bash
curl http://127.0.0.1:8000/api/orders/
```

**Point out:**
```json
{
  "buyer": "Nestle India Ltd",
  "quantity_kg": 1500,
  "order_amount": 73500,           // 1500kg × ₹49
  "platform_fee": 1470,            // 2% fee
  "total_amount": 74970,
  "status": "pending_payment"
}
```

---

### **Scene 4: Smart Contract Creates Escrow** (1 minute)
**Narrator says:**
> "Here's the magic: Smart contract locks funds on blockchain. Funds are automatically split and released to all 3 farmers only after delivery confirmation. **No trust needed.**"

#### Get Smart Contract
```bash
curl http://127.0.0.1:8000/api/smartcontracts/
```

**Highlight the recipient distribution:**
```json
{
  "contract_type": "escrow",
  "status": "active",
  "escrow_amount": 74970,
  "recipient_data": {
    "farmers": [
      {
        "name": "Green Valley Farm",
        "wallet": "0x1234567890...",
        "amount": 22727,        // 30.3% of total
        "percentage": 30.3
      },
      {
        "name": "Sunrise Organic Farm",
        "wallet": "0x2234567890...",
        "amount": 27273,        // 36.4% of total
        "percentage": 36.4
      },
      {
        "name": "Golden Harvest Farm",
        "wallet": "0x3234567890...",
        "amount": 24970,        // 33.3% of total
        "percentage": 33.3
      }
    ]
  }
}
```

---

## 📊 Comparison: The Solution Explained

### Before FarmLink ❌
```
FACTORY: Signs 20 separate contracts
FARMERS: 20 different negotiations
TIME: 2-4 weeks with Letter of Credit
COST: 1.5-3% fee for each contract
TRUST: High risk on both sides
```

### With FarmLink ✅
```
FACTORY: 1 order from 1 aggregated pool
FARMERS: 1 smart contract to 20 farmers
TIME: Instant blockchain settlement
COST: 2% platform fee (better than LoC)
TRUST: Smart contract enforces delivery
```

---

## 🎯 Key Metrics to Mention

During demo, emphasize:

1. **Scale Aggregation**: 3 small farms → Meeting bulk requirement
   - Farm 1: 500kg
   - Farm 2: 600kg
   - Farm 3: 550kg
   - **Total: 1650kg** ✓ (Factory needs 1500kg)

2. **Cost Savings**: 2% vs 1.5-3%
   - Order value: ₹73,500
   - Platform fee: ₹1,470 (2%)
   - Farmer payment: ₹72,030

3. **Payment Distribution**: Automatic & Proportional
   - Green Valley: ₹22,727 (30.3%)
   - Sunrise Farm: ₹27,273 (36.4%)
   - Golden Harvest: ₹24,970 (33.3%)

4. **Time to Settlement**: Instant
   - Traditional: 2-4 weeks
   - FarmLink: On-chain in minutes

---

## 🔗 Complete API Endpoints

```
GET  /api/farmers/                    - List all farmers
GET  /api/farmers/{id}/               - Farmer details
POST /api/farmers/                    - Register farmer

GET  /api/buyers/                     - List all buyers
GET  /api/buyers/{id}/                - Buyer details
POST /api/buyers/                     - Register buyer

GET  /api/products/farm-products/     - All products
POST /api/products/farm-products/     - Add product

GET  /api/products/aggregated-pools/  - All pools
POST /api/products/aggregated-pools/  - Create pool

GET  /api/orders/                     - All orders
POST /api/orders/                     - Create order
GET  /api/orders/{id}/                - Order details

GET  /api/smartcontracts/             - All contracts
GET  /api/smartcontracts/{id}/        - Contract details
POST /api/smartcontracts/{id}/release-payment/
```

---

## 📱 Alternative: REST Client Tests

If using Postman or VS Code REST Client, use:

**File: `demo.http`**
```http
### Get all farmers
GET http://127.0.0.1:8000/api/farmers/
Accept: application/json

### Get aggregated pool
GET http://127.0.0.1:8000/api/products/aggregated-pools/
Accept: application/json

### Get order
GET http://127.0.0.1:8000/api/orders/
Accept: application/json

### Get smart contract
GET http://127.0.0.1:8000/api/smartcontracts/
Accept: application/json
```

---

## ✅ Demo Checklist

- [ ] Run migrations
- [ ] Load sample data
- [ ] Start dev server
- [ ] Test `/api/farmers/` endpoint
- [ ] Test `/api/products/aggregated-pools/` endpoint
- [ ] Test `/api/orders/` endpoint
- [ ] Test `/api/smartcontracts/` endpoint
- [ ] Show the complete end-to-end flow

---

## 🎤 Demo Script (Full 5-minute version)

**[Begin with title slide]**

"**FarmLink: Solving the Scale Mismatch Problem Using Smart Contracts**"

**Problem (30 sec):**
> "There's a fundamental mismatch in agriculture. Small Indian farmers can produce 500 kilos per day. But factories needing bulk supplies require 10 tonnes per day. Making farmers sign individual contracts is expensive and slow.
>
> Plus, there's trust issues: Factories worry farmers won't deliver. Farmers worry about non-payment.
>
> Traditional solutions like Letters of Credit take 2-4 weeks and cost 1.5-3% of the shipment value."

**Solution Overview (1 min):**
> "FarmLink uses three key technologies:
> 1. **Automatic Aggregation**: Platform bundles products from multiple farmers
> 2. **Smart Contracts**: Escrow system locks funds on blockchain
> 3. **Transparent Distribution**: Automatic payment to each farmer based on their contribution"

**Demo (3 min):**
> [Show each API endpoint with responses]
> "As you can see, here we have three small farmers: Green Valley, Sunrise Organic, and Golden Harvest. Each produces 500-600 kilos per day.
>
> Our platform automatically creates an aggregated pool combining all three, giving us 1650 kilos to work with.
>
> When Nestle places a 1500kg order, instead of signing 3 contracts, they place one order. The smart contract kicks in, locking ₹74,970 in escrow.
>
> **Here's the key part:** The contract automatically distributes payments to all farmers based on their contribution—no manual work, no delays, no trust issues.
>
> Green Valley gets ₹22,727, Sunrise gets ₹27,273, and Golden Harvest gets ₹24,970. All in their provided wallets."

**Impact (30 sec):**
> "This solves the scale mismatch problem. Factories can source bulk supply from a coordinated network of small farmers. Farmers get instant payment through blockchain. And the 2% platform fee is better than traditional banking methods.
>
> The result: More profits for farmers, reliable supply for factories, and faster, cheaper transactions for everyone."

**Thank you**

---

## 🚨 Troubleshooting

### Issue: "Farmer.DoesNotExist"
```bash
# Reset and reload data
python manage.py flush
python sample_data.py
```

### Issue: "No sample data created"
Check that all models exist:
```bash
python manage.py check
```

### Issue: Port 8000 already in use
```bash
python manage.py runserver 8001
```

---

## 📚 Documentation References

- **BASIC_WORKFLOW.md** - Core workflow explanation
- **ARCHITECTURE.md** - Technical architecture
- **API_DOCUMENTATION.md** - Complete API reference
