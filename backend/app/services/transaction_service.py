from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Imports must match the new Day 6 structure
from app.models.transaction import Transaction
from app.models.customer import Customer
from app.schemas.transaction import TransactionCreate
from app.services.graph_service import graph_service

# Rule Engine & Rules
from app.rules.engine import RuleEngine
from app.rules.structuring import StructuringRule
from app.rules.watchlist import WatchlistRule
from app.rules.velocity import VelocityRule

async def create_transaction(db: AsyncSession, transaction_in: TransactionCreate) -> Transaction:
    # 1. Validate Customer
    result = await db.execute(select(Customer).filter(Customer.id == transaction_in.customer_id))
    customer = result.scalars().first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")

    # 2. Rule Engine
    engine = RuleEngine()
    engine.add_rule(StructuringRule())
    engine.add_rule(VelocityRule())
    # Day 6: The WatchlistRule now scans counterparty_name
    engine.add_rule(WatchlistRule())
    
    context = {"db": db, "customer_id": customer.id}
    # This passes the Pydantic model (with counterparty_name) to the rules
    rule_results = await engine.evaluate(transaction_in, customer_context=context)
    
    # 3. Graph Intelligence (Circular Check)
    # We use a try/except block to ensure Graph downtime doesn't kill the SQL transaction
    try:
        is_circular = graph_service.check_circular_dependency(
            sender_id=customer.id, 
            counterparty_account=transaction_in.counterparty_account
        )
    except Exception as e:
        print(f"Graph Check Warning: {e}")
        is_circular = False

    # 4. Risk Calculation
    total_risk_score = engine.calculate_total_risk(rule_results)
    flagged_reasons = [res.reason for res in rule_results if res.triggered]
    
    # KILL SWITCH
    if is_circular:
        total_risk_score += 100
        flagged_reasons.append("Graph: Circular Round-Trip Detected (LAUNDERING SIGNAL)")

    reason_text = " | ".join(flagged_reasons) if flagged_reasons else None
    
    # Decision Matrix
    if total_risk_score >= 100:
        transaction_status = "BLOCKED"
    elif total_risk_score > 0:
        transaction_status = "FLAGGED"
    else:
        transaction_status = "COMPLETED"

    # 5. Persist to Postgres
    # .model_dump() automatically extracts 'counterparty_name' from the Pydantic model
    db_transaction = Transaction(
        **transaction_in.model_dump(),
        timestamp=datetime.now(),
        status=transaction_status,
        risk_score=total_risk_score,
        flagged_reason=reason_text
    )
    db.add(db_transaction)
    
    try:
        await db.commit()
        await db.refresh(db_transaction)
        
        # 6. Async Shadow Write (Sync to Neo4j)
        try:
            # Note: Graph Service might need updates later, but for now we sync core data
            graph_service.create_customer_node(customer.id, customer.full_name, customer.risk_score)
            graph_service.record_transaction(
                customer.id, 
                transaction_in.counterparty_account, 
                transaction_in.amount, 
                transaction_in.currency
            )
        except Exception as graph_e:
            print(f"WARNING: Graph sync failed: {graph_e}")
            
        return db_transaction
    except Exception as e:
        await db.rollback()
        # This will show up in your Terminal 1 logs if DB save fails
        print(f"DATABASE ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database commit failed: {str(e)}")