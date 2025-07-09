import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from swapi_search.api.v1.endpoints.search import router as search_router
from swapi_search.core.config import settings
from swapi_search.core.logging import setup_logging
from swapi_search.db.session import async_engine, check_db_connection

# Setup structured logging for the application
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events, such as initializing database connections.
    """
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
app.include_router(search_router, prefix="/api/v1")


@app.get("/health", tags=["Monitoring"])
async def health_check():
    """
    Health check endpoint to verify service is running.
    """
    return {"status": "ok"}