from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from app.models.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True) # Bank Reference ID
    
    amount = Column(Float)
    currency = Column(String)
    
    sender_id = Column(Integer, ForeignKey("customers.id"))
    receiver_account = Column(String) 
    
    # AML Fields
    transaction_type = Column(String) # wire, cash, crypto
    status = Column(String, default="processed") 
    flagged_reason = Column(String, nullable=True)
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())