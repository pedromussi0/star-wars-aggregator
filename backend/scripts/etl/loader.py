import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from swapi_search.db.models import SwapiResource

logger = logging.getLogger(__name__)

class DataLoader:
    """
    Handles loading the transformed data into the PostgreSQL database.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def load_data(self, data: List[Dict[str, Any]]):
        """
        Performs a bulk insert of normalized data into the database.

        Args:
            data: A list of dictionaries, where each represents a row to be inserted.
        """
        if not data:
            logger.warning("No data provided to load. Skipping.")
            return

        try:
            logger.info(f"Starting to load {len(data)} records into the database...")
            self.db_session.bulk_insert_mappings(SwapiResource, data)
            self.db_session.commit()
            logger.info("Successfully committed all records to the database.")
        except Exception as e:
            logger.error(f"Database load failed: {e}", exc_info=True)
            self.db_session.rollback()
            raise
        finally:
            self.db_session.close()