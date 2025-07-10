import logging
from typing import Dict, List, Any, Optional

from swapi_search.core.config import settings
from .data_models import SwapiBaseModel

logger = logging.getLogger(__name__)


class DataNormalizer:
    """
    Transforms raw SWAPI data into an enriched format for our database.
    It uses a resilient "enrich" strategy, replacing relational URL strings
    with rich objects containing both the URL and the resolved name/title.
    """

    def __init__(self):
        self.url_to_name_cache: Dict[str, str] = {}

    def _build_url_to_name_cache(self, raw_data: Dict[str, List[SwapiBaseModel]]):
        """
        Populates a cache mapping SWAPI URLs to their corresponding resource
        names or titles. This is a critical pre-computation step.
        """
        logger.info("Building URL-to-name cache for relationship resolution...")
        for items in raw_data.values():
            for item in items:
                name = getattr(item, "title", None) or getattr(item, "name", None)
                if item.url and name:
                    self.url_to_name_cache[item.url] = name
        logger.info(f"Cache built with {len(self.url_to_name_cache)} entries.")

    def _resolve_value_to_rich_object(self, value: Any) -> Any:
        """
        Transforms a relational URL or a list of URLs into a structured object.
        This function is designed to be resilient and will not discard data
        if a name lookup fails.
        """
        # For a list of URLs (e.g., a person's 'films' or a ship's 'pilots')
        if isinstance(value, list) and value and isinstance(value[0], str) and "http" in value[0]:
            resolved_objects = []
            for url in value:
                # --- THIS IS THE CRITICAL FIX ---
                # Always append the object. Use the looked-up name if it exists,
                # otherwise default to None. This prevents data loss.
                name = self.url_to_name_cache.get(url) # Will be None if not found
                name_key = "title" if "/films/" in url else "name"
                resolved_objects.append({"url": url, name_key: name})
                # --- END FIX ---
            return resolved_objects
        
        # For a single URL (e.g., a person's 'homeworld')
        if isinstance(value, str) and value in self.url_to_name_cache:
            name = self.url_to_name_cache.get(value)
            return {"url": value, "name": name}
            
        return value

    def _create_searchable_text(self, item_dict: Dict[str, Any]) -> str:
        # This function remains the same as the previous correct version.
        content = [item_dict.get(key, "") for key in ["name", "title", "model", "manufacturer", "director", "classification"]]
        for key, value in item_dict.items():
            if isinstance(value, dict) and 'name' in value and value['name']:
                content.append(value['name'])
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                for sub_item in value:
                    if sub_item.get('name'):
                        content.append(sub_item.get('name'))
                    if sub_item.get('title'):
                        content.append(sub_item.get('title'))
        return " ".join(filter(None, content)).lower()

    def normalize_all(self, raw_data: Dict[str, List[SwapiBaseModel]]) -> List[Dict[str, Any]]:
        # This function remains the same as the previous correct version.
        self._build_url_to_name_cache(raw_data)
        
        all_final_records = []
        for resource_type, items in raw_data.items():
            for item_model in items:
                enriched_data = item_model.model_dump()
                
                for key, value in list(enriched_data.items()):
                    if key != "url":
                        enriched_data[key] = self._resolve_value_to_rich_object(value)
                
                swapi_id = int(item_model.url.strip("/").split("/")[-1])
                our_api_url = f"{settings.API_BASE_URL}/api/v1/{resource_type}/{swapi_id}"
                enriched_data["url"] = our_api_url
                
                enriched_data["type"] = resource_type
                if "title" in enriched_data and "name" not in enriched_data:
                    enriched_data["name"] = enriched_data["title"]

                db_record = {
                    "swapi_id": swapi_id,
                    "type": resource_type,
                    "name": enriched_data.get("name", "Unknown"),
                    "data": enriched_data,
                    "searchable_text": self._create_searchable_text(enriched_data),
                }
                all_final_records.append(db_record)
        
        return all_final_records