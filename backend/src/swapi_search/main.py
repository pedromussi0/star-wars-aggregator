import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
from swapi_search.api.v1 import schemas
from swapi_search.api.v1.endpoints.resources import resource_router_factory

from swapi_search.api.v1.endpoints.search import router as search_router
from swapi_search.core.config import settings
from swapi_search.core.logging import setup_logging
from swapi_search.db.session import async_engine, check_db_connection

# Setup structured logging for the application
setup_logging()
logger = logging.getLogger(__name__)

class ResourceType(str, Enum):
    films = "films"
    people = "people"
    planets = "planets"
    species = "species"
    starships = "starships"
    vehicles = "vehicles"

RESOURCE_CONFIG = {
    ResourceType.films: schemas.FilmResponse,
    ResourceType.people: schemas.PersonResponse,
    ResourceType.planets: schemas.PlanetResponse,
    ResourceType.species: schemas.SpeciesResponse,
    ResourceType.starships: schemas.StarshipResponse,
    ResourceType.vehicles: schemas.VehicleResponse,
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup...")
    logger.info("Checking database connection...")
    await check_db_connection()
    yield
    logger.info("Closing database connection pool...")
    async_engine.dispose()
    logger.info("Application shutdown.")

app = FastAPI(
    title="SWAPI Search Service",
    description="A service to ingest and search data from the Star Wars API.",
    version="1.0.0",
    lifespan=lifespan,
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Routers ---

API_V1_PREFIX = "/api/v1"

app.include_router(search_router, prefix=API_V1_PREFIX)

for resource_type, response_model in RESOURCE_CONFIG.items():
    router = resource_router_factory(
        resource_type=resource_type.value,
        response_model=response_model,
        tag=resource_type.name.capitalize()
    )
    app.include_router(router, prefix=API_V1_PREFIX)

@app.get("/health", tags=["Monitoring"])
async def health_check():
    """
    Health check endpoint to verify service is running.
    """
    return {"status": "ok"}