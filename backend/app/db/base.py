from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Database URL
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Session Factory
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base Class for Models
Base = declarative_base()

# Dependency for API
async def get_db():
    async with async_session_factory() as session:
        yield session