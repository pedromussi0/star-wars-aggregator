from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query

from swapi_search.api.v1.dependencies import get_search_engine
from swapi_search.api.v1.schemas import PaginatedSearchResponse
from swapi_search.search.base import BaseSearchEngine

router = APIRouter(tags=["Search"])


@router.get(
    "/search",
    response_model=PaginatedSearchResponse,
    summary="Unified Search Across SWAPI Resources",
    description="Performs a case-insensitive, partial search across all indexed SWAPI resources. "
                "Results are paginated and can be filtered by resource type.",
)
async def search_resources(
    search_engine: Annotated[BaseSearchEngine, Depends(get_search_engine)],
    q: str = Query(
        ...,
        min_length=1,
        description="The search query term (e.g., 'skywalker', 'tatooine').",
    ),
    type: Optional[str] = Query(
        None,
        description="Filter results by resource type (e.g., 'people', 'films', 'planets').",
        enum=["films", "people", "planets", "species", "starships", "vehicles"],
    ),
    limit: int = Query(10, ge=1, le=100, description="Number of results to return per page."),
    offset: int = Query(0, ge=0, description="Offset for pagination."),
):
    """
    Search endpoint that leverages the search engine abstraction.
    """
    results = await search_engine.search(
        query=q, resource_type=type, limit=limit, offset=offset
    )
    
    return PaginatedSearchResponse(
        count=len(results), 
        limit=limit,
        offset=offset,
        results=results
    )