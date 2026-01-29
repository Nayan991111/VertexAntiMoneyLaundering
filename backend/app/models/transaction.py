import uuid
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # External Reference ID (UUID for Idempotency)
    transaction_uuid = Column(String, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    
    # Financial Core Data
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)  # Enforce ISO 3-char code length
    transaction_type = Column(String, nullable=False)  # DEPOSIT, WITHDRAWAL, etc.
    status = Column(String, default="PENDING")  # PENDING, COMPLETED, FLAGGED, REJECTED
    
    # Counterparty Info (Who is on the other side?)
    counterparty_name = Column(String, nullable=False)
    counterparty_account = Column(String, nullable=False)
    
    # Relationship Linkage
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer", back_populates="transactions")
    
    # AML & Compliance Intelligence
    risk_score = Column(Float, default=0.0)  # 0.0 to 100.0
    flagged_reason = Column(String, nullable=True)  # "Velocity limit breached", etc.
    
    # Metadata
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Transaction {self.transaction_uuid} - {self.amount} {self.currency}>"