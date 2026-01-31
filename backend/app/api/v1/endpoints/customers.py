from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.deps import get_db  # We will create this dependency next
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services import customer_service

router = APIRouter()

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_new_customer(
    customer: CustomerCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new customer.
    - Validates email, phone, and country codes.
    - Persists to PostgreSQL.
    - Returns the created customer with ID and KYC status.
    """
    try:
        return await customer_service.create_customer(db=db, customer_in=customer)
    except Exception as e:
        # In a real app, we'd handle specific IntegrityErrors (duplicate email) here
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[CustomerResponse])
async def read_customers(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """
    Get a list of customers.
    """
    return await customer_service.get_customers(db=db, skip=skip, limit=limit)