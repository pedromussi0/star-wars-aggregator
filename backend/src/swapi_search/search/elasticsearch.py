from typing import List, Optional, Dict, Any

from swapi_search.search.base import BaseSearchEngine


class ElasticSearchEngine(BaseSearchEngine):
    """
    A placeholder for a future Elasticsearch-based search engine.
    This demonstrates the swappable nature of the search abstraction.
    """

    async def search(
        self,
        query: str,
        resource_type: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        This method would contain the logic to query an Elasticsearch index.
        """
        print(
            "Elasticsearch engine is not implemented. "
            "This is a placeholder for future extension."
        )
        return []