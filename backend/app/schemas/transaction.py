from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# Base Schema
class TransactionBase(BaseModel):
    transaction_id: str = Field(..., description="Unique Transaction Reference (UTR) from bank")
    amount: float = Field(..., gt=0, description="Transaction amount")
    currency: str = Field(..., min_length=3, max_length=3, to_upper=True)
    sender_id: int = Field(..., description="Internal ID of the sending customer")
    receiver_account: str = Field(..., min_length=5, description="External receiver account/IBAN")
    transaction_type: str = Field("WIRE", description="WIRE, ACH, SWIFT, etc.")

# Input Schema
class TransactionCreate(TransactionBase):
    pass

# Output Schema
class TransactionResponse(TransactionBase):
    id: int
    status: str
    flagged_reason: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True