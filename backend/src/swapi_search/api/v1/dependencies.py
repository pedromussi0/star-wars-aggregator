# src/swapi_search/api/v1/dependencies.py

from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from swapi_search.repositories.resource import ResourceRepository
from swapi_search.db.session import get_db
from swapi_search.search.base import BaseSearchEngine
from swapi_search.search.postgres import PostgresSearchEngine

def get_search_engine(
    db_session: Annotated[AsyncSession, Depends(get_db)]
) -> BaseSearchEngine:
    """Dependency provider for the search engine."""
    return PostgresSearchEngine(db_session=db_session)

def get_resource_repository(
    db_session: Annotated[AsyncSession, Depends(get_db)]
) -> ResourceRepository:
    """
    Dependency provider for the ResourceRepository.
    Creates a repository instance with the current database session.
    """
    return ResourceRepository(db_session=db_session)
