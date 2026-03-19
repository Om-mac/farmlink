# Architecture Documentation - FarmLink

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                             │
│         (Web App, Mobile App, External Systems)                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    Django REST API Layer                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Farmers | Buyers | Products | Orders | SmartContracts  │   │
│  │ (ViewSets, Serializers, Permission Classes)            │   │
│  └──────────────────┬──────────────────────────────────────┘   │
└─────────────────────┼──────────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────────┐
│                   Business Logic Layer                         │
│  ┌──────────────────┐      ┌──────────────────┐               │
│  │ Aggregation      │      │ Smart Contract   │               │
│  │ Engine           │      │ Service          │               │
│  │ - Pool Creation  │      │ - Escrow Logic   │               │
│  │ - Matching       │      │ - Fund Release   │               │
│  │ - Capacity Calc  │      │ - Dispute Mgt    │               │
│  └──────────────────┘      └──────────────────┘               │
│         │                           │                          │
└─────────┼───────────────────────────┼──────────────────────────┘
          │                           │
┌─────────▼───────────────────────────▼──────────────────────────┐
│                    Data Access Layer (ORM)                     │
│            (Django Models & Database Queries)                  │
└─────────────────┬──────────────────────────────────────────────┘
                  │
┌─────────────────▼──────────────────────────────────────────────┐
│                   Data Storage Layer                           │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │  SQLite (Dev)    │  │  PostgreSQL      │                   │
│  │  Or PostgreSQL   │  │  (Production)    │                   │
│  │                  │  │                  │                   │
│  │ 14 Models total  │  │ - Farmers        │                   │
│  │                  │  │ - Buyers         │                   │
│  │                  │  │ - Orders         │                   │
│  │                  │  │ - Smart Contracts│                   │
│  │                  │  │ - & more...      │                   │
│  └──────────────────┘  └──────────────────┘                   │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                  External Integrations                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ AWS Managed Blockchain                                   │   │
│  │ - Smart Contract Deployment                             │   │
│  │ - Fund Escrow Management                                │   │
│  │ - Transaction Tracking                                  │   │
│  │ - Event Logging                                         │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Email/Notification Service (Future)                     │   │
│  │ Payment Gateway (Future)                                │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

## Data Models Relationship Diagram

```
┌─────────────┐
│    User     │ (Django Auth)
└──────┬──────┘
       │
       ├─────────────────────────┬──────────────────────────
       │                         │
       ▼                         ▼
  ┌─────────────┐          ┌─────────────┐
  │  Farmer     │          │   Buyer     │
  ├─────────────┤          ├─────────────┤
  │ - profile   │          │ - company   │
  │ - capacity  │          │ - details   │
  │ - wallet    │          │ - wallet    │
  └──────┬──────┘          └──────┬──────┘
         │                        │
         ▼                        ▼
  ┌─────────────┐          ┌──────────────┐
  │ FarmProduct │          │    Order     │
  ├─────────────┤          ├──────────────┤
  │ - product   │          │ - quantity   │
  │ - price     │          │ - status     │
  │ - capacity  │          │ - smart_ct   │
  └──────┬──────┘          │ - amount     │
         │                 └────────┬─────┘
         │                         │
         └──────────┬──────────────┘
                    ▼
         ┌─────────────────────┐
         │ Aggregated Pool     │
         ├─────────────────────┤
         │ - product_name      │
         │ - total_capacity    │
         │ - farmers (M2M)     │
         │ - status            │
         └──────────┬──────────┘
                    │
                    ▼
         ┌─────────────────────┐
         │  SmartContract      │
         ├─────────────────────┤
         │ - address           │
         │ - escrow_amount     │
         │ - seller_wallets    │
         │ - status            │
         │ - txn_hashes        │
         └──────────┬──────────┘
                    │
                    ▼
         ┌─────────────────────┐
         │  ContractEvent      │
         ├─────────────────────┤
         │ - event_type        │
         │ - event_hash        │
         │ - block_number      │
         └─────────────────────┘
```

## Order Lifecycle & Smart Contract Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: INITIALIZATION                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Buyer creates Order from Aggregated Pool                      │
│  ├─ SELECT pool with multiple farmers                          │
│  ├─ ENTER quantity_kg and shipping_address                     │
│  └─ CALCULATE: product_cost + 2% platform_fee = total_amount   │
│                                                                 │
│  Status: PENDING                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: SMART CONTRACT DEPLOYMENT                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Admin initiates smart contract creation                       │
│  ├─ GET buyer wallet (from Buyer profile)                      │
│  ├─ GET farmer wallets (from aggregated pool farmers)          │
│  ├─ LOCK escrow_amount on blockchain                           │
│  └─ DEPLOY contract with delivery deadline                     │
│                                                                 │
│  SmartContract created:                                        │
│  ├─ contract_address: 0xabcd... (immutable)                    │
│  ├─ status: DEPLOYED                                           │
│  └─ Order.smart_contract_id = contract_address                │
│                                                                 │
│  Status: PENDING (awaiting buyer payment)                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: PAYMENT LOCKING (Buyer Action)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Buyer calls: /orders/{id}/initiate_payment/                  │
│  ├─ TRANSFER total_amount to smart contract                    │
│  ├─ Smart contract VERIFIES funds received                     │
│  ├─ CONTRACT LOCKS funds (no withdrawal possible)              │
│  └─ CONTRACT STATUS → ACTIVE                                   │
│                                                                 │
│  Security: Funds now controlled by blockchain, not buyer      │
│  ├─ Farmer protected: will get paid on delivery               │
│  └─ Buyer protected: can dispute if issues arise              │
│                                                                 │
│  Status: ESCROW_LOCKED                                        │
│  event: FUNDED (logged in ContractEvent)                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: FULFILLMENT (Farmer Action)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Farmers ship their portions of the order                      │
│  ├─ AGGREGATE shipments from 5-20 different farmers            │
│  ├─ CONSOLIDATE at distribution center (quality check)         │
│  └─ TRACK shipments separately                                 │
│                                                                 │
│  Farmer calls: /orders/{id}/mark_shipped/                     │
│  ├─ ENTER tracking numbers                                     │
│  └─ STATUS → SHIPPED                                           │
│                                                                 │
│  Quality Assurance Check:                                      │
│  ├─ Verify all portions match specifications                   │
│  ├─ Check weight and grade                                     │
│  └─ Log results in QualityAssurance model                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: DELIVERY CONFIRMATION (Buyer Action)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Buyer inspects received goods                                 │
│                                                                 │
│  Buyer calls: /orders/{id}/confirm_delivery/                  │
│  ├─ CONFIRM goods match order specifications                   │
│  ├─ TriggerSmart Contract → RELEASE_FUNDS                      │
│  └─ STATUS → DELIVERED                                         │
│                                                                 │
│  Smart Contract Execution:                                     │
│  ├─ SEND proporitonal amount to each farmer wallet             │
│  ├─ Example (5 farmers totaling 5 tonnes):                     │
│  │  Farmer1: 1000kg × price = wallet transfer                 │
│  │  Farmer2: 1200kg × price = wallet transfer                 │
│  │  Farmer3: 900kg × price = wallet transfer                  │
│  │  Farmer4: 1100kg × price = wallet transfer                 │
│  │  Farmer5: 800kg × price = wallet transfer                  │
│  │  Platform: 2% fee = wallet transfer                        │
│  │                                                             │
│  ├─ ALL TRANSFERS in single transaction (atomic)               │
│  └─ STATUS → COMPLETED                                         │
│                                                                 │
│  event: PAYMENT_RELEASED (logged in ContractEvent)            │
│                                                                 │
│  All funds transferred permanently & irreversibly             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STEP 6: DISPUTE HANDLING (Optional)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  IF at any point buyer detects issue:                          │
│                                                                 │
│  Buyer calls: /orders/{id}/raise_dispute/                     │
│  ├─ SPECIFY reason (quality, quantity, late delivery, etc)     │
│  ├─ PROVIDE evidence                                           │
│  └─ STATUS → DISPUTED                                          │
│                                                                 │
│  Smart Contract Pauses:                                        │
│  ├─ HOLD funds in escrow                                       │
│  ├─ PREVENT any releases                                       │
│  └─ AWAIT admin resolution                                     │
│                                                                 │
│  Admin Reviews:                                                │
│  ├─ ANALYZE evidence and shipment data                         │
│  ├─ CONTACT buyer and farmers                                  │
│  └─ RESOLVE dispute                                            │
│                                                                 │
│  Outcomes:                                                      │
│  ├─ IF buyer false claim → RELEASE to farmers                  │
│  ├─ IF farmer fraud detected → REFUND buyer                    │
│  └─ IF partial issue → PARTIAL release/refund                  │
│                                                                 │
│  event: DISPUTE_FILED & DISPUTE_RESOLVED (logged)             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Aggregation Engine Algorithm

```
INPUT: Buyer needs 10 tonnes of Rice

┌────────────────────────────────────────┐
│ STEP 1: FIND ALL ELIGIBLE PRODUCTS    │
├────────────────────────────────────────┤
│                                        │
│ Query: FarmProduct.filter(             │
│     product_name__icontains='rice',   │
│     verified=True,                     │
│     farmer__verified=True              │
│ )                                      │
│                                        │
│ Result: 12 farmers with rice           │
│ ├─ Farmer A: 500 kg/day, Grade A      │
│ ├─ Farmer B: 400 kg/day, Grade A      │
│ ├─ Farmer C: 300 kg/day, Grade B      │
│ └─ ... (9 more)                       │
│                                        │
└────────────────────────────────────────┘
                  │
                  ▼
┌────────────────────────────────────────┐
│ STEP 2: AGGREGATE CAPACITY            │
├────────────────────────────────────────┤
│                                        │
│ total_capacity = SUM(daily_capacity)   │
│ = 500 + 400 + 300 + ... = 5500 kg     │
│                                        │
│ ✓ Sufficient for 10-tonne order       │
│   (5500 kg can be scaled to 10+ tonnes)│
│                                        │
└────────────────────────────────────────┘
                  │
                  ▼
┌────────────────────────────────────────┐
│ STEP 3: CREATE AGGREGATED POOL       │
├────────────────────────────────────────┤
│                                        │
│ AggregatedProductPool.create(          │
│     product_name='Basmati Rice',      │
│     source_products=[A, B, C...],      │
│     total_available_kg=5000,           │
│     target_quantity_kg=10000,          │
│     average_price_per_kg=45.50         │
│ )                                      │
│                                        │
│ Result: One pool representing          │
│ 10+ farmers' combined capacity         │
│                                        │
└────────────────────────────────────────┘
                  │
                  ▼
┌────────────────────────────────────────┐
│ STEP 4: ENABLE BULK ORDERS            │
├────────────────────────────────────────┤
│                                        │
│ Buyer can now:                         │
│ ├─ Single order for 10 tonnes          │
│ ├─ Single smart contract               │
│ ├─ Single payment/escrow               │
│ └─ Automatic multi-farmer settlement   │
│                                        │
│ Instead of:                            │
│ ├─ ✗ 10 separate orders                │
│ ├─ ✗ 10 separate smart contracts       │
│ ├─ ✗ 10 separate negotiations          │
│ └─ ✗ 10 separate payments              │
│                                        │
└────────────────────────────────────────┘
```

## AWS Managed Blockchain Integration Points

```
┌─────────────────────────────────────────────────────────────────┐
│ AWS Managed Blockchain Configuration                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1. NETWORK SETUP                                               │
│    ├─ Create network (Hyperledger Fabric or Ethereum)         │
│    ├─ Create member in network                                 │
│    └─ Configure CA (Certificate Authority)                    │
│                                                                 │
│ 2. RPC ENDPOINT                                                │
│    ├─ Get RPC endpoint from AWS console                       │
│    ├─ Configure in AWSManagedBlockchainConfig                 │
│    └─ Use for contract deployment                             │
│                                                                 │
│ 3. SMART CONTRACT                                              │
│    ├─ Write Solidity contract (escrow logic)                  │
│    ├─ Compile contract                                        │
│    ├─ Deploy to network via RPC                               │
│    └─ Store contract_address in config                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Order Execution on Blockchain                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1. CREATE ESCROW (Buyer creates order)                        │
│    ├─ Call: escrowContract.createEscrow(                      │
│    │      buyer, sellers, amount, deadline)                   │
│    ├─ Blockchain locks funds                                  │
│    └─ Return: contractInstance                                │
│                                                                 │
│ 2. DEPOSIT FUNDS (Buyer pays)                                 │
│    ├─ Call: escrowContract.deposit( )                         │
│    │      {value: totalAmount}                                │
│    ├─ Funds transferred to escrow address                     │
│    └─ Status: FUNDED                                          │
│                                                                 │
│ 3. MARK SHIPPED (Farmer ships)                                │
│    ├─ Call: escrowContract.markShipped(orderId)              │
│    └─ Log event: SHIPPED                                      │
│                                                                 │
│ 4. RELEASE ESCROW (Buyer confirms)                           │
│    ├─ Call: escrowContract.releasePayment(                    │
│    │      sellerWallets, amounts)                             │
│    ├─ For each seller:                                        │
│    │  └─ Transfer amount to wallet                            │
│    └─ Status: RELEASED                                        │
│                                                                 │
│ 5. REFUND (Dispute resolution)                               │
│    ├─ Call: escrowContract.refund(buyerWallet, amount)       │
│    ├─ Not executed in normal flow                             │
│    └─ Only on confirmed fraud/non-delivery                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Security Model

```
Authentication & Authorization:
├─ Token-based (Django REST framework)
├─ Role-based access:
│  ├─ Public: List endpoints
│  ├─ Authenticated: Own profile/orders
│  ├─ Admin: Contract management, verification
│  └─ SuperUser: Full access
└─ Permission classes on all endpoints

Data Protection:
├─ CSRF tokens on all forms
├─ SQL injection prevention (ORM)
├─ Input validation (serializers)
├─ Password hashing (Django auth)
└─ HTTPS recommended for production

Blockchain Security:
├─ Smart contract controls fund access
├─ Immutable transaction records
├─ All state changes logged
├─ Multi-signature possible
└─ Wallet private keys never stored on server
```

---

This architecture enables FarmLink to solve the scale mismatch problem while maintaining security, transparency, and trust through blockchain technology.
