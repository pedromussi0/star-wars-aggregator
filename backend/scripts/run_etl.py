import asyncio
import logging
from swapi_search.core.logging import setup_logging
from swapi_search.db.session import sync_engine, SyncSessionLocal
from swapi_search.db.models import Base
from etl.swapi_client import SwapiClient
from etl.normalizer import DataNormalizer
from etl.loader import DataLoader
from sqlalchemy import text

# Setup logging before any other imports that might initialize logging
setup_logging()
logger = logging.getLogger(__name__)

# Define all resource types to be processed
RESOURCE_TYPES = ["films", "people", "planets", "species", "starships", "vehicles"]

async def run_etl_pipeline():
    """
    Orchestrates the entire ETL (Extract, Transform, Load) process.
    """
    logger.info("Starting SWAPI ETL pipeline...")

    # --- Setup ---
    client = SwapiClient()
    normalizer = DataNormalizer()
    db_session = SyncSessionLocal()
    loader = DataLoader(db_session)

    try:
        with sync_engine.connect() as connection:
            connection.execute(text("TRUNCATE TABLE swapi_resource RESTART IDENTITY;"))
            connection.commit()
        # --- Extract ---
        logger.info("Phase 1: Extracting all data from SWAPI...")
        raw_data = {}
        for resource_type in RESOURCE_TYPES:
            raw_data[resource_type] = await client.fetch_all_resources(resource_type)
        logger.info("Data extraction complete.")
        
        # --- Transform ---
        logger.info("Phase 2: Normalizing and enriching data...")
        normalized_data = normalizer.normalize_all(raw_data)
        logger.info("Data normalization complete.")
        
        # --- Load ---
        logger.info("Phase 3: Loading data into PostgreSQL...")
        loader.load_data(normalized_data)
        logger.info("Data loading complete.")

        logger.info("ETL pipeline finished successfully!")

    except Exception as e:
        logger.error(f"An error occurred during the ETL process: {e}", exc_info=True)
    finally:
        db_session.close()
        await client.close()

if __name__ == "__main__":
    asyncio.run(run_etl_pipeline())