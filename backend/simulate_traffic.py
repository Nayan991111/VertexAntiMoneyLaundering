import asyncio
import random
import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import async_session_factory
from app.models.transaction import Transaction
from app.models.customer import Customer

# Step 2 Import: The Graph Service
from app.services.graph_service import graph_service

# Lists for random generation
SANCTIONED_NAMES = ["Osama Bin Laden", "Pablo Escobar", "Ivan Drago"]
SAFE_NAMES = ["Alice Corp", "Bob Ltd", "Charlie Inc", "Delta LLC"]

async def generate_data():
    # 1. Check Graph Connection
    print("--- CHECKING INFRASTRUCTURE ---")
    if graph_service.check_connection():
        print("✅ Neo4j Graph Database is ONLINE.")
    else:
        print("⚠️ Neo4j is OFFLINE. Graph data will be skipped.")

    async with async_session_factory() as session:
        print("--- GENERATING DAY 12 HYBRID DATA ---")
        
        # Check if root customer exists
        result = await session.execute(select(Customer).where(Customer.email == "nayan@sentinelflow.com"))
        customer = result.scalars().first()

        if not customer:
            customer = Customer(
                full_name="Nayan Trading", 
                email="nayan@sentinelflow.com", 
                risk_score=10.0,
                kyc_status="VERIFIED",
                phone_number="+91 6297537885",
                nationality="IN",
                jurisdiction="India",
                risk_level="LOW",
                is_pep=False
            )
            session.add(customer)
            await session.flush()
            print("Created Root Customer.")
        else:
            print("Found Existing Customer.")

        transactions = []
        
        # --- 1. SAFE TRANSACTIONS (SQL ONLY) ---
        for _ in range(20):
            transactions.append(Transaction(
                transaction_uuid=str(uuid.uuid4()),
                amount=random.uniform(100, 5000),
                currency="USD",
                transaction_type="WIRE_OUT",
                status="CLEARED",
                counterparty_name=random.choice(SAFE_NAMES),
                counterparty_account=f"ACC-{random.randint(1000,9999)}",
                nationality="US",
                customer_id=customer.id,
                risk_score=random.uniform(0, 10),
                timestamp=datetime.now()
            ))

        # --- 2. SANCTIONED TRANSACTIONS (SQL ONLY) ---
        for _ in range(5):
            target = random.choice(SANCTIONED_NAMES)
            transactions.append(Transaction(
                transaction_uuid=str(uuid.uuid4()),
                amount=random.uniform(10000, 50000),
                currency="USD",
                transaction_type="WIRE_OUT",
                status="BLOCKED",
                counterparty_name=target,
                counterparty_account="BLOCKED-ACC",
                nationality="NK", 
                customer_id=customer.id,
                risk_score=100.0,
                flagged_reason=f"SANCTION MATCH: '{target}'"
            ))

        # --- 3. MONEY LAUNDERING RING (SQL + GRAPH SYNC) ---
        # We create a closed loop: Member A -> Member B -> Member C -> Member A
        print("⚠️ Injecting Money Laundering Ring (A->B->C->A)...")
        
        ring_members = ["Ring_Member_A", "Ring_Member_B", "Ring_Member_C"]
        
        for i in range(len(ring_members)):
            sender = ring_members[i]
            receiver = ring_members[(i + 1) % len(ring_members)] # Wraps back to start
            amount = 9500.0 # Just under 10k threshold
            txn_uuid = str(uuid.uuid4())

            # A. Ingest into Graph (The Relationship)
            graph_service.ingest_transaction(sender, receiver, amount, txn_uuid)

            # B. Ingest into SQL (The Ledger Record)
            # Note: We associate these with the root customer for visibility in the dashboard
            transactions.append(Transaction(
                transaction_uuid=txn_uuid,
                amount=amount,
                currency="USD",
                transaction_type="WIRE_OUT",
                status="CLEARED", # Often cleared because they look individually safe
                counterparty_name=receiver, # The root customer is sending to these ring members in this sim context
                counterparty_account=f"RING-{receiver}",
                nationality="KY", # Cayman Islands
                customer_id=customer.id,
                risk_score=85.0,
                flagged_reason="GRAPH_ANALYSIS_PENDING"
            ))

        session.add_all(transactions)
        await session.commit()
        print(f"Successfully injected {len(transactions)} transactions.")
        print("✅ Graph Data Synchronized.")

if __name__ == "__main__":
    asyncio.run(generate_data())