from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class BaseSearchEngine(ABC):
    """
    Abstract base class for a search engine.
    This interface defines the contract for all search implementations,
    allowing for swappable backends (e.g., PostgreSQL, Elasticsearch).
    """

    @abstractmethod
    async def search(
        self,
        query: str,
        resource_type: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Performs a search for resources.

        Args:
            query: The search term.
            resource_type: Optional filter to restrict search to a specific type.
            limit: The maximum number of results to return.
            offset: The starting point for pagination.

        Returns:
            A list of search results.
        """
        pass