import asyncio
import logging
from typing import List, Dict, Any

import httpx
from pydantic import BaseModel, ValidationError
from tenacity import retry, stop_after_attempt, wait_exponential

from swapi_search.core.config import settings
from .data_models import RESOURCE_MODEL_MAP

logger = logging.getLogger(__name__)

class SwapiClient:
    """
    An asynchronous client for fetching data from the Star Wars API (swapi.info).
    This client is designed based on the observed API behavior:
    1. List endpoints (/api/resource) return a complete, non-paginated JSON array.
    2. Detail endpoints (/api/resource/uid) return a flat JSON object.
    """
    def __init__(self):
        self.base_url = settings.SWAPI_BASE_URL
        # Use concurrent connections for fetching detail URLs in parallel
        limits = httpx.Limits(max_connections=20, max_keepalive_connections=10)
        self.client = httpx.AsyncClient(timeout=20.0, limits=limits)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=6))
    async def _fetch_url(self, url: str) -> Any:
        """
        Fetches and returns the JSON from any given URL. The return type can be
        a list or a dictionary depending on the endpoint.
        """
        logger.debug(f"Fetching URL: {url}")
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def fetch_all_resources(self, resource_type: str) -> List[BaseModel]:
        """
        Fetches all items for a resource type by first getting the list of all
        items, then fetching each detail URL concurrently.
        """
        model_to_validate = RESOURCE_MODEL_MAP.get(resource_type)
        if not model_to_validate:
            logger.error(f"No Pydantic model defined for resource type: {resource_type}")
            return []

        logger.info(f"[{resource_type.upper()}] Stage 1: Fetching list view to gather all detail URLs.")
        try:
            list_view_url = f"{self.base_url}/{resource_type}"
            # The list view returns a plain list of summary objects
            list_response = await self._fetch_url(list_view_url)

            if not isinstance(list_response, list):
                logger.error(f"Expected a list from {list_view_url} but got {type(list_response)}")
                return []

            detail_urls = [item['url'] for item in list_response if 'url' in item]
            logger.info(f"[{resource_type.upper()}] Stage 1 Complete: Found {len(detail_urls)} detail URLs.")

            logger.info(f"[{resource_type.upper()}] Stage 2: Fetching all detail URLs concurrently.")
            fetch_tasks = [self._fetch_url(url) for url in detail_urls]
            detail_responses = await asyncio.gather(*fetch_tasks, return_exceptions=True)

            all_validated_items: List[BaseModel] = []
            for i, res in enumerate(detail_responses):
                if isinstance(res, Exception):
                    logger.error(f"Failed to fetch detail URL {detail_urls[i]}: {res}")
                    continue

                try:
                    # The detail response is a flat object, ready for validation
                    validated_item = model_to_validate.model_validate(res)
                    all_validated_items.append(validated_item)
                except ValidationError as e:
                    url = res.get('url', detail_urls[i])
                    logger.warning(f"Validation failed for item at {url}: {e}. Skipping.")

            logger.info(f"[{resource_type.upper()}] Stage 2 Complete: Successfully validated {len(all_validated_items)} items.")
            return all_validated_items

        except Exception as e:
            logger.error(f"A critical error occurred during ETL for '{resource_type}': {e}", exc_info=True)
            return []

    async def close(self):
        await self.client.aclose()