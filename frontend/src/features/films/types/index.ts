export interface Film {
    url: string;
    title: string;
    episode_id: number;
    director: string;
    release_date: string;
  }
  
  interface RelatedEntity {
    url: string;
    name?: string;
    title?: string;
  }
  
  export interface FilmDetails extends Film {
    opening_crawl: string;
    producer: string;
    characters: RelatedEntity[];
    planets: RelatedEntity[];
    starships: RelatedEntity[];
    vehicles: RelatedEntity[];
    species: RelatedEntity[];
  }