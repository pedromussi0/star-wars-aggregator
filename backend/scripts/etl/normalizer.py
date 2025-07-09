import logging
from typing import Dict, List, Any

from .data_models import SwapiBaseModel

logger = logging.getLogger(__name__)


class DataNormalizer:
    """
    Transforms raw SWAPI data from Pydantic models into a structured format
    suitable for the database.
    """

    def __init__(self):
        self.url_to_name_cache: Dict[str, str] = {}

    def _build_url_to_name_cache(self, raw_data: Dict[str, List[SwapiBaseModel]]):
        """Populates a cache mapping SWAPI URLs to resource names."""
        logger.info("Building URL-to-name cache for relationship resolution...")
        for resource_type, items in raw_data.items():
            for item in items:
                name = getattr(item, "title", None) or getattr(item, "name", None)
                if item.url and name:
                    self.url_to_name_cache[item.url] = name
        logger.info(f"Cache built with {len(self.url_to_name_cache)} entries.")

    def _resolve_urls(self, value: Any) -> Any:
        """Recursively replaces URLs with their cached names."""
        if isinstance(value, str) and value in self.url_to_name_cache:
            return self.url_to_name_cache[value]
        if isinstance(value, list):
            return [self._resolve_urls(item) for item in value]
        return value

    def _create_searchable_text(self, item_dict: Dict[str, Any], resource_type: str) -> str:
        """Creates a concatenated string of key fields for full-text search."""
        
        searchable_fields = []
        field_map = {
            "people": ["name", "gender", "hair_color", "skin_color"],
            "films": ["title", "director", "producer", "opening_crawl"],
            "planets": ["name", "climate", "terrain"],
            "species": ["name", "classification", "designation", "language"],
            "starships": ["name", "model", "manufacturer", "starship_class"],
            "vehicles": ["name", "model", "manufacturer", "vehicle_class"],
        }
        fields_to_index = field_map.get(resource_type, ["name", "title"])
        for key, value in item_dict.items():
            if key in fields_to_index and isinstance(value, str):
                searchable_fields.append(value.strip())
        return " ".join(filter(None, searchable_fields)).lower()

    def _normalize_item(self, item_model: SwapiBaseModel, resource_type: str) -> Dict[str, Any]:
        """Normalizes a single Pydantic model instance."""
        item_dict = item_model.model_dump()
        normalized_item = {}
        for key, value in item_dict.items():
            normalized_item[key] = self._resolve_urls(value)
        normalized_item["type"] = resource_type
        if "title" in normalized_item and "name" not in normalized_item:
            normalized_item["name"] = normalized_item["title"]
        return normalized_item

    def normalize_all(self, raw_data: Dict[str, List[SwapiBaseModel]]) -> List[Dict[str, Any]]:
        """Normalizes all fetched data."""
        self._build_url_to_name_cache(raw_data)
        
        all_normalized_items = []
        for resource_type, items in raw_data.items():
            for item_model in items:
                item_dict_raw = item_model.model_dump()
                normalized_data_obj = self._normalize_item(item_model, resource_type)
                
                db_record = {
                    "swapi_id": int(item_model.url.strip("/").split("/")[-1]),
                    "type": resource_type,
                    "name": normalized_data_obj.get("name", "Unknown"),
                    "data": normalized_data_obj,
                    "searchable_text": self._create_searchable_text(item_dict_raw, resource_type),
                }
                all_normalized_items.append(db_record)
        
        return all_normalized_items