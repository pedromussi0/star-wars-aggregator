from enum import Enum
from . import schemas

class ResourceType(str, Enum):
    """
    An enumeration of all supported resource types.
    This provides a single source of truth and prevents typos.
    """
    films = "films"
    people = "people"
    planets = "planets"
    species = "species"
    starships = "starships"
    vehicles = "vehicles"

# A centralized configuration dictionary that maps each resource type
# to its corresponding Pydantic models for responses and filtering.
#
# This registry is the single source of truth for configuring the
# browsable RESTful endpoints in the application. To add a new
# resource or update an existing one, you only need to modify this dictionary.
RESOURCE_CONFIG = {
    ResourceType.films: {
        "response_model": schemas.FilmResponse,
        "filters_model": schemas.FilmFilters,
    },
    ResourceType.people: {
        "response_model": schemas.PersonResponse,
        "filters_model": schemas.PersonFilters,
    },
    ResourceType.planets: {
        "response_model": schemas.PlanetResponse,
        "filters_model": schemas.PlanetFilters,
    },
    ResourceType.species: {
        "response_model": schemas.SpeciesResponse,
        "filters_model": schemas.SpeciesFilters,
    },
    ResourceType.starships: {
        "response_model": schemas.StarshipResponse,
        "filters_model": schemas.StarshipFilters,
    },
    ResourceType.vehicles: {
        "response_model": schemas.VehicleResponse,
        "filters_model": schemas.VehicleFilters,
    },
}