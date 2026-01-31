from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.deps import get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services import transaction_service

router = APIRouter()

@router.post("/", response_model=TransactionResponse, status_code=201)
async def create_new_transaction(
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Ingest a new financial transaction.
    - Validates Customer ID existence.
    - Enforces ISO currency codes.
    - Sets initial risk score to 0.0.
    """
    return await transaction_service.create_transaction(db=db, transaction_in=transaction)

@router.get("/customer/{customer_id}", response_model=List[TransactionResponse])
async def read_customer_transactions(
    customer_id: int,
    skip: int = 0, 
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await transaction_service.get_transactions_by_customer(db, customer_id, skip, limit)