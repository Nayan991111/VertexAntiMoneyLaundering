from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    # The new field MUST be here
    counterparty_name: str = Field(..., min_length=1)
    counterparty_account: str = Field(..., min_length=1)
    transaction_type: str
    nationality: Optional[str] = None

    @field_validator('transaction_type')
    def validate_type(cls, v):
        allowed = {'DEPOSIT', 'WITHDRAWAL', 'TRANSFER', 'PAYMENT'}
        if v.upper() not in allowed:
            raise ValueError(f"Must be one of: {allowed}")
        return v.upper()

class TransactionCreate(TransactionBase):
    customer_id: int

class TransactionResponse(TransactionBase):
    id: int
    transaction_uuid: str
    status: str
    risk_score: float
    flagged_reason: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True