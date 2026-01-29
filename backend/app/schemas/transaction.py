from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount must be positive")
    currency: str = Field(..., min_length=3, max_length=3, pattern=r"^[A-Z]{3}$")
    transaction_type: str = Field(..., pattern=r"^(DEPOSIT|WITHDRAWAL|TRANSFER|PAYMENT)$")
    counterparty_name: str = Field(..., min_length=2, max_length=100)
    counterparty_account: str = Field(..., min_length=5, max_length=50)
    customer_id: int = Field(..., description="Foreign key linking to the customer")

    @field_validator('currency')
    def validate_currency(cls, v):
        allowed = ["USD", "EUR", "GBP", "INR", "JPY", "SGD"] # Add more as needed per ZeTheta specs
        if v not in allowed:
            raise ValueError(f"Currency {v} is not supported by ZeTheta Engine")
        return v

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    timestamp: datetime
    status: str  # PENDING, COMPLETED, FLAGGED
    risk_score: float

    class Config:
        from_attributes = True