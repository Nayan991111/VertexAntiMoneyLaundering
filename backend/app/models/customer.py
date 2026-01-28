from sqlalchemy import Column, Integer, String, DateTime, Float, Enum, Boolean
from sqlalchemy.sql import func
from app.models.base import Base
import enum

class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    
    # KYC Specifics
    nationality = Column(String)
    jurisdiction = Column(String) 
    kyc_status = Column(String, default="pending") 
    
    # Risk Engine
    risk_score = Column(Float, default=0.0)
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.LOW)
    is_pep = Column(Boolean, default=False) 
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())