# FarmLink API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Authentication

All endpoints (except public list views) require authentication via Token:

```
Header: Authorization: Token <your-token>
```

### Get Token
```bash
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
```

---

## Farmer Endpoints

### 1. Register New Farmer
```
POST /farmers/
Content-Type: application/json
Authorization: Token <token>

{
  "farm_name": "Green Valley Farm",
  "location": "Punjab, India",
  "country": "India",
  "phone": "+91-9876543210",
  "farm_size_hectares": 5.5,
  "certification": "organic",
  "years_in_business": 10,
  "daily_production_kg": 500,
  "max_order_size_kg": 2000,
  "min_order_size_kg": 250,
  "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f42904"
}
```

### 2. List All Farmers
```
GET /farmers/
GET /farmers/?country=India
GET /farmers/?search=Green
GET /farmers/?ordering=-rating

Response:
{
  "count": 42,
  "next": "http://localhost:8000/api/farmers/?page=2",
  "results": [
    {
      "id": 1,
      "farm_name": "Green Valley Farm",
      "location": "Punjab",
      "country": "India",
      "rating": 4.8,
      "verified": true,
      "daily_production_kg": 500,
      "available_products": [...]
    }
  ]
}
```

### 3. Get Farmer Details
```
GET /farmers/{id}/

Response:
{
  "id": 1,
  "farm_name": "Green Valley Farm",
  "location": "Punjab, India",
  "country": "India",
  "phone": "+91-9876543210",
  "farm_size_hectares": 5.5,
  "certification": "organic",
  "years_in_business": 10,
  "daily_production_kg": 500,
  "max_order_size_kg": 2000,
  "rating": 4.8,
  "total_orders": 45,
  "on_time_delivery_rate": 98.5,
  "verified": true,
  "available_products": [
    {
      "id": 1,
      "product_name": "Basmati Rice",
      "daily_capacity_kg": 500,
      "quality_grade": "A",
      "price_per_kg": 45.50
    }
  ]
}
```

### 4. Get Current Farmer Profile
```
GET /farmers/me/
Authorization: Token <farmer-token>
```

### 5. List Verified Farmers Only
```
GET /farmers/verified/
```

### 6. Search Farmers by Product
```
GET /farmers/search_by_product/?product=Rice

Response: Array of farmers producing rice
```

### 7. Add Farm Product
```
POST /farmers/products/
Authorization: Token <token>

{
  "farmer": 1,
  "product_name": "Basmati Rice",
  "daily_capacity_kg": 500,
  "year_round_available": true,
  "quality_grade": "A",
  "price_per_kg": 45.50
}
```

---

## Buyer Endpoints

### 1. Register New Buyer
```
POST /buyers/
Content-Type: application/json
Authorization: Token <token>

{
  "company_name": "Global Foods Ltd",
  "buyer_type": "factory",
  "location": "Dubai, UAE",
  "country": "UAE",
  "phone": "+971-4-123-4567",
  "avg_monthly_orders": 12,
  "payment_method": "escrow",
  "wallet_address": "0x8ba1f109551bD432803012645Ac136ddd64DBA72"
}
```

### 2. List Buyers
```
GET /buyers/
GET /buyers/?buyer_type=factory
GET /buyers/?country=UAE
```

### 3. Get Current Buyer Profile
```
GET /buyers/me/
Authorization: Token <buyer-token>
```

### 4. Get Buyer Details
```
GET /buyers/{id}/

Response:
{
  "id": 1,
  "company_name": "Global Foods Ltd",
  "buyer_type": "factory",
  "location": "Dubai, UAE",
  "country": "UAE",
  "rating": 4.9,
  "total_purchases": 156,
  "successful_deliveries": 154,
  "payment_success_rate": 98.7,
  "verified": true
}
```

---

## Product Aggregation Endpoints

### 1. List All Aggregated Pools
```
GET /products/pools/
GET /products/pools/?status=open
GET /products/pools/?search=rice

Response:
{
  "count": 15,
  "results": [
    {
      "id": 1,
      "product_name": "Basmati Rice",
      "total_available_kg": 5000,
      "target_quantity_kg": 10000,
      "average_price_per_kg": 45.50,
      "status": "open",
      "participating_farmers_count": 10,
      "total_pool_value": 227500
    }
  ]
}
```

### 2. Create Aggregated Pool (Admin)
```
POST /products/pools/create_aggregation/
Authorization: Token <admin-token>
Content-Type: application/json

{
  "product_name": "Basmati Rice",
  "target_quantity_kg": 10000
}

Response:
{
  "id": 1,
  "product_name": "Basmati Rice",
  "source_products": [
    {
      "id": 1,
      "product_name": "Basmati Rice",
      "daily_capacity_kg": 500,
      "farmer": 1
    }
  ],
  "total_available_kg": 5000,
  "target_quantity_kg": 10000,
  "average_price_per_kg": 45.50,
  "status": "open",
  "participating_farmers_count": 10
}
```

### 3. Get Pool Details
```
GET /products/pools/{id}/

Shows all participating farmers, quality assurance status, availability
```

### 4. Get Participating Farmers
```
GET /products/pools/{id}/participating_farmers/

Response: Array of farmer profiles in this pool
```

### 5. Search Pools by Quantity
```
GET /products/pools/search_by_quantity/?quantity_kg=5000

Returns only pools with at least 5000kg available
```

---

## Order Endpoints

### 1. Create New Order
```
POST /orders/create_order/
Authorization: Token <buyer-token>
Content-Type: application/json

{
  "pool_id": 1,
  "quantity_kg": 5000,
  "shipping_address": "123 Factory Street, Dubai, UAE"
}

Response:
{
  "id": 1,
  "buyer": 1,
  "buyer_company": "Global Foods Ltd",
  "aggregated_pool": 1,
  "pool_info": {
    "product_name": "Basmati Rice",
    "available_kg": 5000
  },
  "quantity_kg": 5000,
  "unit_price": 45.50,
  "product_cost": 227500,
  "platform_fee": 4550,
  "total_amount": 232050,
  "status": "pending",
  "expected_delivery_date": "2026-03-25"
}
```

### 2. List My Orders
```
GET /orders/
Authorization: Token <buyer-token>

Returns only orders for current buyer
```

### 3. Get Order Details
```
GET /orders/{id}/
Authorization: Token <token>

Response:
{
  "id": 1,
  "buyer": 1,
  "aggregated_pool": 1,
  "quantity_kg": 5000,
  "status": "pending",
  "smart_contract_id": "0x_demo_1",
  "payment_transactions": [
    {
      "id": 1,
      "payment_type": "order_payment",
      "amount": 232050,
      "transaction_hash": "0x...",
      "status": "confirmed"
    }
  ],
  "dispute": null,
  "created_at": "2026-03-20T10:30:00Z"
}
```

### 4. Initiate Payment (Lock Escrow)
```
POST /orders/{id}/initiate_payment/
Authorization: Token <buyer-token>

Response:
{
  "status": "payment initiated",
  "smart_contract_id": "0x_demo_1",
  "amount_locked": "232050",
  "order_id": 1
}

Note: Funds now locked in smart contract
```

### 5. Mark Shipped (Farmer Action)
```
POST /orders/{id}/mark_shipped/
Authorization: Token <farmer-token>
Content-Type: application/json

{
  "tracking_number": "DHL-123456789"
}

Response:
{
  "status": "order marked as shipped"
}
```

### 6. Confirm Delivery (Buyer Action)
```
POST /orders/{id}/confirm_delivery/
Authorization: Token <buyer-token>

Response:
{
  "status": "delivery confirmed",
  "message": "Smart contract funds released to farmers",
  "order_id": 1
}

Note: Escrow automatically releases to farmers' wallets
```

### 7. Raise Dispute
```
POST /orders/{id}/raise_dispute/
Authorization: Token <token>
Content-Type: application/json

{
  "reason": "quality",
  "description": "Rice has excessive broken grains, exceeds contract specs"
}

Response:
{
  "id": 1,
  "reason": "quality",
  "description": "...",
  "status": "open",
  "created_at": "2026-03-20T15:45:00Z"
}

Note: Escrow remains locked until dispute resolved
```

---

## Smart Contract Endpoints

### 1. Create Escrow Contract (Admin)
```
POST /smartcontracts/contracts/create_escrow/
Authorization: Token <admin-token>
Content-Type: application/json

{
  "order_id": 1,
  "buyer_wallet": "0x8ba1f109551bD432803012645Ac136ddd64DBA72",
  "seller_wallets": [
    "0x742d35Cc6634C0532925a3b844Bc9e7595f42904",
    "0x123...",
    "0x456..."
  ],
  "delivery_days": 30
}

Response:
{
  "contract_id": 1,
  "contract_address": "0xabcd1234...",
  "status": "deployed",
  "escrow_amount": "232050",
  "delivery_deadline": "2026-04-19T10:30:00Z"
}
```

### 2. Check Contract Status
```
GET /smartcontracts/contracts/{id}/status/
Authorization: Token <token>

Response:
{
  "contract_id": 1,
  "contract_address": "0xabcd1234...",
  "status": "active",
  "order_id": 1,
  "escrow_amount": "232050",
  "delivery_deadline": "2026-04-19T10:30:00Z",
  "events": [
    {
      "event_type": "funded",
      "event_hash": "0x...",
      "block_number": 12345678,
      "created_at": "2026-03-20T12:00:00Z"
    }
  ]
}
```

### 3. Activate Contract (After Payment)
```
POST /smartcontracts/contracts/{id}/activate/
Authorization: Token <admin-token>

Response:
{
  "status": "active",
  "activation_tx": "0x..."
}

Note: Escrow funds now locked and unspendable
```

### 4. Release Funds (After Delivery)
```
POST /smartcontracts/contracts/{id}/release_funds/
Authorization: Token <admin-token>
Content-Type: application/json

{
  "recipient_wallets": {
    "0x742d35Cc6634C0532925a3b844Bc9e7595f42904": 50000,
    "0x123...": 45000,
    "0x456...": 42050
  }
}

Response:
{
  "status": "completed",
  "completion_tx": "0x...",
  "payments": {
    "0x742d35Cc...": 50000,
    "0x123...": 45000
  }
}

Note: Funds immediately transferred to farmer wallets
```

### 5. File Dispute (On Contract)
```
POST /smartcontracts/contracts/{id}/file_dispute/
Authorization: Token <admin-token>
Content-Type: application/json

{
  "reason": "Delivery failure - goods not received"
}

Response: Contract status updated, funds remain locked
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "quantity_kg must be a number"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
  "error": "Pool not found"
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## Example Flow: Complete Order Lifecycle

```bash
# 1. Buyer searches for rice pools
curl http://localhost:8000/api/products/pools/?search=rice \
  -H "Authorization: Token buyer_token"

# 2. Buyer finds a 10-tonne pool, needs 5 tonnes
# 3. Buyer creates order
curl -X POST http://localhost:8000/api/orders/create_order/ \
  -H "Authorization: Token buyer_token" \
  -H "Content-Type: application/json" \
  -d '{
    "pool_id": 1,
    "quantity_kg": 5000,
    "shipping_address": "Factory Address"
  }'

# 4. System creates order, status: "pending"
# Response: Order ID 42, Amount: 232050

# 5. Admin creates smart contract
curl -X POST http://localhost:8000/api/smartcontracts/contracts/create_escrow/ \
  -H "Authorization: Token admin_token" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 42,
    "buyer_wallet": "buyer_wallet_addr",
    "seller_wallets": ["farmer1", "farmer2", "farmer3"],
    "delivery_days": 30
  }'

# 6. Buyer initiates payment
curl -X POST http://localhost:8000/api/orders/42/initiate_payment/ \
  -H "Authorization: Token buyer_token"
# Status: "escrow_locked"

# 7. Farmers ship products
curl -X POST http://localhost:8000/api/orders/42/mark_shipped/ \
  -H "Authorization: Token farmer_token" \
  -H "Content-Type: application/json" \
  -d '{"tracking_number": "DHL-123456"}'

# 8. Buyer confirms delivery
curl -X POST http://localhost:8000/api/orders/42/confirm_delivery/ \
  -H "Authorization: Token buyer_token"
# Smart contract automatically releases funds to farmers

# 9. Admin can check final status
curl http://localhost:8000/api/smartcontracts/contracts/1/status/ \
  -H "Authorization: Token token"
# Shows: Status "completed", all funds released, blockchain events logged
```

---

## Rate Limiting & Pagination

All list endpoints support pagination:
```
GET /farmers/?page=2&page_size=20
```

---
