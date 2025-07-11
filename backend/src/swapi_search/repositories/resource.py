from typing import List, Dict, Any, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from swapi_search.db.models import SwapiResource

class ResourceRepository:
    """
    This class encapsulates all database access logic for SwapiResource entities.
    The rest of the application should use this repository to interact with
    the database.
    """
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_resource_by_id(self, resource_type: str, resource_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a single resource by its type and swapi_id."""
        stmt = select(SwapiResource.data).where(
            SwapiResource.type == resource_type,
            SwapiResource.swapi_id == resource_id
        )
        result = (await self.db_session.execute(stmt)).scalar_one_or_none()
        return result

    async def get_all_resources(self, resource_type: str, limit: int, offset: int) -> List[Dict[str, Any]]:
        """Retrieves a paginated list of resources of a specific type."""
        stmt = (
            select(SwapiResource.data)
            .where(SwapiResource.type == resource_type)
            .order_by(SwapiResource.swapi_id)
            .limit(limit)
            .offset(offset)
        )
        result = await self.db_session.execute(stmt)
        return [row[0] for row in result.all()]

    async def count_resources(self, resource_type: str) -> int:
        """Counts the total number of resources of a specific type."""
        count_stmt = select(func.count(SwapiResource.id)).where(SwapiResource.type == resource_type)
        total_count = (await self.db_session.execute(count_stmt)).scalar_one()
        return total_count