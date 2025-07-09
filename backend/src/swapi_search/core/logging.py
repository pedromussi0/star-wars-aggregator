import logging
import sys

from pythonjsonlogger import jsonlogger
from swapi_search.core.config import settings

def setup_logging():
    """
    Configures structured JSON logging for the application.
    """
    log_handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s"
    )
    log_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    
    # Avoid adding duplicate handlers
    if not root_logger.handlers:
        root_logger.addHandler(log_handler)
    
    root_logger.setLevel(settings.LOG_LEVEL.upper())
    
    # Suppress verbose logs from libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)