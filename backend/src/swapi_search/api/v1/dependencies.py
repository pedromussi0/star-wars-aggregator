from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from swapi_search.db.session import get_db
from swapi_search.search.base import BaseSearchEngine
from swapi_search.search.postgres import PostgresSearchEngine

def get_search_engine(
    db_session: Annotated[AsyncSession, Depends(get_db)]
) -> BaseSearchEngine:
    """
    Dependency provider for the search engine.
    This function determines which search engine implementation to use.
    """
    # if settings.SEARCH_ENGINE == "elasticsearch":
    #     return ElasticSearchEngine()
    return PostgresSearchEngine(db_session=db_session)