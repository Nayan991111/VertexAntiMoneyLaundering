from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import Settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

settings = Settings()

# Re-create engine here for dependency injection usage
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False, 
    autoflush=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session for a request
    and closes it when the request is done.
    """
    async with AsyncSessionLocal() as session:
        yield session