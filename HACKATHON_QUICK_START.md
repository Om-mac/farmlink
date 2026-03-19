# 🌾 FarmLink Hackathon - Quick Start Guide

## Start Here! ⚡ 5-Minute Setup

### Step 1: Database & Data (3 minutes)
```bash
# Run migrations
python manage.py migrate

# Load demo data
python sample_data.py
```

### Step 2: Start Server (1 minute)
```bash
python manage.py runserver
```

Server: **http://127.0.0.1:8000/**

### Step 3: View the Demo (1 minute)
Open these URLs in your browser:

| Endpoint | What It Shows |
|----------|---------------|
| [/api/farmers/](http://127.0.0.1:8000/api/farmers/) | 3 small farmers with their daily capacity |
| [/api/buyers/](http://127.0.0.1:8000/api/buyers/) | 1 buyer (Nestle) looking for bulk supply |
| [/api/products/aggregated-pools/](http://127.0.0.1:8000/api/products/aggregated-pools/) | **System automatically bundles all 3 farmers** |
| [/api/orders/](http://127.0.0.1:8000/api/orders/) | Buyer's order from the pool |
| [/api/smartcontracts/](http://127.0.0.1:8000/api/smartcontracts/) | **Smart contract escrow with auto-payment distribution** |

---

## 🎯 The 30-Second Pitch

> "With FarmLink, 3 small farmers producing 500kg each can meet factory demand of 1500kg through automatic aggregation. A smart contract locks payment on blockchain and distributes it automatically to all farmers. No intermediaries. No delays. Instant blockchain settlement."

**Why it matters:**
- ✅ Solves scale mismatch (3 × 500kg farms = 1500kg)
- ✅ Instant payment (blockchain, no 2-4 week wait)
- ✅ Cost savings (2% fee vs 1.5-3% Letter of Credit)
- ✅ No trust needed (smart contract enforces delivery)

---

## 📊 What the Demo Shows

### Farmers (Individual Capacity)
```
Green Valley Farm:    500 kg/day → Grows Tomatoes
Sunrise Organic:      600 kg/day → Grows Tomatoes  
Golden Harvest:       550 kg/day → Grows Tomatoes
                    ________________
TOTAL:              1650 kg/day (meets 1500kg demand!)
```

### Aggregated Pool (Automatic System)
**FarmLink's Magic:** All 3 farmers' products combined into 1 pool ✨

### Order (Single Contract)
```
Buyer:    Nestle (Mumbai)
Quantity: 1500 kg
Amount:   ₹73,500 + ₹1,470 fee = ₹74,970 total
```

### Smart Contract (Auto Distribution)
```
Escrow locks: ₹74,970

Auto-pays to farmers:
├─ Green Valley:   ₹22,727 (30.3%)
├─ Sunrise Org:    ₹27,273 (36.4%)
└─ Golden Harvest: ₹24,970 (33.3%)

Status: Funds released on delivery confirmation (no manual work!)
```

---

## 🎬 Full Demo Script (5 minutes)

### 1. Show the Problem (1 min)
"Factories need 10 tonnes of tomatoes. But individual farms only produce 500kg. We need 20 separate contracts—expensive and slow."

**Show:** [/api/farmers/](http://127.0.0.1:8000/api/farmers/) - Point out each farm's small capacity

### 2. Show the Solution (2 min)
"FarmLink automatically bundles products and uses smart contracts for instant payment."

**Show:** 
- [/api/products/aggregated-pools/](http://127.0.0.1:8000/api/products/aggregated-pools/) - "System combined all 3 farms into 1 pool"
- [/api/buyers/](http://127.0.0.1:8000/api/buyers/) - "Single buyer places one order"
- [/api/orders/](http://127.0.0.1:8000/api/orders/) - "Order from pool instead of 3 separate contracts"

### 3. Show the Payment Magic (1.5 min)
"Here's where blockchain helps:"

**Show:** [/api/smartcontracts/](http://127.0.0.1:8000/api/smartcontracts/)

"₹74,970 is locked in a smart contract. It automatically splits and pays all 3 farmers based on their contribution. No waiting, no trust issues—the contract enforces delivery before paying."

### 4. Business Impact (0.5 min)
"Traditional letter of credit: 2-4 weeks, 1.5-3% cost
FarmLink: Instant payment, 2% cost
Result: Farmers profit more, factories get reliable supply faster"

---

## 🔧 Customizing the Demo

### Change the Farmer Capacities
Edit `sample_data.py` line ~40:
```python
'daily_production_kg': 500,  # Change this
```

### Change Product Type
Edit line ~115:
```python
'product_name': 'Tomatoes',  # Change to rice, wheat, etc.
```

### Change Buyer
Edit line ~130:
```python
'company_name': 'Nestle India Ltd',  # Change to any buyer
```

### Change Prices
Edit line ~117:
```python
'price_per_kg': 50,  # Change the price
```

Then reload:
```bash
python manage.py flush
python sample_data.py
```

---

## 📱 API Testing (curl commands)

```bash
# List farmers
curl -s http://127.0.0.1:8000/api/farmers/ | python -m json.tool

# List buyers
curl -s http://127.0.0.1:8000/api/buyers/ | python -m json.tool

# List pools (aggregation)
curl -s http://127.0.0.1:8000/api/products/aggregated-pools/ | python -m json.tool

# List orders
curl -s http://127.0.0.1:8000/api/orders/ | python -m json.tool

# List smart contracts
curl -s http://127.0.0.1:8000/api/smartcontracts/ | python -m json.tool
```

---

## 🎓 Understanding the Architecture

```
┌─────────────────────┐
│   3 Small Farms     │
│ (500kg each)        │
└──────────┬──────────┘
           │
           ▼
    ┌────────────────┐
    │ FarmLink       │
    │ Aggregation    │
    │ Engine         │
    └────────┬───────┘
             │
             ▼ (Combines 3→1)
    ┌────────────────┐
    │ Product Pool   │
    │ (1650kg total) │
    └────────┬───────┘
             │
             ▼
    ┌────────────────┐
    │ Buyer Order    │
    │ (1500kg)       │
    └────────┬───────┘
             │
             ▼
    ┌────────────────┐
    │ Smart Contract │
    │ Escrow         │
    │ (Locks Funds)  │
    └────────┬───────┘
             │
             ▼ (Auto-pays after delivery)
    ┌────────────────┐
    │ 3 Farmers Get  │
    │ Paid           │
    │ (Proportional) │
    └────────────────┘
```

---

## ✅ Demo Checklist

Before your presentation:

- [ ] `python manage.py migrate` - Database ready
- [ ] `python sample_data.py` - Sample data loaded
- [ ] `python manage.py runserver` - Server running
- [ ] Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) - Root API works
- [ ] Test each endpoint in the table above
- [ ] Prepare your 30-second pitch
- [ ] Practice the 5-minute demo script
- [ ] Have fallback screenshots if internet is slow

---

## 🚀 Key Talking Points

### Problem Solved: Scale Mismatch
"Small farmers can't meet bulk buyer requirements. FarmLink automates aggregation."

### Technology Used: Smart Contracts
"Blockchain ensures trust—funds locked until delivery confirmed. No intermediaries."

### Business Model: 2% Fee
"Better than traditional 1.5-3% Letter of Credit. Farmers keep more profit."

### Time to Market: Real-time
"Blockchain settlement is instant. No 2-4 week waiting period."

---

## 📚 Documentation

- **DEMO_GUIDE.md** - Full demo script with every detail
- **BASIC_WORKFLOW.md** - 5-step workflow explanation
- **ARCHITECTURE.md** - Technical details
- **README.md** - Complete project overview

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| `Farmer.DoesNotExist` | Run `python manage.py flush` then `python sample_data.py` |
| Port 8000 taken | Try `python manage.py runserver 8001` |
| Import error | Check `pip install -r requirements.txt` |
| Database error | Run `python manage.py migrate` again |

---

## 🎉 Good Luck!

You now have a complete FarmLink prototype demonstrating:
1. ✅ Problem identification  
2. ✅ Automatic aggregation solution
3. ✅ Smart contract integration
4. ✅ Transparent payment distribution

**This is everything you need for a winning hackathon pitch!**

Questions? Check **DEMO_GUIDE.md** for detailed explanations.
