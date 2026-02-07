from fastapi import APIRouter, HTTPException
from typing import List, Any
from pydantic import BaseModel
from datetime import datetime
import uuid
import random

# Define schemas locally to avoid import errors
class TransactionCreate(BaseModel):
    amount: float
    currency: str = "USD"
    sender_account_id: str
    receiver_account_id: str
    notes: str = None
    is_simulated: bool = False

class Transaction(TransactionCreate):
    transaction_id: str
    timestamp: datetime

router = APIRouter()

# -------------------------------------------------------------------
# 1. INGESTION ENDPOINT (Used by live_simulation.py)
# -------------------------------------------------------------------
@router.post("/", response_model=Transaction)
async def create_transaction(transaction: TransactionCreate):
    # In a real app
    # portfolio demo
    return {
        "transaction_id": str(uuid.uuid4()),
        "amount": transaction.amount,
        "currency": transaction.currency,
        "sender_account_id": transaction.sender_account_id,
        "receiver_account_id": transaction.receiver_account_id,
        "timestamp": datetime.now(),
        "notes": transaction.notes,
        "is_simulated": True
    }

# -------------------------------------------------------------------
# 2. VIEW ENDPOINT (This fixes the 405 Error on Dashboard)
# -------------------------------------------------------------------
@router.get("/", response_model=List[dict])
async def read_transactions(limit: int = 50):
    """
    Returns recent transactions. 
    Generates realistic mock data so the Dashboard ALWAYS looks alive.
    """
    mock_data = []
    names = ["ACC_NAYAN", "ACC_VIKRAM", "ACC_SHELL_CORP", "ACC_OFFSHORE_A", "ACC_KAVYA"]
    
    for _ in range(limit):
        sender = random.choice(names)
        receiver = random.choice([n for n in names if n != sender])
        mock_data.append({
            "transaction_id": str(uuid.uuid4()),
            "amount": round(random.uniform(100, 15000), 2),
            "currency": "USD",
            "sender_account_id": sender,
            "receiver_account_id": receiver,
            "timestamp": datetime.now().isoformat(),
            "notes": "High Frequency Trading" if random.random() > 0.2 else "REF: CYCLIC_LOOP_DETECTED",
            "is_simulated": True
        })
    return mock_data