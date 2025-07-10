from typing import Dict, List, Any, Optional, TypeVar, Generic
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


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

DataType = TypeVar('DataType')

class PaginatedResponse(GenericModel, Generic[DataType]):
    """
    A generic, reusable paginated response structure.
    """
    count: int = Field(description="Total number of items available for the query.")
    limit: int = Field(description="The number of items requested per page.")
    offset: int = Field(description="The starting offset for the returned items.")
    results: List[DataType] = Field(description="The list of items for the current page.")



# --- API Response Models ---
# These models define the public contract for our browse endpoints. They are
# intentionally kept separate from the ETL data models.

class FilmRelation(BaseModel):
    url: str
    title: Optional[str] = None 

class PersonRelation(BaseModel):
    url: str
    name: Optional[str] = None 

class PlanetRelation(BaseModel):
    url: str
    name: Optional[str] = None 

class SpeciesRelation(BaseModel):
    url: str
    name: Optional[str] = None 

class StarshipRelation(BaseModel):
    url: str
    name: Optional[str] = None 

class VehicleRelation(BaseModel):
    url: str
    name: Optional[str] = None 

class FilmResponse(BaseModel):
    title: str
    episode_id: int
    director: str
    producer: str
    release_date: str
    characters: List[PersonRelation]
    planets: List[PlanetRelation]
    starships: List[StarshipRelation]
    vehicles: List[VehicleRelation]
    species: List[SpeciesRelation]
    url: str

    class Config:
        from_attributes = True

class PersonResponse(BaseModel):
    name: str
    height: str
    mass: str
    gender: str
    homeworld: Optional[PlanetRelation] = None
    films: List[FilmRelation]
    species: List[SpeciesRelation]
    vehicles: List[VehicleRelation]
    starships: List[StarshipRelation]
    url: str

    class Config:
        from_attributes = True


class PlanetResponse(BaseModel):
    name: str
    rotation_period: str
    orbital_period: str
    diameter: str
    climate: str
    gravity: str
    terrain: str
    surface_water: str
    population: str
    residents: List[PersonRelation]
    films: List[FilmRelation]
    url: str

    class Config:
        from_attributes = True

class SpeciesResponse(BaseModel):
    name: str
    classification: str
    designation: str
    average_height: str
    skin_colors: str
    hair_colors: str
    eye_colors: str
    average_lifespan: str
    homeworld: Optional[PlanetRelation] = None
    language: str
    people: List[PersonRelation]
    films: List[FilmRelation]
    url: str

    class Config:
        from_attributes = True

class StarshipResponse(BaseModel):
    name: str
    model: str
    manufacturer: str
    cost_in_credits: str
    length: str
    max_atmosphering_speed: str
    crew: str
    passengers: str
    cargo_capacity: str
    consumables: str
    hyperdrive_rating: str
    MGLT: str
    starship_class: str
    pilots: List[PersonRelation]
    films: List[FilmRelation]
    url: str

    class Config:
        from_attributes = True

class VehicleResponse(BaseModel):
    name: str
    model: str
    manufacturer: str
    cost_in_credits: str
    length: str
    max_atmosphering_speed: str
    crew: str
    passengers: str
    cargo_capacity: str
    consumables: str
    vehicle_class: str
    pilots: List[PersonRelation]
    films: List[FilmRelation]
    url: str

    class Config:
        from_attributes = True