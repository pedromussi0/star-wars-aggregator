from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from swapi_search.db.models import SwapiResource
from swapi_search.db.session import get_db
from swapi_search.api.v1.schemas import PaginatedResponse

def resource_router_factory(
    resource_type: str,
    response_model: type,
    tag: str
) -> APIRouter:
    """
    A factory that generates a set of RESTful endpoints for a resource type.

    This powerful pattern allows us to create complete CRUD-like APIs for
    any resource ('films', 'people', etc.) with minimal code duplication.

    Args:
        resource_type: The string name of the resource (e.g., 'films').
        response_model: The Pydantic model for the response.
        tag: The tag to group endpoints under in the OpenAPI documentation.

    Returns:
        An APIRouter instance with 'get all' and 'get one' endpoints.
    """
    router = APIRouter(prefix=f"/{resource_type}", tags=[tag])
    DetailResponseModel = response_model

    @router.get(
        "",
        response_model=PaginatedResponse[DetailResponseModel],
        summary=f"Get a list of all {resource_type.capitalize()}"
    )
    async def get_all_resources(
        db: AsyncSession = Depends(get_db),
        limit: int = Query(10, ge=1, le=100, description="Number of results to return."),
        offset: int = Query(0, ge=0, description="Offset for pagination."),
    ):
        """
        Retrieves a paginated list of all resources of this type from the
        database, ordered by their original SWAPI ID.
        """
        # A subquery to get the total count efficiently.
        count_stmt = select(func.count(SwapiResource.id)).where(SwapiResource.type == resource_type)
        total_count = (await db.execute(count_stmt)).scalar_one()

        # The main query to fetch the paginated data.
        stmt = (
            select(SwapiResource.data)
            .where(SwapiResource.type == resource_type)
            .order_by(SwapiResource.swapi_id)
            .limit(limit)
            .offset(offset)
        )
        result = await db.execute(stmt)
        # We extract the JSON data from the first column of each row.
        items = [row[0] for row in result.all()]

        return {
            "count": total_count,
            "limit": limit,
            "offset": offset,
            "results": items,
        }

    @router.get(
        "/{resource_id}",
        response_model=DetailResponseModel,
        summary=f"Get a single {resource_type.capitalize()} by ID"
    )
    async def get_single_resource(resource_id: int, db: AsyncSession = Depends(get_db)):
        """
        Retrieves a single resource by its unique SWAPI ID for this type.
        """
        stmt = select(SwapiResource.data).where(
            SwapiResource.type == resource_type,
            SwapiResource.swapi_id == resource_id
        )
        result = (await db.execute(stmt)).scalar_one_or_none()

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"{resource_type.capitalize()} with ID {resource_id} not found"
            )
        return result

    return router