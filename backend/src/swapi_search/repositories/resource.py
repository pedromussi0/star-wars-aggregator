from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, String


from swapi_search.db.models import SwapiResource

class ResourceRepository:
    """
    This class encapsulates all database access logic for SwapiResource entities.
    The rest of the application should use this repository to interact with
    the database.
    """
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    def _apply_filters(self, stmt, filters: Optional[Dict[str, Any]] = None):
        """
        A helper method to dynamically apply filters to a SQLAlchemy query.
        This function iterates through a dictionary of filters and adds
        a WHERE clause for each one, searching within the JSONB 'data' column.
        """
        if filters:
            for key, value in filters.items():
                if value is not None:
                    # This query searches within the 'data' JSONB column.
                    # It casts the JSONB value to text to perform a case-insensitive LIKE.
                    # e.g., data->>'director' ILIKE '%George Lucas%'
                    stmt = stmt.where(
                        cast(SwapiResource.data[key], String).ilike(f"%{value}%")
                    )
        return stmt

    async def get_resource_by_id(self, resource_type: str, resource_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a single resource by its type and swapi_id."""
        stmt = select(SwapiResource.data).where(
            SwapiResource.type == resource_type,
            SwapiResource.swapi_id == resource_id
        )
        result = (await self.db_session.execute(stmt)).scalar_one_or_none()
        return result

    async def get_all_resources(self, resource_type: str, limit: int, offset: int, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieves a paginated list of resources of a specific type."""
        stmt = (
            select(SwapiResource.data)
            .where(SwapiResource.type == resource_type)
            .order_by(SwapiResource.swapi_id)
            .limit(limit)
            .offset(offset)
        )
        stmt = self._apply_filters(stmt, filters)

        result = await self.db_session.execute(stmt)
        return [row[0] for row in result.all()]

    async def count_resources(self, resource_type: str, filters: Optional[Dict[str, Any]] = None) -> int:
        """Counts the total number of resources of a specific type."""
        count_stmt = select(func.count(SwapiResource.id)).where(SwapiResource.type == resource_type)
        count_stmt = self._apply_filters(count_stmt, filters)
        total_count = (await self.db_session.execute(count_stmt)).scalar_one()
        return total_count