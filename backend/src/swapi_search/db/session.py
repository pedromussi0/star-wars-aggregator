# src/swapi_search/db/session.py

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text

from swapi_search.core.config import settings

logger = logging.getLogger(__name__)

# The SWAPI ETL script is synchronous, so it needs a synchronous engine.
sync_engine = create_engine(str(settings.DATABASE_URL), pool_pre_ping=True)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Use the new ASYNC_DATABASE_URL computed field for the async engine
async_engine = create_async_engine(settings.ASYNC_DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncSession:
    """
    Dependency to get an async database session.
    """
    async with AsyncSessionLocal() as session:
        yield session

async def check_db_connection():
    """
    Verifies that the database connection is available.
    """
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection successful.")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise