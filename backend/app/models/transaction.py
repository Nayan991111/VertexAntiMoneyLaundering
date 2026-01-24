import uuid
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # External Reference ID
    transaction_uuid = Column(String, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    
    # Financial Core Data
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    transaction_type = Column(String, nullable=False)
    status = Column(String, default="PENDING")
    
    # Counterparty Info
    counterparty_name = Column(String, nullable=False)
    counterparty_account = Column(String, nullable=False)
    
    # MISSING FIELD ADDED HERE:
    nationality = Column(String, nullable=True)
    
    # Relationship Linkage
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer", back_populates="transactions")
    
    # Compliance Intelligence
    risk_score = Column(Float, default=0.0)
    flagged_reason = Column(String, nullable=True)
    
    # Metadata
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Transaction {self.transaction_uuid} - {self.amount} {self.currency}>"