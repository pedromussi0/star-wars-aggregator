from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from swapi_search.db.models import SwapiResource
from swapi_search.db.session import get_db
from swapi_search.api.v1.schemas import PaginatedResponse
from swapi_search.repositories.resource import ResourceRepository

def get_resource_repository(db: AsyncSession = Depends(get_db)) -> ResourceRepository:
    """Dependency injector for the ResourceRepository."""
    return ResourceRepository(db_session=db)

def resource_router_factory(
    resource_type: str,
    response_model: type,
    tag: str
) -> APIRouter:
    """
    A factory that generates a set of RESTful endpoints for a resource type.
    
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
        repo: ResourceRepository = Depends(get_resource_repository),
        limit: int = Query(10, ge=1, le=100, description="Number of results to return."),
        offset: int = Query(0, ge=0, description="Offset for pagination."),
    ):
        """
        Retrieves a paginated list of all resources of this type from the
        database, ordered by their original SWAPI ID.
        """
        total_count = await repo.count_resources(resource_type=resource_type)
        items = await repo.get_all_resources(
            resource_type=resource_type, limit=limit, offset=offset
        )
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
    async def get_single_resource(
        resource_id: int,
        repo: ResourceRepository = Depends(get_resource_repository),
    ):
        """
        Retrieves a single resource by its unique SWAPI ID for this type.
        """
        item = await repo.get_resource_by_id(
            resource_type=resource_type, resource_id=resource_id
        )
        if item is None:
            raise HTTPException(
                status_code=404,
                detail=f"{resource_type.capitalize()} with ID {resource_id} not found"
            )
        return item

    return router