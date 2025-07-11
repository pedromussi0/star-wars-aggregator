from typing import List, Optional, Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from swapi_search.db.models import SwapiResource
from swapi_search.search.base import BaseSearchEngine


class PostgresSearchEngine(BaseSearchEngine):
    """
    A search engine implementation that uses PostgreSQL's ILIKE for
    case-insensitive, partial-text search.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def search(
        self,
        query: str,
        resource_type: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Searches the swapi_resource table using a full-text search strategy.
        """
        stmt = select(SwapiResource.data).where(
            SwapiResource.searchable_text.ilike(f"%{query}%")
        )

        if resource_type:
            stmt = stmt.where(SwapiResource.type == resource_type)

        stmt = stmt.order_by(SwapiResource.id).limit(limit).offset(offset)

        result = await self.db_session.execute(stmt)
        return [row[0] for row in result.all()]