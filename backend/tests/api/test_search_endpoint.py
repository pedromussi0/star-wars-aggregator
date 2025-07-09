from fastapi.testclient import TestClient
import pytest

from swapi_search.main import app
from swapi_search.api.v1.dependencies import get_search_engine
from tests.conftest import MockSearchEngine


MOCK_RESULTS = [
    {"name": "Luke Skywalker", "type": "people", "url": "...", "details": {}},
    {"name": "Leia Organa", "type": "people", "url": "...", "details": {}},
    {"name": "Tatooine", "type": "planets", "url": "...", "details": {}},
    {"name": "Sand Crawler", "type": "vehicles", "url": "...", "details": {}},
    {"name": "Death Star", "type": "starships", "url": "...", "details": {}},
]

@pytest.fixture(autouse=True)
def override_dependencies(mock_search_engine: MockSearchEngine):
    """
    This fixture automatically replaces the real search engine with our mock
    for every test in this file. It's a clean way to manage dependencies.
    `autouse=True` makes it apply to all tests here without needing to be passed as an argument.
    """
    mock_search_engine.set_results(MOCK_RESULTS)
    app.dependency_overrides[get_search_engine] = lambda: mock_search_engine
    yield
    # Teardown: clear the overrides after tests are done
    app.dependency_overrides.clear()
    mock_search_engine.clear()


def test_search_endpoint_success(client: TestClient):
    """Tests a successful query returning multiple results."""
    response = client.get("/api/v1/search?q=test")

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 5
    assert len(data["results"]) == 5
    assert data["results"][0]["name"] == "Luke Skywalker"


def test_search_endpoint_with_type_filter(client: TestClient):
    """Tests filtering by a specific resource type."""
    response = client.get("/api/v1/search?q=luke&type=people")

    assert response.status_code == 200
    data = response.json()
    
    assert data["count"] == 2
    assert all(r["type"] == "people" for r in data["results"])


def test_search_pagination_limit(client: TestClient):
    """Tests that the 'limit' parameter correctly paginates results."""
    response = client.get("/api/v1/search?q=test&limit=2")

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2 
    assert len(data["results"]) == 2
    assert data["results"][0]["name"] == "Luke Skywalker"
    assert data["results"][1]["name"] == "Leia Organa"


def test_search_pagination_offset(client: TestClient):
    """Tests that the 'offset' parameter correctly skips results."""
    response = client.get("/api/v1/search?q=test&limit=2&offset=2")

    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 2
    assert data["results"][0]["name"] == "Tatooine"


def test_search_endpoint_no_query_param(client: TestClient):
    """Tests that a 422 is returned if the 'q' query parameter is missing."""
    response = client.get("/api/v1/search")
    assert response.status_code == 422 # Unprocessable Entity
    assert "field required" in response.text


def test_search_endpoint_invalid_type_filter(client: TestClient):
    """Tests that an invalid 'type' enum value returns a 422 error."""
    response = client.get("/api/v1/search?q=test&type=invalid_type")
    assert response.status_code == 422
    assert "Input should be" in response.text