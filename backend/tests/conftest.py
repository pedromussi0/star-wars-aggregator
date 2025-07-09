import pytest
from typing import AsyncGenerator

from fastapi.testclient import TestClient
from swapi_search.main import app
from swapi_search.search.base import BaseSearchEngine

@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)

class MockSearchEngine(BaseSearchEngine):
    """A mock search engine for testing purposes."""
    
    _results = []
    _should_raise_error = False
    
    async def search(self, query: str, resource_type: str | None = None, limit: int = 10, offset: int = 0):
        if self._should_raise_error:
            raise ValueError("Simulated search engine error")
        
        filtered_results = self._results
        if resource_type:
            filtered_results = [r for r in self._results if r.get("type") == resource_type]
            
        return filtered_results[offset : offset + limit]

    @classmethod
    def set_results(cls, results):
        cls._results = results

    @classmethod
    def clear(cls):
        cls._results = []
        cls._should_raise_error = False

@pytest.fixture
async def mock_search_engine() -> AsyncGenerator[MockSearchEngine, None]:
    """
    Provides a clean instance of the MockSearchEngine for each test.
    """
    engine = MockSearchEngine()
    yield engine
    engine.clear()