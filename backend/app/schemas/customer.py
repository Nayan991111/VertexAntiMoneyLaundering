from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.customer import RiskLevel

# Base Schema: Shared properties
class CustomerBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100, description="Legal full name")
    email: EmailStr
    phone_number: str = Field(..., pattern=r"^\+?[1-9]\d{1,14}$", description="E.164 format")
    nationality: str = Field(..., min_length=2, max_length=2, to_upper=True, description="ISO 3166-1 alpha-2 code")
    jurisdiction: str = Field(..., min_length=2, max_length=2, to_upper=True, description="Tax residence jurisdiction")

# Input Schema
class CustomerCreate(CustomerBase):
    pass

# Output Schema
class CustomerResponse(CustomerBase):
    id: int
    kyc_status: str
    risk_score: float
    risk_level: RiskLevel
    is_pep: bool
    created_at: datetime
    # FIX: Make updated_at Optional because it is None on creation
    updated_at: Optional[datetime] = None 

    class Config:
        from_attributes = True