import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.models.base import Base
# IMPORTANT: Import models so they register with Base.metadata
from app.models.customer import Customer
from app.models.transaction import Transaction

async def init_db():
    print(f"Connecting to: {settings.DATABASE_URL}")
    engine = create_async_engine(str(settings.DATABASE_URL))
    
    async with engine.begin() as conn:
        print("--- DROPPING OLD TABLES (IF ANY) ---")
        await conn.run_sync(Base.metadata.drop_all)
        print("--- CREATING NEW SCHEMA ---")
        await conn.run_sync(Base.metadata.create_all)
        print("--- SUCCESS: TABLES CREATED ---")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())