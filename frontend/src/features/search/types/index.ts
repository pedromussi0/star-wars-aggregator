export type ResourceType = 'films' | 'people' | 'planets' | 'species' | 'starships' | 'vehicles';

interface BaseSearchResult {
  url: string;
  created: string;
  edited: string;
  type: ResourceType; 
}

export interface FilmResult extends BaseSearchResult {
  type: 'films';
  title: string;
  episode_id: number;
  opening_crawl: string;
  director: string;
  producer: string;
  release_date: string;
  characters: string[];
  planets: string[];
  starships: string[];
  vehicles: string[];
  species: string[];
}

export interface PersonResult extends BaseSearchResult {
  type: 'people';
  name: string;
  height: string;
  mass: string;
  hair_color: string;
  skin_color: string;
  eye_color: string;
  birth_year: string;
  gender: string;
  homeworld: string;
  films: string[];
  species: string[];
  vehicles: string[];
  starships: string[];
}

export interface PlanetResult extends BaseSearchResult {
  type: 'planets';
  name: string;
  rotation_period: string;
  orbital_period: string;
  diameter: string;
  climate: string;
  gravity: string;
  terrain: string;
  surface_water: string;
  population: string;
  residents: string[];
  films: string[];
}

export interface SpeciesResult extends BaseSearchResult {
  type: 'species';
  name: string;
  classification: string;
  designation: string;
  average_height: string;
  skin_colors: string;
  hair_colors: string;
  eye_colors: string;
  average_lifespan: string;
  homeworld: string | null; 
  language: string;
  people: string[];
  films: string[];
}

export interface StarshipResult extends BaseSearchResult {
  type: 'starships';
  name: string;
  model: string;
  manufacturer: string;
  cost_in_credits: string;
  length: string;
  max_atmosphering_speed: string;
  crew: string;
  passengers: string;
  cargo_capacity: string;
  consumables: string;
  hyperdrive_rating: string;
  MGLT: string;
  starship_class: string;
  pilots: string[];
  films: string[];
}

export interface VehicleResult extends BaseSearchResult {
  type: 'vehicles';
  name: string;
  model: string;
  manufacturer: string;
  cost_in_credits: string;
  length: string;
  max_atmosphering_speed: string;
  crew: string;
  passengers: string;
  cargo_capacity: string;
  consumables: string;
  vehicle_class: string;
  pilots: string[];
  films: string[];
}

export type SearchResultItem =
  | FilmResult
  | PersonResult
  | PlanetResult
  | SpeciesResult
  | StarshipResult
  | VehicleResult;

export type SearchApiResponse = {
  count: number;
  limit: number;
  offset: number;
  results: SearchResultItem[];
};

export type SearchParams = {
  q: string;
  type?: ResourceType;
  limit?: number;
  offset?: number;
};

export interface UnifiedSearchResult {
    resourceType: ResourceType;
    title: string;
    url: string; 
    summary: Record<string, string>;
  }