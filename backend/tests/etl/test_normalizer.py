from scripts.etl.normalizer import DataNormalizer

# Sample raw data mimicking the structure from SWAPI
SAMPLE_RAW_DATA = {
    "planets": [
        {"name": "Tatooine", "climate": "arid", "url": "https://swapi.info/api/planets/1/"}
    ],
    "people": [
        {
            "name": "Luke Skywalker",
            "homeworld": "https://swapi.info/api/planets/1/",
            "films": ["https://swapi.info/api/films/1/"],
            "url": "https://swapi.info/api/people/1/",
        }
    ],
    "films": [
        {
            "title": "A New Hope",
            "characters": ["https://swapi.info/api/people/1/"],
            "url": "https://swapi.info/api/films/1/",
        }
    ],
}

def test_data_normalizer_url_resolution():
    """
    Tests that the DataNormalizer correctly resolves SWAPI URLs to names.
    """
    # Arrange
    normalizer = DataNormalizer()

    # Act
    normalized_data = normalizer.normalize_all(SAMPLE_RAW_DATA)

    # Assert
    luke_record = next(item for item in normalized_data if item["name"] == "Luke Skywalker")
    film_record = next(item for item in normalized_data if item["name"] == "A New Hope")
    
    # Check that URLs in 'homeworld' and 'films' fields are replaced by names
    assert luke_record["data"]["homeworld"] == "Tatooine"
    assert luke_record["data"]["films"] == ["A New Hope"]
    
    # Check that URLs in 'characters' are also replaced
    assert film_record["data"]["characters"] == ["Luke Skywalker"]

def test_data_normalizer_searchable_text_creation():
    """
    Tests that the searchable_text field is created correctly.
    """
    # Arrange
    normalizer = DataNormalizer()

    # Act
    normalized_data = normalizer.normalize_all(SAMPLE_RAW_DATA)

    # Assert
    luke_record = next(item for item in normalized_data if item["name"] == "Luke Skywalker")
    planet_record = next(item for item in normalized_data if item["name"] == "Tatooine")
    
    assert "luke skywalker" in luke_record["searchable_text"]
    assert "tatooine" in planet_record["searchable_text"]
    assert "arid" in planet_record["searchable_text"]

def test_data_normalizer_structure():
    """
    Tests that the final normalized records have the correct structure.
    """
    # Arrange
    normalizer = DataNormalizer()

    # Act
    normalized_data = normalizer.normalize_all(SAMPLE_RAW_DATA)
    first_record = normalized_data[0]

    # Assert
    assert len(normalized_data) == 3 # planets: 1, people: 1, films: 1
    assert "swapi_id" in first_record
    assert "type" in first_record
    assert "name" in first_record
    assert "data" in first_record
    assert "searchable_text" in first_record
    assert isinstance(first_record["data"], dict)