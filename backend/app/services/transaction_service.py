from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.transaction import Transaction
from app.models.customer import Customer
from app.schemas.transaction import TransactionCreate
from app.services.graph_service import graph_service  # <--- Ensure this exists from Step 3

async def create_transaction(db: AsyncSession, transaction_in: TransactionCreate) -> Transaction:
    # 1. Verify Customer Exists
    result = await db.execute(select(Customer).filter(Customer.id == transaction_in.customer_id))
    customer = result.scalars().first()
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer ID {transaction_in.customer_id} not found.")

    # 2. Create Transaction Object in Postgres
    db_transaction = Transaction(
        **transaction_in.model_dump(),
        timestamp=datetime.now(), # Fixed: used now() instead of utcnow() for Py3.13 compat if needed
        status="COMPLETED", 
        risk_score=0.0
    )
    
    db.add(db_transaction)
    
    try:
        await db.commit()
        await db.refresh(db_transaction)
        
        # 3. Sync to Neo4j (Shadow Write)
        try:
            # Ensure customer node exists first
            graph_service.create_customer_node(customer.id, customer.full_name, customer.risk_score)
            
            # Draw the relationship
            graph_service.record_transaction(
                sender_id=customer.id,
                counterparty_account=transaction_in.counterparty_account,
                amount=transaction_in.amount,
                currency=transaction_in.currency
            )
        except Exception as graph_e:
            print(f"WARNING: Graph sync failed: {graph_e}")
            
        return db_transaction

    except Exception as e:
        await db.rollback()
        raise e

async def get_transactions_by_customer(db: AsyncSession, customer_id: int, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Transaction)
        .filter(Transaction.customer_id == customer_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()