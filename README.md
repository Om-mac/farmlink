# FarmLink - Farm Aggregation Platform with Smart Contract Escrow

A Django-based web application that solves the "Scale Mismatch Kills Small Farmers" problem using smart contracts and blockchain technology.

## 🎯 Problem Solved

**Scale Mismatch Problem:**
- Factories need 10 tonnes/day but small farmers produce only 500kg
- Factory can't sign 20 separate contracts with 20 different farmers
- Trust issues: Factory worries farmer won't deliver; Farmer worries about non-payment
- Traditional Letters of Credit take weeks and cost 1.5-3% of shipment value

**Our Solution:**
- **Smart Contract Escrow**: Funds locked on blockchain, released only after delivery confirmation
- **Automatic Aggregation**: Platform matches multiple farmers to fulfill bulk orders
- **Transparent Payments**: Direct blockchain settlements to farmers
- **No Intermediaries**: Reduced costs and faster processing

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FarmLink Platform                         │
├──────────────────┬──────────────────┬──────────────────────┤
│   Farmer Mgmt    │   Buyer Portal   │  Aggregation Engine  │
├──────────────────┴──────────────────┴──────────────────────┤
│                   Django REST API                           │
├──────────────────────────────────────────────────────────────┤
│         Order Management & Product Matching                 │
├──────────────────────────────────────────────────────────────┤
│    Smart Contract Service (AWS Managed Blockchain)          │
├──────────────────────────────────────────────────────────────┤
│         Payment Escrow & Settlement                         │
└──────────────────────────────────────────────────────────────┘
```

## 📋 Features

### 1. **Farmer Management**
- Profile creation and product listing
- Capacity management (daily/max production)
- Certification tracking (Organic, Fair Trade, etc.)
- Wallet address for blockchain payments
- Performance metrics (rating, on-time delivery rate)

### 2. **Buyer Portal**
- Company profile registration
- Search and filter aggregated products
- Order creation and management
- Payment confirmation via smart contracts
- Dispute resolution

### 3. **Product Aggregation Engine**
- Automatic matching of similar products from multiple farmers
- Capacity calculations to meet buyer requirements
- Quality assurance tracking
- Transparent pricing with platform fees (2%)

### 4. **Smart Contract Escrow System**
- AWS Managed Blockchain integration
- Automatic fund locking on order creation
- Conditional release after delivery confirmation
- Dispute handling
- Event logging and auditing

### 5. **Payment Processing**
- Multi-farmer settlement in single transaction
- Proportional fund distribution
- Transaction tracking and confirmation
- Refund handling for disputed orders

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Django 4.2+
- PostgreSQL (optional, uses SQLite by default)
- AWS Account (for Managed Blockchain)
- Virtual Environment

### Installation

1. **Clone and setup**
```bash
cd Farmlink2
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your AWS credentials and settings
```

3. **Run migrations**
```bash
python manage.py migrate
```

4. **Create superuser**
```bash
python manage.py createsuperuser
```

5. **Start development server**
```bash
python manage.py runserver
```

Access at: `http://localhost:8000`
Admin panel: `http://localhost:8000/admin/`

## 📚 API Endpoints

### Authentication
- `POST /api/token/` - Get auth token
- `POST /api/token/refresh/` - Refresh token

### Farmers
- `GET /api/farmers/` - List all farmers
- `POST /api/farmers/` - Register new farmer
- `GET /api/farmers/{id}/` - Get farmer details
- `GET /api/farmers/me/` - Get current farmer profile
- `GET /api/farmers/verified/` - List verified farmers
- `GET /api/farmers/search_by_product/` - Search by product type

### Buyers
- `GET /api/buyers/` - List buyers
- `POST /api/buyers/` - Register new buyer
- `GET /api/buyers/{id}/` - Get buyer details
- `GET /api/buyers/me/` - Get current buyer profile

### Products (Aggregation)
- `GET /api/products/pools/` - List aggregated pools
- `POST /api/products/pools/create_aggregation/` - Create pool (admin)
- `GET /api/products/pools/{id}/` - Get pool details
- `GET /api/products/pools/{id}/participating_farmers/` - List farmers in pool
- `GET /api/products/pools/search_by_quantity/` - Find pools by capacity

### Orders
- `POST /api/orders/create_order/` - Create new order
- `GET /api/orders/` - List buyer's orders
- `POST /api/orders/{id}/initiate_payment/` - Lock funds in escrow
- `POST /api/orders/{id}/mark_shipped/` - Mark order as shipped
- `POST /api/orders/{id}/confirm_delivery/` - Release funds
- `POST /api/orders/{id}/raise_dispute/` - Raise dispute

### Smart Contracts
- `POST /api/smartcontracts/contracts/create_escrow/` - Create escrow contract
- `POST /api/smartcontracts/contracts/{id}/activate/` - Activate contract
- `POST /api/smartcontracts/contracts/{id}/release_funds/` - Release escrow
- `POST /api/smartcontracts/contracts/{id}/file_dispute/` - File dispute
- `GET /api/smartcontracts/contracts/{id}/status/` - Get contract status

## 🔐 Smart Contract Flow

```
1. Buyer Creates Order
   ↓
2. Order Validation & Escrow Creation
   ↓
3. Smart Contract Deployed (escrow_amount locked)
   ↓
4. Buyer Confirms Payment → Escrow Activated
   ↓
5. Farmers Ship Products
   ↓
6. Buyer Confirms Delivery
   ↓
7. Smart Contract Releases Funds to Farmers
   ↓
8. Platform Fee Transferred
```

## 🏦 AWS Managed Blockchain Integration

### Setup Steps

1. **Create AWS Managed Blockchain Network**
```bash
aws managedblockchain create-network \
  --framework HYPERLEDGER_FABRIC \
  --framework-version 2.2 \
  --network-fabric-attributes Edition=STANDARD
```

2. **Configure in Django Admin**
- Go to Smart Contracts → AWS Managed Blockchain Configs
- Add your network details:
  - Network ID
  - Member ID
  - RPC Endpoint
  - AWS Credentials
  - Region

3. **Deploy Smart Contract**
- Platform provides Solidity contract
- Deploy to configured network
- Update contract address in config

## 🤝 Data Models

### Key Relationships
```
User (Django Auth)
├── Farmer Profile
│   ├── FarmProducts (multiple)
│   └── AggregatedProductPool (many-to-many)
├── Buyer Profile
│   └── Orders (multiple)
│
Order
├── AggregatedProductPool
├── SmartContract (Escrow)
├── OrderDispute (optional)
└── PaymentTransactions (multiple)

SmartContract
├── ContractEvents (multiple)
└── AWSManagedBlockchainConfig
```

## 📊 How It Solves Scale Mismatch

**Before (Traditional Method):**
- Risk: Farmer ships first → gets non-payment (80% loss)
- OR Risk: Buyer pays first → non-delivery (100% loss)
- OR Cost: Letter of Credit (1.5-3% f shipment)
- TIME: 2-4 weeks processing

**With FarmLink Smart Contracts:**
- ✅ Farmer: Protected by escrow (funds locked, released only to verified wallet)
- ✅ Buyer: Protected by delivery confirmation requirement
- ✅ Cost: 2% platform fee (vs 1.5-3% LOC)
- ✅ TIME: Real-time settlement (minutes, not weeks)
- ✅ Aggregation: Combines 5-20 small farmers into single order

## 💾 Database Schema Highlights

### Aggregated Product Pool
Solves scale mismatch by bundling:
- Multiple FarmProducts from different farmers
- Aggregated capacity meets buyer requirements
- Single smart contract for entire pool

### Smart Contract Model
Ensures trust and transparency:
- `contract_address`: Immutable blockchain address
- `status`: deployed → active → completed
- `escrow_amount`: Locked funds
- `seller_wallets`: Multiple farmer recipients
- `delivery_deadline`: Automatic dispute period

### Order Model
Links everything together:
- `smart_contract_id`: Blockchain escrow reference
- Status progression: pending → escrow_locked → shipped → delivered → completed
- `payment_transactions`: Immutable blockchain records

## 🔄 Workflow Examples

### Example 1: Factory needs 5 tonnes
```
1. Factory searches for rice
2. Platform aggregates 10 farmers × 500kg each
3. Factory creates order for 5 tonnes
4. Smart contract locks payment (5T × price)
5. Farmers ship their portions
6. Factory confirms delivery
7. Funds automatically distributed to 10 farmers
```

### Example 2: Dispute Handling
```
1. If delivery incomplete: Buyer raises dispute
2. System pauses fund release
3. Platform admin investigates
4. If fraud detected: Refund to buyer
5. If false claim: Release to farmer
6. Both parties notified via smart contract event
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test farmers.tests

# With coverage
coverage run --source='.' manage.py test
coverage report
```

## 📦 Deployment

### Docker
```bash
docker build -t farmlink .
docker run -p 8000:8000 farmlink
```

### Production Checklist
- [ ] Set `DEBUG=False` in settings
- [ ] Configure proper database (PostgreSQL)
- [ ] Set up SSL/HTTPS
- [ ] Configure AWS credentials securely
- [ ] Set up Celery for async tasks
- [ ] Configure logging and monitoring
- [ ] Run migrations on prod DB
- [ ] Collect static files: `python manage.py collectstatic`

## 🎓 Hackathon Notes

This prototype demonstrates:
- ✅ Complete Django architecture for farm-to-buyer marketplace
- ✅ Automatic product aggregation engine
- ✅ Smart contract integration (AWS Managed Blockchain ready)
- ✅ Escrow payment system
- ✅ Multi-farmer settlement
- ✅ Dispute resolution framework
- ✅ RESTful API for all operations

**For Production:**
- Add real blockchain integration (solidity contracts)
- Implement payment gateway integration
- Add email notifications
- Build frontend (React/Vue)
- Add comprehensive testing
- Implement rate limiting and security
- Add KYC/AML verification

## 📞 Support

For questions about the platform architecture, smart contracts, or aggregation engine, refer to:
- Django REST Framework docs: https://www.django-rest-framework.org/
- AWS Managed Blockchain: https://docs.aws.amazon.com/managed-blockchain/
- Web3.py for blockchain: https://web3py.readthedocs.io/

## 📄 License

MIT License - See LICENSE file

---

**Built for Hackers | Solving Real Farmer Problems | Powered by Blockchain**
# farmlink
# farmlink
