# FarmLink - Quick Start Guide

## ⚡ 5-Minute Setup

### For macOS/Linux:

```bash
# 1. Clone/Navigate to project
cd /Users/tapdiyaom/Desktop/Farmlink2

# 2. Run setup script
bash setup.sh

# 3. Activate environment
source venv/bin/activate

# 4. Load sample data (optional)
python manage.py shell < sample_data.py

# 5. Run server
python manage.py runserver

# 6. Open browser
# Admin: http://localhost:8000/admin/
# API: http://localhost:8000/api/
```

### For Windows:

```bash
# 1. Navigate to project
cd Farmlink2

# 2. Run setup script
setup.bat

# 3. Activate environment
venv\Scripts\activate.bat

# 4. Load sample data (optional)
python manage.py shell < sample_data.py

# 5. Run server
python manage.py runserver

# 6. Open browser
# Admin: http://localhost:8000/admin/
# API: http://localhost:8000/api/
```

---

## 🏃 First Run Checklist

- [ ] Python 3.9+ installed
- [ ] Create `.env` file (use `.env.example` as template)
- [ ] Run `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] (Optional) Load sample data: `python manage.py shell < sample_data.py`
- [ ] Start server: `python manage.py runserver`

---

## 📚 Key Endpoints to Test

### 1. Admin Panel (Create Data)
```
http://localhost:8000/admin/
- Login with superuser credentials
- Create Farmers, Buyers, Products
```

### 2. List Farmers
```bash
curl http://localhost:8000/api/farmers/
```

### 3. List Buyers
```bash
curl http://localhost:8000/api/buyers/
```

### 4. List Product Pools
```bash
curl http://localhost:8000/api/products/pools/
```

### 5. Get Bearer Token
```bash
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

---

## 🎯 Complete Demo Flow (10 minutes)

### Step 1: Create Test Data (Admin Panel)
1. Go to http://localhost:8000/admin/
2. Create 2-3 Farmers with products
3. Create 1-2 Buyers

### Step 2: Create Aggregated Pool
```bash
curl -X POST http://localhost:8000/api/products/pools/create_aggregation/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Rice",
    "target_quantity_kg": 10000
  }'
```

### Step 3: Create Order
```bash
curl -X POST http://localhost:8000/api/orders/create_order/ \
  -H "Authorization: Token BUYER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pool_id": 1,
    "quantity_kg": 5000,
    "shipping_address": "123 Main Street"
  }'
```

### Step 4: Initiate Payment
```bash
curl -X POST http://localhost:8000/api/orders/1/initiate_payment/ \
  -H "Authorization: Token BUYER_TOKEN"
```

### Step 5: Mark Shipped
```bash
curl -X POST http://localhost:8000/api/orders/1/mark_shipped/ \
  -H "Authorization: Token FARMER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tracking_number": "TRACK-123"}'
```

### Step 6: Confirm Delivery (Releases Smart Contract)
```bash
curl -X POST http://localhost:8000/api/orders/1/confirm_delivery/ \
  -H "Authorization: Token BUYER_TOKEN"
```

### Step 7: Check Smart Contract Status
```bash
curl http://localhost:8000/api/smartcontracts/contracts/1/status/ \
  -H "Authorization: Token TOKEN"
```

---

## 🐳 Docker Setup (Alternative)

```bash
# Build and run with Docker Compose
docker-compose up

# In another terminal
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell < sample_data.py

# Access at http://localhost:8000
```

---

## 📁 Project Structure

```
Farmlink2/
├── farmers/              # Farmer management
│   ├── models.py        # Farmer & FarmProduct
│   ├── views.py         # API endpoints
│   └── serializers.py    # REST serializers
├── buyers/              # Buyer management
├── products/            # Product aggregation engine
├── orders/              # Order processing
├── smartcontracts/      # Blockchain integration
│   └── blockchain_service.py  # AWS AMB service
├── settings.py          # Django settings
├── manage.py            # Django CLI
├── requirements.txt     # Python dependencies
├── README.md            # Full documentation
└── API_DOCUMENTATION.md # Complete API reference
```

---

## 🔑 Test Credentials (After Sample Data Load)

| Role | Username | Password |
|------|----------|----------|
| Farmer | farmer_1 | password123 |
| Buyer | buyer_1 | password123 |
| Admin | admin | (from setup) |

---

## ⚙️ Environment Configuration

Edit `.env` file:

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key

# Database (use default SQLite for development)
DATABASE_URL=sqlite:///db.sqlite3

# AWS (for blockchain integration)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_REGION=us-east-1

# Blockchain
BLOCKCHAIN_NETWORK=AWS_MANAGED_BLOCKCHAIN
WEB3_PROVIDER=http://localhost:8545
```

---

## 🆘 Troubleshooting

### "Migrate is not found"
```bash
python manage.py migrate --run-syncdb
```

### "Port 8000 already in use"
```bash
python manage.py runserver 0.0.0.0:8001
```

### "ModuleNotFoundError: No module named 'django'"
```bash
pip install -r requirements.txt
```

### "Database error"
```bash
rm db.sqlite3
python manage.py migrate
```

---

## 📚 Learn More

- **Full Documentation**: [README.md](README.md)
- **API Reference**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Hackathon Checklist**: [HACKATHON_CHECKLIST.md](HACKATHON_CHECKLIST.md)

---

## 🚀 Ready to Check Out?

```bash
# Test Django is working
python manage.py check

# Run tests
python manage.py test

# Create fresh database
python manage.py flush

# Generate migrations
python manage.py makemigrations
```

---

## 💡 Key Concepts

**Smart Contract Escrow**: Payment locked until delivery confirmed
**Product Aggregation**: 5-20 small farms bundled for bulk orders
**Multi-Farmer Settlement**: Automatic payment distribution to all participating farmers
**AWS Managed Blockchain**: Enterprise-grade chain for trust & transparency

---

**You're ready! Open http://localhost:8000/admin to start exploring! 🌾**
