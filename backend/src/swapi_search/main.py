# src/swapi_search/main.py

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum  # <-- Import Mangum

from swapi_search.api.v1.endpoints.resources import resource_router_factory
from swapi_search.api.v1.endpoints.search import router as search_router
from swapi_search.api.v1.registry import RESOURCE_CONFIG

from swapi_search.core.config import settings
from swapi_search.core.logging import setup_logging
from swapi_search.db.session import async_engine, check_db_connection

# Setup structured logging for the application
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """
    logger.info("Application startup...")
    # This check now happens inside the custom Settings initializer
    # So we can be confident the connection details are present.
    await check_db_connection()
    yield
    logger.info("Closing database connection pool...")
    await async_engine.dispose()
    logger.info("Application shutdown.")


def create_app() -> FastAPI:
    """
    Application factory to create and configure the FastAPI app.
    """
    app = FastAPI(
        title="SWAPI Search and Browse Service",
        description="A service to ingest, search, and browse data from the Star Wars API.",
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
    for resource_type, config in RESOURCE_CONFIG.items():
        router = resource_router_factory(
            resource_type=resource_type.value,
            response_model=config["response_model"],
            filters_model=config.get("filters_model"),
            tag=resource_type.name.capitalize()
        )
        app.include_router(router, prefix=API_V1_PREFIX)

    @app.get("/health", tags=["Monitoring"])
    async def health_check():
        """Health check endpoint to verify service is running."""
        return {"status": "ok"}

    return app

# Create the application instance
app = create_app()

# === THIS IS THE CRITICAL FIX ===
# Create the Mangum handler which will be the entry point for AWS Lambda
handler = Mangum(app, lifespan="on")