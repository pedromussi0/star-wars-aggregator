from typing import Dict, List, Any
from pydantic import BaseModel, Field


class SearchResultItem(BaseModel):
    """
    Represents a single search result item.
    The structure is generic to accommodate different resource types.
    """
    name: str = Field(..., description="The name or title of the resource.")
    type: str = Field(..., description="The type of the resource (e.g., 'people', 'films').")
    url: str = Field(..., description="The original SWAPI URL of the resource.")
    details: Dict[str, Any] = Field(..., description="Additional details specific to the resource type.")


class SearchResponse(BaseModel):
    """
    The response model for the search endpoint.
    Results are grouped by their resource type.
    """
    count: int = Field(..., description="Total number of results found across all types.")
    results: Dict[str, List[Dict[str, Any]]] = Field(
        ...,
        description="Search results, grouped by resource type.",
        example={
            "people": [{"name": "Luke Skywalker", "url": "...", "details": {}}],
            "planets": [{"name": "Tatooine", "url": "...", "details": {}}],
        },
    )

class PaginatedSearchResponse(BaseModel):
    count: int = Field(description="Total number of items matching the query.")
    limit: int = Field(description="The number of items per page.")
    offset: int = Field(description="The offset of the current page.")
    results: List[Dict[str, Any]] = Field(description="The list of search results for the current page.")