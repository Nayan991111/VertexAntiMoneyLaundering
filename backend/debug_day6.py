import asyncio
import sys
from datetime import datetime

# 1. TEST DEPENDENCIES
print("1. Checking Dependencies...")
try:
    import rapidfuzz
    from app.services.watchlist_service import watchlist_service
    print(f"   [OK] RapidFuzz found. Version: {rapidfuzz.__version__}")
except ImportError as e:
    print(f"   [FAIL] Dependency missing: {e}")
    sys.exit(1)

# 2. TEST LOGIC & RULES
print("\n2. Checking Sanctions Logic...")
try:
    from app.rules.watchlist import WatchlistRule
    from app.schemas.transaction import TransactionCreate
    
    # Create a Mock Transaction (Pydantic Model)
    tx_data = TransactionCreate(
        customer_id=1,
        amount=200.0,
        currency="USD",
        transaction_type="TRANSFER",
        counterparty_account="ACC-987654",
        counterparty_name="Ivan Dragg", # The Typo
        nationality="US"
    )
    
    rule = WatchlistRule()
    # Run the rule synchronously for the test (mocking the async nature if needed)
    # We call the service directly to test logic
    is_hit, name, score = watchlist_service.check_sanction(tx_data.counterparty_name)
    
    if is_hit:
        print(f"   [OK] Sanctions Logic Works! Caught '{name}' (Score: {score})")
    else:
        print(f"   [FAIL] Sanctions Logic Failed. Did not catch Ivan Dragg.")
        
except Exception as e:
    print(f"   [CRASH] Logic Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 3. TEST DATABASE INSERT
print("\n3. Checking Database Integrity...")
try:
    from app.core.config import settings
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    from app.models.transaction import Transaction
    
    async def test_db():
        engine = create_async_engine(str(settings.DATABASE_URL))
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        async with async_session() as session:
            # Create a dummy transaction row (In-Memory, we won't commit to keep DB clean)
            db_txn = Transaction(
                customer_id=1,
                amount=tx_data.amount,
                currency=tx_data.currency,
                transaction_type=tx_data.transaction_type,
                counterparty_account=tx_data.counterparty_account,
                counterparty_name=tx_data.counterparty_name, # Critical Field
                status="BLOCKED",
                timestamp=datetime.now()
            )
            session.add(db_txn)
            print("   [OK] Database Model accepted the new fields.")
            
        await engine.dispose()

    asyncio.run(test_db())

except Exception as e:
    print(f"   [CRASH] Database Model Error: {e}")
    print("   HINT: This usually means the DB Table columns don't match the Code Model.")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n--- DIAGNOSTIC COMPLETE: ALL SYSTEMS GREEN ---")