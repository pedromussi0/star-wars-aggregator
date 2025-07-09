"""
Pydantic models for validating the raw data fetched from the SWAPI API.

"""
from typing import List, Optional
from pydantic import BaseModel

class SwapiBaseModel(BaseModel):
    url: str
    created: str
    edited: str

class Film(SwapiBaseModel):
    title: str
    episode_id: int
    opening_crawl: str
    director: str
    producer: str
    release_date: str
    characters: List[str]
    planets: List[str]
    starships: List[str]
    vehicles: List[str]
    species: List[str]

class Person(SwapiBaseModel):
    name: str
    height: str
    mass: str
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: str
    gender: str
    homeworld: str
    films: List[str]
    species: List[str]
    vehicles: List[str]
    starships: List[str]

class Planet(SwapiBaseModel):
    name: str
    rotation_period: str
    orbital_period: str
    diameter: str
    climate: str
    gravity: str
    terrain: str
    surface_water: str
    population: str
    residents: List[str]
    films: List[str]

class Species(SwapiBaseModel):
    name: str
    classification: str
    designation: str
    average_height: str
    skin_colors: str
    hair_colors: str
    eye_colors: str
    average_lifespan: str
    homeworld: Optional[str] = None
    language: str
    people: List[str]
    films: List[str]

class Starship(SwapiBaseModel):
    name: str
    model: str
    manufacturer: str
    cost_in_credits: str
    length: str
    max_atmosphering_speed: str
    crew: str
    passengers: str
    cargo_capacity: str
    consumables: str
    hyperdrive_rating: str
    MGLT: str # Megalights
    starship_class: str
    pilots: List[str]
    films: List[str]

class Vehicle(SwapiBaseModel):
    name: str
    model: str
    manufacturer: str
    cost_in_credits: str
    length: str
    max_atmosphering_speed: str
    crew: str
    passengers: str
    cargo_capacity: str
    consumables: str
    vehicle_class: str
    pilots: List[str]
    films: List[str]

RESOURCE_MODEL_MAP = {
    "films": Film,
    "people": Person,
    "planets": Planet,
    "species": Species,
    "starships": Starship,
    "vehicles": Vehicle,
}