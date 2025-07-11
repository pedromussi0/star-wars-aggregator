from typing import List, Optional, Dict, Any
from sqlalchemy import select, text, case

from swapi_search.db.models import SwapiResource
from swapi_search.search.base import BaseSearchEngine
from sqlalchemy.ext.asyncio import AsyncSession


class PostgresSearchEngine(BaseSearchEngine):
    """
    A search engine implementation that uses PostgreSQL's ILIKE for
    case-insensitive, partial-text search, with a relevance-ranking system.
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
        Searches the swapi_resource table, ranking results that match
        the 'name' field higher than those that match in other fields.
        """
        search_term = f"%{query}%"

        relevance = case(
            (SwapiResource.name.ilike(search_term), 2),
            else_=1
        ).label("relevance")

        stmt = select(SwapiResource.data, relevance).where(
            SwapiResource.searchable_text.ilike(search_term)
        )

        if resource_type:
            stmt = stmt.where(SwapiResource.type == resource_type)

        stmt = stmt.order_by(relevance.desc(), SwapiResource.id).limit(limit).offset(offset)

        result = await self.db_session.execute(stmt)
        return [row[0] for row in result.all()]