from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.customer import Customer, RiskLevel
from app.schemas.customer import CustomerCreate

async def create_customer(db: AsyncSession, customer_in: CustomerCreate) -> Customer:
    """
    Creates a new customer in the Postgres database.
    Injects default initial compliance state (PENDING, LOW Risk).
    """
    # 1. Create the ORM object
    # We unpack the input data AND explicitly set the initial compliance state
    db_customer = Customer(
        **customer_in.model_dump(),
        kyc_status="PENDING",
        risk_score=0.0,
        risk_level=RiskLevel.LOW,  # Ensure this matches your Enum in models/customer.py
        is_pep=False
    )
    
    # 2. Add to session
    db.add(db_customer)
    
    # 3. Commit the transaction (save to DB)
    try:
        await db.commit()
        # 4. Refresh to get ID and timestamps
        await db.refresh(db_customer)
        return db_customer
    except Exception as e:
        await db.rollback()
        raise e

async def get_customers(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of customers with pagination.
    """
    result = await db.execute(select(Customer).offset(skip).limit(limit))
    return result.scalars().all()